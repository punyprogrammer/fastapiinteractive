from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import (
    Field,
    Session,
    SQLModel,
    create_engine,
    select,
)


# ============================================================
# 1. DATABASE MODELS
# ============================================================

class HeroBase(SQLModel):
    # These fields are shared by multiple models.
    #
    # index=True creates a database index.
    # An index makes lookups/filtering on these columns faster.
    name: str = Field(index=True)
    age: int | None = Field(
        default=None,
        index=True,
    )


class Hero(HeroBase, table=True):
    """
    Actual DATABASE TABLE.

    table=True tells SQLModel:
        "Create a database table for this class."

    The resulting table is roughly:

        hero
        --------------------------------
        id
        name
        age
        secret_name

    id is the PRIMARY KEY, meaning every hero has
    a unique identifier.
    """

    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
    )

    secret_name: str


class HeroPublic(HeroBase):
    """
    Response model.

    This model is NOT a database table.

    It defines what the API is allowed to return to clients.

    Notice that secret_name is NOT included.

    Therefore:

        Database:
        id + name + age + secret_name

        API response:
        id + name + age

    This prevents accidentally exposing secret_name.
    """

    id: int


class HeroCreate(HeroBase):
    """
    Request model used when CREATING a hero.

    Client sends:

        POST /heroes/

        {
            "name": "Deadpond",
            "age": 35,
            "secret_name": "Dive Wilson"
        }

    This model validates that incoming data.
    """

    secret_name: str


class HeroUpdate(SQLModel):
    """
    Request model used when UPDATING a hero.

    Every field is optional because PATCH means:

        "Update only the fields I provide."

    Example:

        PATCH /heroes/1

        {
            "age": 40
        }

    Only age should change.
    """

    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

# SQLite database file.
#
# This will create/use:
#
#     database.db
#
# in the current project directory.
sqlite_file_name = "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"


# SQLite normally restricts a connection to the thread
# that created it.
#
# FastAPI can execute different parts of a request using
# different threads, so we disable that SQLite restriction.
connect_args = {
    "check_same_thread": False,
}


# The ENGINE is responsible for managing connections
# between our Python application and the database.
#
# Think of the engine as the database connection manager.
#
# IMPORTANT:
#
# Engine != Session
#
# Engine:
#     Manages database connections.
#
# Session:
#     Used by our application to actually perform
#     database operations.
engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
)


# ============================================================
# 3. CREATE DATABASE TABLES
# ============================================================

def create_db_and_tables():
    """
    Create all SQLModel tables if they don't already exist.

    SQLModel.metadata contains information about models
    such as:

        Hero
        Hero fields
        Primary keys
        Table structure

    create_all() tells SQLAlchemy/SQLModel:

        "Make sure these tables exist in the database."
    """

    SQLModel.metadata.create_all(engine)


# ============================================================
# 4. DATABASE SESSION MANAGEMENT
# ============================================================

def get_session():
    """
    Create ONE database session for a request.

    The important part is:

        with Session(engine) as session:

    This opens a database session.

    The session is then yielded to the FastAPI endpoint.

    When the request is finished, the 'with' block automatically
    closes the session.

    Conceptually:

        HTTP request
             ↓
        create Session
             ↓
        endpoint uses Session
             ↓
        request finishes
             ↓
        Session closes


    Why do we need a session?

    The session is the object through which we perform
    database operations such as:

        session.add()
        session.get()
        session.exec()
        session.delete()
        session.commit()
        session.refresh()


    IMPORTANT:

    We should NOT create one global Session and reuse it
    for every request.

    Instead:

        Request 1 → Session 1
        Request 2 → Session 2
        Request 3 → Session 3

    Each request gets its own session.
    """

    with Session(engine) as session:
        yield session


# ============================================================
# 5. FASTAPI DEPENDENCY FOR DATABASE SESSION
# ============================================================

# This is a convenient type alias for:

