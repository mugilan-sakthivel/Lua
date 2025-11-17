
import os
from dotenv import load_dotenv
from src.tools.component_database import initialize_component_database

# Load environment variables from .env file
load_dotenv()

# Check if DATABASE_URL is set
if not os.getenv("DATABASE_URL"):
    print("❌ DATABASE_URL environment variable not set.")
    print("Please create a .env file with your Supabase connection string.")
else:
    print("🚀 Initializing component database with mock data...")
    initialize_component_database()
    print("✅ Database initialization complete.")
