"""Smart Grocery Store Management System
Topics: Lists, dictionaries, loops, conditional statements and custom functions
"""

LOW_STOCK_LIMIT = 5  # products with stock below this number appear in the report


# ---------------------------------------------------------------
# Input helper functions
# ---------------------------------------------------------------

def get_valid_int(prompt, minimum=0):
    # Keep asking until the user enters a whole number that is at least `minimum`
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("  Invalid input. Please enter a whole number.")
            continue

        if number >= minimum:
            return number
        print(f"  Value must be {minimum} or more.")


def get_valid_price(prompt):
    # Keep asking until the user enters a price greater than zero
    while True:
        value = input(prompt).strip()
        try:
            price = float(value)
        except ValueError:
            print("  Invalid input. Please enter a number (for example 250 or 99.5).")
            continue

        if price > 0:
            return price
        print("  Price must be greater than 0.")


def get_valid_text(prompt):
    # Keep asking until a non-empty text is entered, then clean it with strip() and title()
    while True:
        text = input(prompt).strip()
        if text:
            return text.title()
        print("  This field cannot be empty.")


# ---------------------------------------------------------------
# Search helper functions
# ---------------------------------------------------------------

def find_product_by_id(products, product_id):
    # Return the product dictionary with this ID, or None if it does not exist
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def find_products_by_name(products, search_text):
    # Return a list of products whose name contains the search text (not case sensitive)
    matches = []
    for product in products:
        if search_text.lower() in product["name"].lower():
            matches.append(product)
    return matches


# ---------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------

def print_product_table(product_list):
    # Print the given products in a neat table
    line = "-" * 56
    print(line)
    print(f"{'ID':<6}{'Name':<18}{'Category':<14}{'Price':>10}{'Stock':>8}")
    print(line)
    for product in product_list:
        print(f"{product['id']:<6}{product['name']:<18}{product['category']:<14}"
              f"{product['price']:>10.2f}{product['stock']:>8}")
    print(line)


def show_menu():
    # Print the main menu
    print()
    print("=" * 36)
    print("SMART GROCERY STORE SYSTEM")
    print("=" * 36)
    print()
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Search Product")
    print("4. Update Product Stock")
    print("5. Process Customer Sale")
    print("6. View Sales Records")
    print("7. Generate Store Report")
    print("8. Exit")
    print()


# ---------------------------------------------------------------
# Main features
# ---------------------------------------------------------------

def add_product(products):
    # Ask for product details, build a dictionary and append it to the products list
    print("\n--- Add New Product ---")

    # Keep asking until the ID is not already used (prevents duplicates)
    while True:
        product_id = get_valid_int("Enter product ID: ", 1)
        if find_product_by_id(products, product_id) is None:
            break
        print(f"  Product ID {product_id} already exists. Please enter a different ID.")

    name = get_valid_text("Enter product name: ")
    category = get_valid_text("Enter category: ")
    price = get_valid_price("Enter price: ")
    stock = get_valid_int("Enter available stock: ", 0)

    new_product = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
    }
    products.append(new_product)
    print(f"\n  '{name}' was added successfully.")


def view_all_products(products):
    # Display every product, or a message if the store has no products yet
    print("\n--- All Products ---")
    if len(products) == 0:
        print("  No products available.")
        return
    print_product_table(products)


def search_product(products):
    # Search by ID (if the input is digits) or by name, and show the full details
    print("\n--- Search Product ---")
    search_text = input("Enter product name or ID: ").strip()

    if search_text == "":
        print("  Search text cannot be empty.")
        return

    if search_text.isdigit():
        product = find_product_by_id(products, int(search_text))
        results = [product] if product is not None else []
    else:
        results = find_products_by_name(products, search_text)

    if len(results) == 0:
        print(f"  No product found for '{search_text}'.")
    else:
        print(f"\n  {len(results)} product(s) found:")
        print_product_table(results)


def update_stock(products):
    # Add stock to a product or set a new quantity, then show the updated stock
    print("\n--- Update Product Stock ---")
    product_id = get_valid_int("Enter product ID: ", 1)
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  Product with ID {product_id} does not exist.")
        return

    print(f"  {product['name']} currently has {product['stock']} units in stock.")
    print("  1. Add stock")
    print("  2. Set new quantity")

    # Only accept option 1 or 2
    while True:
        option = get_valid_int("Choose an option (1-2): ", 1)
        if option in (1, 2):
            break
        print("  Please choose 1 or 2.")

    if option == 1:
        extra = get_valid_int("Enter quantity to add: ", 1)
        product["stock"] += extra
    else:
        product["stock"] = get_valid_int("Enter new stock quantity: ", 0)

    print(f"\n  Stock updated. {product['name']} now has {product['stock']} units.")


