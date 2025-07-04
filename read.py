def read_products():
    """Reads product data from a file and returns it as a dictionary."""
    product_catalog = {}
    try:
        inventory_file = open("products.txt", "r")
        inventory_lines = inventory_file.readlines()
        item_id = 1
        for entry in inventory_lines:
            entry = entry.replace("\n", "").split(",")
            product_catalog[item_id] = entry
            item_id = item_id + 1
        inventory_file.close()
    except FileNotFoundError:
        print("Error: The file 'products.txt' was not found.")

    return product_catalog
