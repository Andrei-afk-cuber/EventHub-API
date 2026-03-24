import os
import dotenv

dotenv.load_dotenv()

# Create class with config constants
class Config:
    NAME=os.getenv("NAME")
    USER=os.getenv("USER")
    PASSWORD=os.getenv("PASSWORD")
    HOST=os.getenv("HOST")
    PORT=os.getenv("PORT")