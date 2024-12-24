import reflex as rx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#DATABASE_URL = os.getenv("NEON_DATABASE_URL")
DATABASE_URL = "sqlite:///reflex.db"

config = rx.Config(
    app_name="full_stack_python",
    db_url=DATABASE_URL, 
)   