# Install and Import Dependencies 
import pymysql 
import boto3
from botocore.exceptions import ClientError
from time import sleep
from datetime import datetime


def createConnection():
    """ Establishes connection to Amazon Aurora """
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

def getCustomer():
    """ A function that uses a cursor to retrieve selected data from Amazon Aurora """
    retval = []
    conn = createConnection()
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('select customerID, username,  sum(quantity) as quantity from Customer group by username order by customerID asc;')
        conn.commit()
        retval = cursor.fetchall()
    return retval

def amountBillable(quantList, amountList): 
    """ Uses a FOR LOOP with IF/ELIF/ELSE to determine the appropriate price based on quantity """
    for x in quantList:
        if x >= 1 and x <= 10:
            amountList.append(x * 5)
        elif x >= 11 and x <= 20:
            amountList.append(x * 4)
        else:
            amountList.append(x * 3)
    
def writeFile(custIDList, quantList, userList, amountList):
    """ A function that uses a FOR LOOP to iterate through each variable list and write data to a text file """
    with open("billable_customers.txt", "w") as f:
        for x in range(len(custIDList)):
            custIDList[x] = str(custIDList[x])
            f.write(f"{custIDList[x].rjust(10,'0')}\t" )
            f.write(f"{userList[x]}\t")
            f.write(f"{str(quantList[x])}\t")
            amountList[x] = "${:,.2f}". format(amountList[x])
            f.write(f"{str(amountList[x])}\t\n")

def upload():
    """ Uploads the written text file 'billable_customer.txt' to S3 """
    print('*** Uploading file to S3 ***')
    s3_client = boto3.client('s3')
    file = 'billable_customers.txt'
    bucketName = 'siua-bucket'
    objectName = 'TeamBees/billable_customers.txt'
    try:
        response = s3_client.upload_file(file, bucketName, objectName)
        print(response)
    except ClientError as e:
        print(e)


def main():

    customerList = getCustomer()
    """ Calls the getCustomer function to retrieve the selected data from Amazon Aurora """
    custIDList = []
    quantList = []
    userList = []
    amountList = []

    # Uses a FOR LOOP to iterate through each data set and append to the correct variable list
    for x in customerList:
        quantList.append( x['quantity'])
        userList.append( x['username'])
        custIDList.append( x['customerID'])

    # A function that takes in two parameters, quantList and amountList, to calculate final billing amount
    amountBillable(quantList, amountList)

    # A function that takes in four parmeters, custIDList, quantList, userList, and amountList to write data to a text file
    writeFile(custIDList, quantList, userList, amountList)

    # Uploads the 'billable_customer.txt' file to S3 inside of the TeamBees folder
    upload()

    # A forever process that meets stretch goal documentation requirements
    INTERVAL_SECONDS = 60 
    print("To exit press ctrl + c")
    while True:
        timestamp = datetime.today().strftime('%m/%d/%Y %I:%M:%S %p')
        print(f'Last run: {timestamp}.')
        sleep(INTERVAL_SECONDS)


if __name__ == "__main__":  
    main()