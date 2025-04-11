import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def init_db():
    """Initialize database and create initial migration"""
    # Clean up any existing migration files if needed
    os.system("rm -rf migrations/*")
    
    # Initialize aerich
    os.system("aerich init-db")
    
    print("Database initialized and initial migration created!")

if __name__ == "__main__":
    asyncio.run(init_db())
