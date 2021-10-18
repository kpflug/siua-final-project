import pymysql

def main():
    #Getting Customer information & Loops untill broken
    while True:
        customerID = input("Enter your customer ID: ")  # Getting customer ID
        # Checks if its an integer 
        try:
            if customerID.isspace():
                raise ValueError
            customerID = int(customerID)
            if customerID <= 0:
                raise ValueError
        except ValueError:
            print('Enter valid number')
            continue

        username = input("Enter first and last name: ") # Getting username from customer
        # If empty or is not alphabetic
        # Error and prompted to try again
        try:
            if username.isnumeric() or len(username) < 1 or username.isspace():
                raise ValueError
            if all(x.isalpha() or x.isspace() for x in username):
                pass
        except ValueError:
            print('Enter only alphabetical letters and spaces')
            continue
            
        quantity = input("Quantity of items: ") # Gettin Quantity
        # Checks if its an integer or if > 1000
        try:
            if quantity.isspace():
                raise ValueError
            quantity = int(quantity)
            if quantity <= 0 or quantity > 1000:
                raise ValueError
        except ValueError:
            print('Enter valid number')
            continue
            
        #Inserting the giving information to online DB
        insertCustomer(customerID, username, quantity)


#Using teamB DB we are inserting customer input to appropriate columns
def insertCustomer(customerID, username, quantity):
    retval = 0
    conn = createConnection()
    with conn.cursor() as cursor:
        cursor.execute("insert into Customer (customerID, username, quantity) values (%s,%s,%s)", (customerID, username, quantity))
        retval = cursor.lastrowid
    conn.commit()
    return retval

#Creating connection to mySQL workbench
def createConnection():
    retval = None  
    USER = 'sia-db-user'
    HOST = 'sia-db-cluster-instance-1.cosgu9wr5iwp.us-east-1.rds.amazonaws.com'
    PWD = 'testtest'
    DB = 'TeamB'
    retval = pymysql.connect(
        user = USER,
        host = HOST,
        password = PWD,
        database = DB)
    return retval

if __name__ == "__main__":
    main()
