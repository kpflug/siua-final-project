import pymysql


def main():
    #Getting Customer information
    #Loops untill broken
    while True:
        customerID = input("Enter your ID: ")
        username = input("Enter your First and Last name: ")
        quantity = int(input("Quantity of items: "))
        
        #Inserting the giving information to online DB
        insertCustomer(customerID, username, quantity)
        

def insertCustomer(customerID, username, quantity):
    retval = 0
    conn = createConnection()
    with conn.cursor() as cursor:
        cursor.execute("insert into Customer (customerID, username, quantity) values (%s,%s,%s)", (customerID, username, quantity))
        retval = cursor.lastrowid
    conn.commit()
    return retval

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
    