import sqlite3
con = sqlite3.connect("/workspaces/Ayudantia-2023-2S/Ayu2/db/maestros2.db")
cur = con.cursor()
#cur.execute("CREATE TABLE masters(id, nombre, inventario, ventas)")
#res = cur.execute("SELECT name FROM sqlite_master WHERE name='masters'")

#cur.execute("""
#   INSERT INTO masters VALUES
#        (3,'pepe', 5, 5)
#""")
#con.commit()

#id_m = input("Enter the 'id' value: ")
#name = input("Enter the 'name' value: ")

#query = f"SELECT nombre FROM masters WHERE id={id_m}"

# Execute the INSERT statement to insert the new record
#ur.execute("""
#INSERT INTO masters(id, nombre, inventario, ventas)
#VALUES (?, ?, ?, ?)
#""", (id_m, name, 0, 0))
#con.commit()

# Commit the transaction to save the changes
#nombre_to_delete = input("Enter the 'name' value to delete: ")

#Execute the DELETE statement to remove records with a matching 'name'
#cur.execute("""
#    DELETE FROM masters
#    WHERE nombre = ?
#    """, (nombre_to_delete,))
#con.commit()

#id_m = input("Enter the 'id' value to update: ")

# Execute the UPDATE statement to set "inventario" to 10 for the specific record
#cur.execute("""
#    UPDATE masters
#    SET inventario = 10
#    WHERE id = ?
#    """, (id_m,))
#con.commit()
# Commit the transaction to save the changes
#con.commit()

#id_to_update = input("Enter the 'id' value to update: ")
#nuevo_ventas = input("Enter the new 'ventas' value: ")

# Execute the UPDATE statement to set "ventas" to the new value for the specific record
#cur.execute("""
#    UPDATE masters
#    SET ventas = ?
#    WHERE id = ?
#    """, (nuevo_ventas, id_to_update))
#con.commit()
# Commit the transaction to save the changes
#con.commit()

res = cur.execute("SELECT id, nombre, inventario, ventas FROM masters")
result = res.fetchall()


for row in result:
    id, name, inventario, ventas = row
    print(f"Id: {id}, Name: {name}, Inventario: {inventario}, Ventas: {ventas}")


