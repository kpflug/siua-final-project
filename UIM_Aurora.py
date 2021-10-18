import pymysql

def main():
    while True:
        try: #Validating Customer ID
           customerID = int(input("Enter your customer ID: "))
        except ValueError:
            print('Enter valid ID number')
            continue
        try:
            username = input("Enter first and last name: ") 
            validate_username(username) #Validation function
        except ValueError:
            print('Enter valid username')
            continue
        try:
            quantity = int(input("Quantity of items: "))
            if quantity > 1000:  # Checks if its an integer or if > 1000
                raise ValueError
        except ValueError:
            print('Enter valid quantity')
            continue
        insertCustomer(customerID, username, quantity)

def validate_username(username):
    ''' Username validation. Checks for empty input, numeric input and spaces'''
    if username.isnumeric() or len(username) < 1 or username.isspace():
        raise ValueError
    if all(x.isalpha() or x.isspace() for x in username):
        pass

def insertCustomer(customerID, username, quantity):
    '''Inserting Customer's input to TEAM-B DB table'''
    retval = 0
    conn = createConnection()
    with conn.cursor() as cursor:
        cursor.execute("insert into Customer (customerID, username, quantity) values (%s,%s,%s)", (customerID, username, quantity))
        retval = cursor.lastrowid
    conn.commit()
    return retval

def createConnection():
    '''Established connection to Amazon Aurora '''
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