#
#     session: Session = Depends(get_session)
#
# Whenever an endpoint declares:
#
#     session: SessionDep
#
# FastAPI automatically:
#
#     1. Calls get_session()
#     2. Gets the yielded Session
#     3. Passes that Session into the endpoint
#     4. Closes the Session when the request is finished
#
SessionDep = Annotated[
    Session,
    Depends(get_session),
]


# ============================================================
# 6. FASTAPI APPLICATION
# ============================================================

app = FastAPI()


# ============================================================
# 7. APPLICATION STARTUP
# ============================================================

@app.on_event("startup")
def on_startup():
    """
    Runs when the FastAPI application starts.

    This makes sure the database tables exist before
    requests start arriving.

    Flow:

        Start FastAPI
             ↓
        on_startup()
             ↓
        create_db_and_tables()
             ↓
        Tables created if necessary
    """

    create_db_and_tables()


# ============================================================
# 8. CREATE HERO
# ============================================================

@app.post(
    "/heroes/",
    response_model=HeroPublic,
)
def create_hero(
    hero: HeroCreate,
    session: SessionDep,
):
    """
    Create a new hero.

    Request:

        POST /heroes/

        {
            "name": "Deadpond",
            "age": 35,
            "secret_name": "Dive Wilson"
        }

    FastAPI automatically converts the JSON request body
    into a HeroCreate object.

    At the same time, FastAPI injects a database Session.
    """

    # Convert the API input model into the database model.
    #
    # HeroCreate:
    #
    #     name
    #     age
    #     secret_name
    #
    # becomes Hero:
    #
    #     id
    #     name
    #     age
    #     secret_name
    #
    # id is initially None.
    db_hero = Hero.model_validate(hero)


    # Add the object to the SQLAlchemy/SQLModel session.
    #
    # IMPORTANT:
    #
    # session.add() does NOT immediately permanently
    # save the record to the database.
    #
    # It tells the session:
    #
    #     "I want this object to be inserted."
    #
    # The actual transaction is persisted when we commit.
    session.add(db_hero)


    # Commit the transaction.
    #
    # This is where the INSERT is actually committed
    # to the database.
    #
    # Conceptually:
    #
    #     session.add()
    #          ↓
    #     object pending
    #          ↓
    #     session.commit()
    #          ↓
    #     INSERT committed to DB
    session.commit()


    # Refresh the Python object using the latest values
    # from the database.
    #
    # This is especially useful because the database may have
    # generated values.
    #
    # For example:
    #
    #     id = 1
    #
    # was generated by the database.
    #
    # refresh() loads that generated value back into db_hero.
    session.refresh(db_hero)


    # FastAPI uses HeroPublic as the response model.
    #
    # Therefore secret_name will NOT be returned.
    return db_hero


# ============================================================
# 9. GET ALL HEROES
# ============================================================

@app.get(
    "/heroes/",
    response_model=list[HeroPublic],
)
def read_heroes(
    session: SessionDep,

    # Number of records to skip.
    #
    # Example:
    #
    # offset=10
    #
    # means:
    #
    #     Skip the first 10 records.
    offset: int = 0,

    # Maximum number of records to return.
    #
    # Query(le=100) means FastAPI will reject values
    # greater than 100.
    #
    # This prevents someone from requesting an
    # unnecessarily huge number of records.
    limit: Annotated[
        int,
        Query(le=100),
    ] = 100,
):
    """
    Retrieve multiple heroes.

    Example:

        GET /heroes/

    Or:

        GET /heroes/?offset=10&limit=20
    """

    # select(Hero)
    #
    # means:
    #
    #     SELECT * FROM hero
    #
    # offset() and limit() implement pagination.
    statement = (
        select(Hero)
        .offset(offset)
        .limit(limit)
    )


    # session.exec() executes the SQL query.
    #
    # .all() converts the result into a Python list.
    #
    # Conceptually:
    #
    #     Python
    #       ↓
    #     SQLModel
    #       ↓
    #     SQLAlchemy
    #       ↓
    #     SQL
    #       ↓
    #     SQLite
    #       ↓
    #     rows
    #       ↓
    #     Python objects
    heroes = session.exec(statement).all()


    return heroes


