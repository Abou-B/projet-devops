# Please make sure as to have the tabulate module installed in order
# to execute this program.
from tabulate import tabulate
import copy

# Creates a class Shoe for stroing the data of each shoe in stock
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

# returns the costs of the object
    def get_cost(self):
        return self.cost

# retunrs the quatity of the object
    def get_quantity(self):
        return self.quantity

# returns string representation of this class
    def __str__(self):
        return f'''{"-" *50}
ShoeData:
country: {self.country}
code: {self.code}
product: {self.product}
cost: {self.cost}
quantity: {self.quantity}
{"-" *50}
'''
    
# Function to read inventory file, create objects and add to list of shoes
def read_shoes_data():
    while True:
        try:
            with open('inventory.txt', 'r') as f:
                shoe_data = f.readlines()
                for i in range(1, len(shoe_data)):
                    data = shoe_data[i].strip("\n").split(",")
                    # creates our shoe objects
                    inventory = Shoe(
                                    data[0],
                                    data[1],
                                    data[2],
                                    float(data[3]),
                                    int(data[4])
                                    )
                    # adds the newly created object to the shoe_list
                    shoe_list.append(inventory)
                break
        # in the event there is not file, we raise an error.
        except FileNotFoundError as error:
            print("Cannot find the inventory file at this time.")
            print(f"{error}\n")
            break

# Function that captures all data for a shoe and
# adds this new data to both the list and updates the 'inventory.txt' file
def capture_shoes():
    print("Please input data for shoe.\n ")
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product: ")
    while True:
        try:
            cost = float(input("Cost: "))
            break
        # To account for value errors on the int/float inputs
        except ValueError:
            print("Please enter a valid number.\n")
    while True:
        try:
            quantity = int(input("Quantity: "))
            break
        except ValueError:
            print("Please enter a valid number.\n")
    # Creates a new object
    inventory = Shoe(country, code, product, cost, quantity)
    shoe_list.append(inventory)
    # Writes our updated data to the 'inventory.txt' file
    update_file()

# Function to update our 'inventory.txt' file
def update_file():
    with open("inventory.txt", "w") as f:
        # writes all the data from each object to a line
        f.write("Country,Code,Product,Cost,Quantity")
        for i in shoe_list:
            f.write(
                    "\n" + i.country + ","
                    + i.code + ","
                    + i.product + ","
                    + str(i.cost) + ","
                    + str(i.quantity)
                    )

# Function displays all data using the tabulate module for clean layout
def view_all():
    # Creates a new list to extract all object data
    new_list = []
    for i in shoe_list:
        new_format = [
                        i.country,
                        i.code,
                        i.product,
                        i.cost,
                        i.quantity,
                        value_per_item(i)
                    ]
        new_list.append(new_format)
    # Uses the "fancy_grid" option from tabulate presets to display
    # our data, and also formats our floats to 2 decimal points)
    print(tabulate(new_list, headers=headings,
                    tablefmt="fancy_grid", floatfmt=".2f")
                    )

# Function to sort our ojbects via stock quantity and prompt for re-stock
def re_stock():
    # Assigns the value of the first item in the sorted list (lowest)
    # and prints the details using .__str__ method.
    # >> NB! lambda sorted reference at bottom of page <<
    low_stock = sorted(shoe_list, key = lambda x : x.quantity)[0]
    print(f"""
The item with lowest stock is:\n
{low_stock.__str__()}
""")
    # Prompt to update stock or not
    while True:
        update = input("Would you like to add to the quantity of this item?: ")
        if update.lower() == "yes" or update.lower() == "y":
            while True:
                try:
                    stock_addition = int(input("How many items to add: "))
                    for i in shoe_list:
                        # Check if the ojbect code entered matches the given code 
                        # and add value to objects quanity if True.
                        if i.code == low_stock.code:
                            i.quantity += stock_addition
                            update_file()
                    break
                except ValueError as error:
                    print("pleaser enter a valid number: {error}")
            break
        elif update.lower() == "no" or update.lower() == "n":
            print("\nNo changes made to stock quantity.\n")
            break
        else:
            print("Please enter a valid response (Yes/No)")

# functon returns the object for the code entered, or returns 0 if
# no object is found
def search_shoe(code):
    for i in shoe_list:
        if i.code == code:
            return i
    return 0

# Function returning the cost x the quatity of a given object
def value_per_item(obj):
    return (obj.cost * obj.quantity)

# Function prints the product name with the highest quantity of stock
def highest_qty():
    high_stock = sorted(shoe_list, key = lambda x : x.quantity, reverse=True)[0]
    print(f"{high_stock.product} should be put on sale!")

# Creates an empty list, populated by 'inventory.txt' and user input
shoe_list = []
# Creates a list in which our headings are stored
headings = ["Country","Code","Product","Cost","Quantity","Value"]
# Reads 'inventory.txt.' file and builds list
read_shoes_data()

# Starts infinite menu loop
while True:
    choice = input("""
What action would you like to take:

1) Find lowest stock item
2) Display all data for shoes
3) Search for product data by code
4) Calculate value on item
5) Highest quantity item to mark for sale
6) Add item to stocklist
7) Exit

Please enter your choice (1-7):""")

    if choice == "1":
        # Displays lowest qty and option for restock
        re_stock()
    elif choice == "2":
        # Displays all shoe data
        view_all()
    elif choice == "3":
        # Displays the object data for the reference 'code' entered
        code = input("Please enter code for search: ")
        if search_shoe(code) == 0:
            print("\nItem not found!")
        else:
            print(search_shoe(code).__str__())
    elif choice == "4":
        # Displays the result of the value function for object
        code = input("Please enter code for search: ")
        if search_shoe(code) == 0:
            print("\nItem not found!")
        else:
            print(search_shoe(code).__str__())
            print(f">>> Value of item: {value_per_item(search_shoe(code))} <<<")
    elif choice == "5":
        # Prints which object has the highest quantity and suggests sale
        highest_qty()
    elif choice == "6":
        # Asks user to input new shoe data and stores it
        capture_shoes()
    elif choice == "7":
        exit()
    else:
        print("please enter a valid choice")


##              >> Below is a website where I found a <<
##      clear explanation of sorting using a key and lambda
##
## Narula, Manav. "Sort With Lambda In Python". Delft Stack, 2022,
## https://www.delftstack.com/howto/python/lambda-functions-in-sort/.
## Accessed 11 Aug 2022.
