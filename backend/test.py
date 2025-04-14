from database import engine

if __name__ == "__main__":
    connection = None
    try:
        connection = engine.connect()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed
            print("✅ Database connection closed.")