import os
import dotenv

dotenv.load_dotenv()

# Create class with config constants
class Config:
    NAME=os.getenv("DB_NAME")
    USER=os.getenv("DB_USER")
    PASSWORD=os.getenv("DB_PASSWORD")
    HOST=os.getenv("DB_HOST")
    PORT=os.getenv("DB_PORT")