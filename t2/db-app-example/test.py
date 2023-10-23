import psycopg2

# Define a function to initialize the database connection
def init_db():
    try:
        connection = psycopg2.connect(
            dbname='init',
            user='postgres',
            password='postgres',
            host='81',
            port="81"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

def serve():
    # Initialize the database connection
    conn = init_db()
    
    if conn:
        try:
            # Create a cursor
            cursor = conn.cursor()
            
            # Execute a SELECT query
            cursor.execute('SELECT * FROM items')
            
            # Fetch the results
            items = cursor.fetchall()
            
            # Print the results
            print(items)
            
        except (Exception, psycopg2.Error) as error:
            print(f"Error while executing SQL: {error}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()
    else:
        print("Unable to connect to the database.")

if __name__ == '__main__':
    serve()
