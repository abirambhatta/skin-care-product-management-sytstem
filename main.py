from read import read_products
from write import update_products, generate_sales_invoice, generate_restock_invoice
from operations import calculate_transaction, restock_product
from datetime import datetime

# Show initial system greeting
print("\n")
print("\n")
print("\t \t \t \t \t \t \tWeCare Wholesale Center")
print("\t \t \t \t \t\tKumaltar, Kathmandu | Contact: 98435965601")
print("\n")
print("*"*121)
print("\t \t \t \t Access granted to WeCare Admin Console. Start your operations!")
print("*"*121)
print("\n")

# Retrieve product inventory from read.py
product_stock = read_products()

# Core loop for administrative functions
system_active = True
while system_active:
    print("="*95)
    print("id \tname \t\t\t brand \t\t stock \t\tprice \t\t origin")
    print("="*95)

    # Present product inventory in a formatted table
    for stock_id, stock_details in product_stock.items():
        print(str(stock_id) + "\t" + stock_details[0] + "\t\t" + stock_details[1] + "\t" + stock_details[2] + "\t\t" + str(int(stock_details[3])*2) + "\t\t" + stock_details[4])
    print("="*95)
    print("\n")
    print("Choose an operation to manage inventory and sales:")
    print("*"*90)
    print("Select 1 to sell items to a client.")
    print("Select 2 to order stock from a supplier.")
    print("Select 3 to shut down the system.")
    print("\n")

    # Obtain admin's choice with error handling
    while True:
        try:
            admin_choice = int(input("Choose an option to continue: "))
            print("\n")
            break
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")
            print("\n")

    # Process a sale to a customer
    if admin_choice == 1:
        print("-----------------------------------------------------------------------------------------------------------------------------")
        print("Input client details for billing purposes:")
        print("-----------------------------------------------------------------------------------------------------------------------------")
        print("\n")
        buyer_name = input("Enter the client's name: ")
        print("\n")
        buyer_contact = input("Enter the client's phone number: ")
        print("\n")
        print("-----------------------------------------------------------------------------------------------------------------------------")
        print("\n")

        sale_items = []  # Track items sold to the client
        sale_subtotal = 0  # Subtotal before delivery charges
        shipping_charge = 0
        buying_more = True

        while buying_more:
            # Display current inventory
            print("*"*80)
            print("id \t name \t\t brand \t\t qty \t price \t origin")
            print("*"*80)

            for stock_id, stock_details in product_stock.items():
                print(str(stock_id) + "\t", end="")
                for index in range(len(stock_details)):
                    if index == 3:
                        print(str(int(product_stock[stock_id][3])*2) + "\t", end="")
                    else:
                        print(stock_details[index] + "\t", end="")
                print()
            print("*"*80)

            # Request a valid product ID with error handling
            while True:
                try:
                    chosen_item_id = int(input("Enter the ID of the item to sell: "))
                    print("\n")
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    print("\n")

            # Validate the product ID
            while chosen_item_id <= 0 or chosen_item_id > len(product_stock):
                print("That item ID is invalid. Please try again.")
                print("\n")
                try:
                    chosen_item_id = int(input("Enter the ID of the item to sell: "))
                    print("\n")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    print("\n")

            # Request quantity with error handling
            while True:
                try:
                    sale_quantity = int(input("Enter the quantity to sell: "))
                    print("\n")
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    print("\n")

            # Execute transaction calculations
            sale_record, sale_cost, promo_items, stock_error = calculate_transaction(chosen_item_id, sale_quantity, product_stock)

            # Handle stock shortages
            while stock_error:
                print("Insufficient stock for the requested quantity. Check the table and enter a valid amount.")
                print("\n")
                while True:
                    try:
                        sale_quantity = int(input("Enter the quantity to sell: "))
                        print("\n")
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                        print("\n")
                sale_record, sale_cost, promo_items, stock_error = calculate_transaction(chosen_item_id, sale_quantity, product_stock)
            print("\n")

            # Inform client of promotional benefits
            print("Dear " + buyer_name + ", our Buy 3 Get 1 Free deal provides " + str(promo_items) + " free items.")

            # Add items to the sale
            sale_items.append(sale_record)
            sale_subtotal = sale_subtotal + sale_cost

            # Ask if client wants to purchase more
            more_purchase_choice = input("DO you want to continue shoping? (Y/N): ").lower()
            print("\n")
            if more_purchase_choice == "y" or more_purchase_choice == "yes":
                buying_more = True
            else:
                buying_more = False

        # Offer delivery service
        delivery_option = input("Need delivery service? (Y/N): ").upper()
        if delivery_option == "Y" or delivery_option == "YES":
            shipping_charge = 500

        # Calculate total with delivery
        final_bill = sale_subtotal + shipping_charge

        # Output the client's invoice
        print("\t \t \t \t WeCare Sales Receipt ")
        print("\n")
        print("\t \t kalanki, Kathmandu | Contact: 9811112255 ")
        print("\n")
        print("-------------------------------------------------------------------------")
        print("Client Details:")
        print("-------------------------------------------------------------------------")
        print("Client Name: " + buyer_name)
        print("Phone Number: " + buyer_contact)
        print("Purchase Timestamp: " + str(datetime.now()))
        print("-------------------------------------------------------------------------")
        print("\n")
        print("Purchase Summary:")
        print("------------------------------------------------------------------------------------------------------------------")
        print("Item Name \t\t Quantity \t Free \t Unit Price \t Total")
        print("------------------------------------------------------------------------------------------------------------------")
        for purchase_entry in sale_items:
            print(purchase_entry[0] + "\t\t" + str(purchase_entry[1]) + "\t\t" + str(purchase_entry[4]) + "\t" + str(purchase_entry[2]) + "\t\t" + "$" + str(purchase_entry[3]))
        print("------------------------------------------------------------------------------------------------------------------")
        if shipping_charge > 0:
            print("Delivery Charge: Rs" + str(shipping_charge))
        print("Total Amount: Rs" + str(final_bill))
        print("\n")

        # Generate invoice file and update inventory
        generate_sales_invoice(buyer_name, buyer_contact, sale_items, sale_subtotal, shipping_charge)
        update_products(product_stock)

    # Process stock replenishment
    elif admin_choice == 2:
        print("-------------------------------------------------------------------------------------------------------------------------")
        print("You have chosen to replenish inventory.\n")
        print("Current stock levels:\n")

        # Show available items
        for stock_id, stock_details in product_stock.items():
            print(str(stock_id) + ". " + stock_details[0] + " (Quantity: " + stock_details[2] + ", Cost Price: " + stock_details[3] + ")")
        print("\n")

        # Get item ID for restocking with error handling
        while True:
            try:
                restock_item_id = int(input("Enter the ID of the item to restock: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                print("\n")

        if restock_item_id in product_stock:
            # Collect restock information with error handling
            while True:
                try:
                    restock_amount = int(input("Enter quantity to add: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    print("\n")
            updated_cost = input("Enter new cost price (or Enter to retain current): ")
            supplier_name = input("Enter supplier's name: ")
            
            # Perform restock operation
            restock_product(restock_item_id, restock_amount, updated_cost, product_stock)

            # Produce and print restock invoice
            print("\n")
            print("\t \t \t \t WeCare Restock Invoice")
            print("\t \t kalanki, Kathmandu | Contact: 9811112255")
            print("*" * 95)
            print("Vendor Details:")
            print("*" * 95)
            print("Vendor Name: " + supplier_name)
            print("Date and time of restock: " + str(datetime.now()))
            print("*" * 95)
            print("\n")
            print("Restock Details:")
            print("*" * 95)
            print("Product \t Brand \t\tQuantity \tCost Price \t Total")
            print("*" * 95)
            restocked_item = product_stock[restock_item_id]
            restock_cost = int(restocked_item[3]) * restock_amount
            print(restocked_item[0] + "\t" + restocked_item[1] + "\t" + str(restock_amount) + "\t\tRs" + restocked_item[3] + "\t\tRs" + str(restock_cost))
            print("*" * 95)
            print("Total Cost: Rs" + str(restock_cost))
            print("\n")
            
            # Produce restock invoice
            generate_restock_invoice(product_stock, restock_item_id, restock_amount, updated_cost, supplier_name)
            
            # Save updated inventory
            update_products(product_stock)
            print("Stock replenishment completed!\n")
        else:
            print("That item ID is not valid.\n")

    # Terminate the system
    elif admin_choice == 3:
        system_active = False
        print("System closing. Farewell, Admin!")
        print("\n")

    # Address invalid selections
    else:
        print("The option " + str(admin_choice) + " is not recognized. Please try again.")
        print("\n")
