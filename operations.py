def calculate_transaction(selected_item_id, requested_quantity, inventory_data):
    """
    Calculates transaction details including promotional offers and updates inventory.
    
    Implements the 'buy 3 get 1 free' promotion by:
    - Calculating bonus items (1 free for every 3 purchased)
    - Verifying stock availability
    - Updating inventory if transaction is valid
    - Calculating total cost (excluding free items)

    Args:
        selected_item_id (int): ID of the product being purchased
        requested_quantity (int): Number of items customer wants to buy
        inventory_data (dict): Current inventory data where:
            key (int): Product ID
            value (list): [name, brand, stock, cost_price, origin]

    Returns:
        tuple: Contains four elements:
            - transaction_details (list): [product_name, quantity, unit_price, total_cost, free_items]
            - transaction_cost (float): Total cost for purchased items (excluding free items)
            - bonus_items (int): Number of free items awarded
            - is_invalid (bool): True if transaction cannot be processed (invalid quantity or insufficient stock)
    """
    available_stock = inventory_data[selected_item_id][2]
    bonus_items = requested_quantity // 3
    total_items_to_deduct = requested_quantity + bonus_items
    is_invalid = False
    
    # Initialize variables to prevent errors when returning
    transaction_details = []
    transaction_cost = 0

    # Check if the requested quantity is valid and stock is sufficient
    if requested_quantity <= 0 or total_items_to_deduct > int(available_stock):
        is_invalid = True
    else:
        # Update the inventory stock after the sale
        inventory_data[selected_item_id][2] = str(int(inventory_data[selected_item_id][2]) - total_items_to_deduct)
        
        # Compute the transaction cost (200% markup from cost price)
        product_name = inventory_data[selected_item_id][0]
        selling_price = int(inventory_data[selected_item_id][3]) * 2
        transaction_cost = selling_price * requested_quantity

        # Record the transaction details
        transaction_details = [product_name, requested_quantity, selling_price, transaction_cost, bonus_items]

    return transaction_details, transaction_cost, bonus_items, is_invalid

def restock_product(item_id_to_restock, quantity_to_add, revised_cost, inventory_data):
    """
    Updates inventory by restocking products and optionally updating cost prices.
    
    Args:
        item_id_to_restock (int): ID of product being restocked
        quantity_to_add (int): Number of items to add to inventory
        revised_cost (str): New cost price (empty string to keep current price)
        inventory_data (dict): Current inventory data where:
            key (int): Product ID
            value (list): [name, brand, stock, cost_price, origin]

    Returns:
        dict: Updated inventory data with:
            - Increased stock quantity
            - Updated cost price (if revised_cost provided)
    """
    # Update the inventory by adding new stock for the specified item
    inventory_data[item_id_to_restock][2] = str(int(inventory_data[item_id_to_restock][2]) + quantity_to_add)
    if revised_cost != "":
        inventory_data[item_id_to_restock][3] = revised_cost
    return inventory_data