def process_sale(products, sales):
    # Sell a product: check it exists and has enough stock, then update stock and save the sale
    print("\n--- Process Customer Sale ---")
    product_id = get_valid_int("Enter product ID: ", 1)
    product = find_product_by_id(products, product_id)

    if product is None:
        print(f"  Product with ID {product_id} does not exist.")
        return

    if product["stock"] == 0:
        print(f"  Sorry, {product['name']} is out of stock.")
        return

    quantity = get_valid_int("Enter purchase quantity: ", 1)

    # Do not allow the sale if the stock is not enough
    if quantity > product["stock"]:
        print(f"  Sale not allowed. Only {product['stock']} units of {product['name']} are available.")
        return

    total_price = product["price"] * quantity
    product["stock"] -= quantity  # deduct the sold quantity from stock

    # Store the completed sale in the separate sales list
    sale_record = {
        "id": product["id"],
        "name": product["name"],
        "quantity": quantity,
        "total": total_price,
    }
    sales.append(sale_record)

    print("\n  ----- Purchase Summary -----")
    print(f"  Product        : {product['name']}")
    print(f"  Price per unit : {product['price']:.2f}")
    print(f"  Quantity       : {quantity}")
    print(f"  Total amount   : {total_price:.2f}")
    print(f"  Stock left     : {product['stock']}")


def view_sales_records(sales):
    # Display all completed sales
    print("\n--- Sales Records ---")
    if len(sales) == 0:
        print("  No sales have been made yet.")
        return

    line = "-" * 52
    print(line)
    print(f"{'ID':<8}{'Product':<20}{'Quantity':>10}{'Total':>14}")
    print(line)
    for sale in sales:
        print(f"{sale['id']:<8}{sale['name']:<20}{sale['quantity']:>10}{sale['total']:>14.2f}")
    print(line)


def generate_report(products, sales):
    # Calculate and print the final store report
    print("\n" + "=" * 40)
    print(f"{'STORE REPORT':^40}")
    print("=" * 40)

    # Total available stock: add up the stock of every product
    total_stock = 0
    for product in products:
        total_stock += product["stock"]

    # Total revenue: add up the total amount of every sale
    total_revenue = 0
    for sale in sales:
        total_revenue += sale["total"]

    print(f"Total products          : {len(products)}")
    print(f"Total available stock   : {total_stock}")
    print(f"Total sales transactions: {len(sales)}")
    print(f"Total revenue generated : {total_revenue:.2f}")

    # Products whose stock is below the limit
    print(f"\nProducts with stock below {LOW_STOCK_LIMIT} units:")
    low_stock_found = False
    for product in products:
        if product["stock"] < LOW_STOCK_LIMIT:
            print(f"  - {product['name']} (ID {product['id']}): {product['stock']} left")
            low_stock_found = True
    if not low_stock_found:
        print("  None. All products have enough stock.")

    # Highest and lowest priced products (all products are shown if prices are tied)
    if len(products) > 0:
        prices = [product["price"] for product in products]
        highest_price = max(prices)
        lowest_price = min(prices)

        print("\nProduct with the highest price:")
        for product in products:
            if product["price"] == highest_price:
                print(f"  - {product['name']}: {product['price']:.2f}")

        print("\nProduct with the lowest price:")
        for product in products:
            if product["price"] == lowest_price:
                print(f"  - {product['name']}: {product['price']:.2f}")
    else:
        print("\nNo products available for price comparison.")

    print("=" * 40)


# ---------------------------------------------------------------
# Program starts here
# ---------------------------------------------------------------

def main():
    # Starting products (sample data). Delete these lines to begin with an empty store.
    products = [
        {"id": 101, "name": "Milk", "category": "Dairy", "price": 250, "stock": 20},
        {"id": 102, "name": "Bread", "category": "Bakery", "price": 120, "stock": 4},
        {"id": 103, "name": "Rice", "category": "Grains", "price": 350, "stock": 50},
        {"id": 104, "name": "Eggs", "category": "Dairy", "price": 300, "stock": 3},
        {"id": 105, "name": "Sugar", "category": "Grocery", "price": 160, "stock": 30},
    ]
    sales = []  # separate list that stores completed sales

    # The menu keeps running until the user chooses 8 (Exit)
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_product(products)
        elif choice == "2":
            view_all_products(products)
        elif choice == "3":
            search_product(products)
        elif choice == "4":
            update_stock(products)
        elif choice == "5":
            process_sale(products, sales)
        elif choice == "6":
            view_sales_records(sales)
        elif choice == "7":
            generate_report(products, sales)
        elif choice == "8":
            print("\nThank you for using the Smart Grocery Store System. Goodbye!")
            break
        else:
            print("\n  Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()