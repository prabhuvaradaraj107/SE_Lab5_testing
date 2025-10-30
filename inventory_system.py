"""
A simple inventory management system module.

This module provides basic functions to add, remove, and track items
in a simple dictionary-based inventory. It also supports loading
from and saving to a JSON file.
"""

import json
import logging

# --- Setup Logging ---
# Configure logging to print to console with a clear format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item, qty):
    """Adds a given quantity of an item to the stock."""

    # --- Type and Value Validation ---
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Item must be a non-empty string.",
                      item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity: %s for item '%s'. "
                      "Quantity must be an integer.", qty, item)
        return
    if qty <= 0:
        logging.warning("Invalid quantity: %s. "
                        "Quantity to add must be positive. No action taken.", qty)
        return

    # --- Logic ---
    stock_data[item] = stock_data.get(item, 0) + qty
    logging.info("Added %s of '%s'. New total: %s",
                 qty, item, stock_data[item])


def remove_item(stock_data, item, qty):
    """Removes a given quantity of an item from the stock."""

    # --- Type and Value Validation ---
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Item must be a non-empty string.",
                      item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity: %s for item '%s'. "
                      "Quantity must be an integer.", qty, item)
        return
    if qty <= 0:
        logging.warning("Invalid quantity: %s. "
                        "Quantity to remove must be positive.", qty)
        return

    # --- Logic with Explicit Checks ---
    if item not in stock_data:
        logging.warning("Attempted to remove non-existent item: '%s'.", item)
        return

    current_qty = stock_data[item]

    if qty > current_qty:
        logging.warning("Attempted to remove %s of '%s', but only %s exist. "
                        "Removing all.", qty, item, current_qty)
        del stock_data[item]
        logging.info("Removed all %s of '%s'.", current_qty, item)
    elif qty == current_qty:
        del stock_data[item]
        logging.info("Removed all %s of '%s'. Stock is now 0.", qty, item)
    else:
        stock_data[item] -= qty
        logging.info("Removed %s of '%s'. New total: %s",
                     qty, item, stock_data[item])


def get_qty(stock_data, item):
    """Safely gets the quantity of an item. Returns 0 if item not found."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.
    Returns a new dictionary, or an empty one on failure.
    """
    stock_data = {}
    try:
        # Use 'with' and specify encoding
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
            if not data:
                # Handle empty file
                logging.warning("File '%s' is empty. Initializing empty inventory.",
                                file)
                stock_data = {}
            else:
                stock_data = json.loads(data)
            logging.info("Successfully loaded data from '%s'.", file)
    except FileNotFoundError:
        logging.warning("File not found: '%s'. Starting with an empty inventory.",
                        file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from '%s'. "
                      "File may be corrupt. Starting with empty inventory.", file)
        stock_data = {}
    except OSError as e:
        # Catch other I/O related errors
        logging.error("An unexpected error occurred while loading data: %s", e)
        stock_data = {}
    return stock_data


def save_data(stock_data, file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    try:
        # Use 'with' and specify encoding
        with open(file, "w", encoding="utf-8") as f:
            # indent=4 makes the JSON file human-readable
            f.write(json.dumps(stock_data, indent=4))
        logging.info("Successfully saved data to '%s'.", file)
    except OSError as e:
        # Catch PermissionError and other I/O errors
        logging.error("An unexpected error occurred while saving data: %s", e)


def print_data(stock_data):
    """Prints a report of the current inventory."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        # .items() is a cleaner way to loop through a dictionary
        for item, qty in stock_data.items():
            print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """Returns a list of items with stock below the threshold."""
    result = []
    for item, qty in stock_data.items():
        # This is now safe because add_item ensures qty is an int
        if qty < threshold:
            result.append(item)
    return result


def main():
    """Main function to run the inventory system demo."""
    # Load data first, in case there's a previous inventory
    # No more global state! 'stock' is managed here.
    stock = load_data()
    print_data(stock)

    # --- Test successful additions ---
    add_item(stock, "apple", 10)
    add_item(stock, "banana", 20)
    add_item(stock, "apple", 5)  # Add more to an existing item

    # --- Test invalid inputs (will be logged and skipped) ---
    add_item(stock, "banana", -2)      # Will log warning, do nothing
    add_item(stock, 123, 10)           # Will log error, do nothing
    add_item(stock, "pear", "ten")     # Will log error, do nothing

    # --- Test removals ---
    remove_item(stock, "apple", 3)
    remove_item(stock, "orange", 1)    # Will log warning (item not found)
    remove_item(stock, "banana", 25)   # Will log warning (over-removal)

    # --- Check final quantities ---
    print("Apple stock:", get_qty(stock, "apple"))
    print("Banana stock:", get_qty(stock, "banana"))  # Should be 0
    print("Orange stock:", get_qty(stock, "orange"))  # Should be 0

    print("Low items (threshold 15):",
          check_low_items(stock, threshold=15))  # Should be ['apple']

    print_data(stock)
    save_data(stock)

    # Removed eval() for security
    print("eval() function was removed for security reasons.")


# Standard Python practice to run main()
if __name__ == "__main__":
    main()