# ============================================================
# 10. GET ONE HERO
# ============================================================

@app.get(
    "/heroes/{hero_id}",
    response_model=HeroPublic,
)
def read_hero(
    hero_id: int,
    session: SessionDep,
):
    """
    Retrieve ONE hero using its primary key.

    Example:

        GET /heroes/5

    FastAPI extracts:

        hero_id = 5
    """

    # session.get() is designed for retrieving an object
    # using its PRIMARY KEY.
    #
    # This is conceptually:
    #
    #     SELECT * FROM hero WHERE id = 5
    #
    hero = session.get(
        Hero,
        hero_id,
    )


    # If no record exists, session.get() returns None.
    if not hero:
        raise HTTPException(
            status_code=404,
            detail="Hero not found",
        )


    return hero


# ============================================================
# 11. UPDATE HERO
# ============================================================

@app.patch(
    "/heroes/{hero_id}",
    response_model=HeroPublic,
)
def update_hero(
    hero_id: int,
    hero: HeroUpdate,
    session: SessionDep,
):
    """
    Partially update an existing hero.

    Example:

        PATCH /heroes/1

        {
            "age": 40
        }

    Only age should be modified.
    """


    # --------------------------------------------------------
    # STEP 1: Fetch the existing database object
    # --------------------------------------------------------

    hero_db = session.get(
        Hero,
        hero_id,
    )

    if not hero_db:
        raise HTTPException(
            status_code=404,
            detail="Hero not found",
        )


    # --------------------------------------------------------
    # STEP 2: Get only fields provided by the client
    # --------------------------------------------------------

    # Suppose the client sends:
    #
    # {
    #     "age": 40
    # }
    #
    # Because of exclude_unset=True:
    #
    # hero_data becomes:
    #
    # {
    #     "age": 40
    # }
    #
    # It will NOT contain:
    #
    #     name
    #     secret_name
    #
    # Therefore those fields remain unchanged.
    hero_data = hero.model_dump(
        exclude_unset=True,
    )


    # --------------------------------------------------------
    # STEP 3: Apply changes to the database object
    # --------------------------------------------------------

    # Update the existing Hero object in memory.
    #
    # For example:
    #
    # hero_db.age = 40
    #
    # The session is already tracking hero_db because
    # it was retrieved using session.get().
    hero_db.sqlmodel_update(hero_data)


    # --------------------------------------------------------
    # STEP 4: Commit the transaction
    # --------------------------------------------------------

    # SQLAlchemy detects that hero_db changed and generates
    # the appropriate UPDATE statement.
    #
    # Conceptually:
    #
    #     UPDATE hero
    #     SET age = 40
    #     WHERE id = hero_id
    #
    session.commit()


    # --------------------------------------------------------
    # STEP 5: Refresh the object
    # --------------------------------------------------------

    # Reload the object from the database so our Python object
    # represents the latest database state.
    session.refresh(hero_db)


    return hero_db


# ============================================================
# 12. DELETE HERO
# ============================================================

@app.delete("/heroes/{hero_id}")
def delete_hero(
    hero_id: int,
    session: SessionDep,
):
    """
    Delete a hero.

    Example:

        DELETE /heroes/5
    """


    # --------------------------------------------------------
    # STEP 1: Find the hero
    # --------------------------------------------------------

    hero = session.get(
        Hero,
        hero_id,
    )

    if not hero:
        raise HTTPException(
            status_code=404,
            detail="Hero not found",
        )


    # --------------------------------------------------------
    # STEP 2: Mark the object for deletion
    # --------------------------------------------------------

    # This tells the session:
    #
    #     "Delete this object when the transaction commits."
    #
    # The deletion isn't permanently committed yet.
    session.delete(hero)


    # --------------------------------------------------------
    # STEP 3: Commit the deletion
    # --------------------------------------------------------

    # This actually persists the DELETE operation.
    #
    # Conceptually:
    #
    #     DELETE FROM hero
    #     WHERE id = hero_id
    #
    session.commit()


    return {
        "ok": True,
    }
