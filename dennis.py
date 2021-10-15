import pymysql

def main():
    #Getting Customer information
    #Loops untill broken
    while True:
        customerID = input("Enter your ID: ")
        checkInt( customerID)
        username = input("Enter your First and Last name: ")
        checkStr(username)
        quantity = input("Quantity of items: ")
        checkInt(quantity)

        #Inserting the giving information to online DB
        insertCustomer(customerID, username, quantity)

# The following check for user input
# If customerID, Quantity are not a int then you will be prompted to enter again 
# If empty -> Try again      
def checkInt(userInput):
    if len(userInput) == 0 or userInput.isalpha():
        print("Invalid try again")
        main()
# If customer Username is not a string then you will be prompted to enter again  
# If empty -> Try again      
def checkStr(userInput):
    if len(userInput) == 0 or userInput.isdigit():
        print("Invalid try again")
        main()    

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
