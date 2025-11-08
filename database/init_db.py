from db_connection import init_database

if __name__ == '__main__':
    print("Initializing Job Portal Database...")
    init_database()
    print("Database setup complete!")