import sqlite3

DB_NAME = "Mini_inventory.db"

# ---------- Database Connection ----------
def connect_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        contact TEXT,
        address TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        supplier_id INTEGER,
        price REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock(
        product_id INTEGER PRIMARY KEY,
        quantity INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS discounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        discount_on_item INTEGER
    )
    """)

    con.commit()
    return con, cur

# ---------- Add Supplier ----------
def add_supplier(name, city, contact, address):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO suppliers(name, city, contact, address) VALUES(?,?,?,?)",
        (name, city, contact, address)
    )
    con.commit()
    con.close()
    print("Supplier added successfully!")

# ---------- Add Product ----------
def add_product(name, supplier_id, price, quantity):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO products(name, supplier_id, price) VALUES(?,?,?)",
        (name, supplier_id, price)
    )
    product_id = cur.lastrowid
    cur.execute(
        "INSERT INTO stock(product_id, quantity) VALUES(?,?)",
        (product_id, quantity)
    )
    con.commit()
    con.close()
    print("Product added successfully!")

# ---------- Update Stock ----------
def update_stock(product_id, quantity):
    if quantity < 0:
        print("Invalid quantity!")
        return

    con, cur = connect_db()
    cur.execute(
        "UPDATE stock SET quantity=? WHERE product_id=?",
        (quantity, product_id)
    )
    con.commit()
    con.close()
    print("Stock updated!")

# ---------- Show Products ----------
def show_products():
    con, cur = connect_db()
    cur.execute("""
    SELECT p.id, p.name, s.name, p.price, st.quantity
    FROM products p
    LEFT JOIN suppliers s ON p.supplier_id = s.id
    LEFT JOIN stock st ON p.id = st.product_id
    """)
    rows = cur.fetchall()
    con.close()

    print("\n--- Product List ---")
    for row in rows:
        print(f"ID:{row[0]} | Product:{row[1]} | Supplier:{row[2]} | Price:{row[3]} | Stock:{row[4]}")
    print("---------------------")

# ---------- Search Product ----------
def search_product(name):
    con, cur = connect_db()
    cur.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
    rows = cur.fetchall()
    con.close()

    print("\nSearch Results:")
    for row in rows:
        print(row)

# ---------- Low Stock Alert ----------
def low_stock_alert():
    con, cur = connect_db()
    cur.execute("""
    SELECT p.name, st.quantity
    FROM stock st
    JOIN products p ON st.product_id = p.id
    WHERE st.quantity < 5
    """)
    rows = cur.fetchall()
    con.close()

    print("\nLow Stock Items:")
    for row in rows:
        print(f"{row[0]} -> {row[1]} left")

# ---------- Add Discount ----------
def add_discount(discount, product_id):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO discounts(discount_on_item, product_id) VALUES(?,?)",
        (discount, product_id)
    )
    con.commit()
    con.close()
    print("Discount added!")

# ---------- Show Discounts ----------
def show_discounts():
    con, cur = connect_db()
    cur.execute("""
    SELECT p.name, d.discount_on_item
    FROM discounts d
    JOIN products p ON d.product_id = p.id
    """)
    rows = cur.fetchall()
    con.close()

    print("\nDiscounts:")
    for row in rows:
        print(f"{row[0]} -> {row[1]}%")

# ---------- Export Report ----------
def export_report():
    con, cur = connect_db()
    cur.execute("""
    SELECT p.id, p.name, p.price, st.quantity
    FROM products p
    JOIN stock st ON p.id = st.product_id
    """)
    rows = cur.fetchall()
    con.close()

    with open("inventory_report.txt", "w") as f:
        for row in rows:
            f.write(str(row) + "\n")

    print("Report exported to inventory_report.txt")

# ---------- Main Menu ----------
def main():
    while True:
        print("""
Mini Inventory Management System
1. Add Supplier
2. Add Product
3. Update Stock
4. Show Products
5. Search Product
6. Low Stock Alert
7. Add Discount
8. Show Discounts
9. Export Report
10. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            add_supplier(
                input("Name: "),
                input("City: "),
                input("Contact: "),
                input("Address: ")
            )

        elif choice == "2":
            add_product(
                input("Product name: "),
                int(input("Supplier ID: ")),
                float(input("Price: ")),
                int(input("Quantity: "))
            )

        elif choice == "3":
            update_stock(
                int(input("Product ID: ")),
                int(input("New quantity: "))
            )

        elif choice == "4":
            show_products()

        elif choice == "5":
            search_product(input("Enter product name: "))

        elif choice == "6":
            low_stock_alert()

        elif choice == "7":
            add_discount(
                int(input("Discount %: ")),
                int(input("Product ID: "))
            )

        elif choice == "8":
            show_discounts()

        elif choice == "9":
            export_report()

        elif choice == "10":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

# ---------- Run ----------
if __name__ == "__main__":
    main()
