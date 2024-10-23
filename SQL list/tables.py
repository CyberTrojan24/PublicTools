def list_tables(data):
    """
    Lists all tables in the database
    """
    if not data:
        print("No tables exist")
        return
    
    print("Tables:")
    for table_name in data.keys():
        print(f"- {table_name}")
