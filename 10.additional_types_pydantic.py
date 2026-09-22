from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


# Annotated combines a Python type with FastAPI metadata.
# Body() tells FastAPI to read the value from the request body.
#
# UUID       → Unique identifier
# datetime   → Date + time
# timedelta  → Duration
# time       → Time of day
#
# Sample values:
# UUID       → "550e8400-e29b-41d4-a716-446655440000"
# datetime   → "2026-09-22T10:00:00"
# timedelta  → "02:30:00"
# time       → "18:30:00"


@app.put("/items/{item_id}")
def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[Union[time, None], Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process

    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
