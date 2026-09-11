from database.db import get_db_connection

print("Starting project DB test...", flush=True)

try:
    connection = get_db_connection()

    print("CONNECTED!", flush=True)
    print("Database:", connection.database, flush=True)

    connection.close()

    print("Connection closed.", flush=True)

except Exception as e:
    print("ERROR:", type(e).__name__, flush=True)
    print("DETAILS:", repr(e), flush=True)