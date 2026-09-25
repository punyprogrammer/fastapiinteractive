from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# Storage for notifications (simulating a log file)
notifications_log = []


class UserRegistration(BaseModel):
    """Model for user registration data."""
    username: str
    email: str


def write_notification(email: str, message: str):
    """
    Background task function to write notification to log.
    This simulates sending an email notification.
    """
    notifications_log.append(f"Notification to {email}: {message}")


def send_welcome_email(username: str, email: str):
    """
    Background task to send a welcome email to new users.
    """

    notifications_log.append(f"Welcome email sent to {email} for user {username}")


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    Send a notification to the specified email address.
    The notification should be processed in the background.
    """ 
    background_tasks.add_task(write_notification,email,"Account activity detected")
    return {"message": "Notification sent in the background"}


@app.post("/register")
async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
    """
    Register a new user and send a welcome email in the background.
    """
    background_tasks.add_task(send_welcome_email,user.username,user.email)
    return {"message": "User registered successfully", "username": user.username}


@app.get("/notifications")
async def get_notifications():
    """
    Get all notifications that have been logged.
    This endpoint helps verify that background tasks executed.
    """
    return {"notifications": notifications_log, "count": len(notifications_log)}

