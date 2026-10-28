# database.py
from pymongo import MongoClient

# REPLACE this string with your real MongoDB connection string!
MONGO_URI = "mongodb+srv://admin:hacktoberfest2026@cluster0.oo6sqgn.mongodb.net/?retryWrites=true&w=majority"

def connect_to_vault():
    """Connects to the MongoDB Atlas Memory Vault."""
    try:
        client = MongoClient(MONGO_URI)
        db = client.phantom_debugger
        print("🔮 Successfully connected to the Memory Vault (MongoDB).")
        return db.ancient_logs
    except Exception as e:
        print(f"❌ Failed to connect to the vault: {e}")
        return None

def seed_ancient_texts(collection):
    """Populates the vault with legacy error logs and their resolutions."""
    legacy_data = [
        {
            "error_code": "500",
            "log_pattern": "Database Connection Timeout",
            "resolution": "Increase connection pool timeout in config.yml to 30s.",
            "status": "dead"
        },
        {
            "error_code": "403",
            "log_pattern": "Invalid API Key Token",
            "resolution": "Regenerate OAuth token in the IAM console and restart service.",
            "status": "dead"
        }
    ]
    
    # Clear old data and insert fresh dummy data
    collection.delete_many({})
    collection.insert_many(legacy_data)
    print("📜 Ancient texts successfully written to the vault.")

if __name__ == "__main__":
    collection = connect_to_vault()
    if collection is not None:
        seed_ancient_texts(collection)
