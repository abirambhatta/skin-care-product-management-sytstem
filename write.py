from datetime import datetime

def update_products(stock_list):
    """
    Updates the inventory file with the latest stock details.
    
    Args:
        stock_list (dict): Dictionary containing product inventory where:
            - Key: Product ID (int)
            - Value: List of product attributes [name, brand, quantity, cost_price, origin]
            
    Writes:
        Updates 'products.txt' file with current inventory data in CSV format:
        name,brand,quantity,cost_price,origin
    """
    inventory_file = open("products.txt", "w")
    for product_attributes in stock_list.values():
        inventory_file.write(product_attributes[0] + "," + product_attributes[1] + "," + 
                            product_attributes[2] + "," + product_attributes[3] + "," + 
                            product_attributes[4] + "\n")
    inventory_file.close()

def generate_sales_invoice(customer_name, contact_number, purchased_items, bill_amount, delivery_fee):
    """
    Generates a sales invoice for customer purchases.
    
    Args:
        customer_name (str): Name of the customer
        contact_number (str): Customer's phone number
        purchased_items (list): List of purchased items where each item is:
            [name, quantity, unit_price, total_price, free_items]
        bill_amount (float): Subtotal before delivery charges
        delivery_fee (int): Shipping cost (0 if no delivery)
            
    Writes:
        Creates a text file named '{customer_name}{contact_number}.txt' containing:
        - Shop header information
        - Customer details
        - Purchase details (items, quantities, prices)
        - Total amount including delivery
    """
    final_amount = bill_amount + delivery_fee
    purchase_timestamp = datetime.now()
    
    receipt_file = open(customer_name + str(contact_number) + ".txt", "w")
    receipt_file.write("\t \t \t \t Product Shop Bill\n")
    receipt_file.write("\t \t Kalanki, Kathmandu | Phone No: 9811112255\n")
    receipt_file.write("*" * 120 + "\n")
    receipt_file.write("Customer Details:\n")
    receipt_file.write("*" * 120 + "\n")
    receipt_file.write("Name of the Customer: " + customer_name + "\n")
    receipt_file.write("Contact number: " + contact_number + "\n")
    receipt_file.write("Date and time of purchase: " + str(purchase_timestamp) + "\n")
    receipt_file.write("*" * 120 + "\n")
    receipt_file.write("\n")
    receipt_file.write("Purchase Detail:\n")
    receipt_file.write("*" * 120 + "\n")
    receipt_file.write("Item Name \t Quantity \t Free \t Unit Price \t Total\n")
    receipt_file.write("*" * 120 + "\n")
    for purchase_entry in purchased_items:
        receipt_file.write(purchase_entry[0] + "\t\t" + str(purchase_entry[1]) + "\t\t" + 
                          str(purchase_entry[4]) + "\t" + str(purchase_entry[2]) + "\t\tRs" + 
                          str(purchase_entry[3]) + "\n")
    receipt_file.write("*" * 120 + "\n")
    if delivery_fee > 0:
        receipt_file.write("Delivery Charge: Rs" + str(delivery_fee) + "\n")
    receipt_file.write("Total Amount: Rs" + str(final_amount) + "\n")
    receipt_file.close()

def generate_restock_invoice(inventory_data, product_to_restock, restock_quantity, updated_price, supplier_name):
    """
    Generates an invoice for inventory restocking.
    
    Args:
        inventory_data (dict): Current product inventory
        product_to_restock (int): ID of product being restocked
        restock_quantity (int): Number of items added to inventory
        updated_price (str): New cost price (empty string to keep current)
        supplier_name (str): Name of the vendor/supplier
            
    Writes:
        Creates a text file named 'supplier_name.txt' containing:
        - Shop header information
        - Vendor details
        - Restock details (product, quantity, cost)
        - Total restocking cost
    """
    restock_timestamp = datetime.now()
    restocked_item = inventory_data[product_to_restock]
    restock_cost = int(restocked_item[3]) * restock_quantity
    
    restock_file = open(str(supplier_name)+".txt", "w")
    restock_file.write("\t \t \t \t Restock Invoice\n")
    restock_file.write("\t \t kalanki, Kathmandu | Phone No: 9811112255\n")
    restock_file.write("*" * 120 + "\n")
    restock_file.write("Vendor Details:\n")
    restock_file.write("*" * 120 + "\n")
    restock_file.write("Vendor Name: " + supplier_name + "\n")
    restock_file.write("Date and time of restock: " + str(restock_timestamp) + "\n")
    restock_file.write("*" * 120 + "\n\n")
    restock_file.write("Restock Detail:\n")
    restock_file.write("*" * 120 + "\n")
    restock_file.write("Product \t Brand \t Quantity \t Cost Price \t Total\n")
    restock_file.write("*" * 120 + "\n")
    restock_file.write(restocked_item[0] + "\t" + restocked_item[1] + "\t" + 
                      str(restock_quantity) + "\t" + restocked_item[3] + "\t\tRs" + 
                      str(restock_cost) + "\n")
    restock_file.write("*" * 120 + "\n")
    restock_file.write("Total Cost: Rs" + str(restock_cost) + "\n")
    restock_file.close()
