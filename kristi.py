# Billing Engine Module (BEM) and S3
import pymysql # <== need to install dependencies: pip install pymysql
import boto3
from botocore.exceptions import ClientError
from time import sleep
from datetime import datetime

# Initial connection to mySQL workbench DB
def createConnection():
  retval = None  
  USER = 'sia-db-user'
  HOST = 'sia-db-cluster-instance-1.cosgu9wr5iwp.us-east-1.rds.amazonaws.com'
  PWD = 'testtest'
  DB = 'TeamB' #Our teams DB with our table
  retval = pymysql.connect(
    user = USER,
    host = HOST,
    password = PWD,
    database = DB)
  return retval

# Created a query to pull all the data from DB
# The values get stored in a tuple
def getCustomer():
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select customerID, username,  sum(quantity) as quantity from Customer group by username order by customerID asc;')
    conn.commit()
    retval = cursor.fetchall()
  return retval

# Getting all the quantity from list and determining which price range
# 1-10 =$5.00, 11-20 = $4.00, >20 = $3.00
# Added all the values to a seperate list
def amountBillable(quantList, amountList): 
   for x in quantList:
     if x >= 1 and x <= 10:
       amountList.append(x * 5)
     elif x >= 11 and x <= 20:
       amountList.append(x * 4)
     else:
       amountList.append(x * 3)
  
# Using all our lists, we make a new txt file
# For Loop to  iterate throw all lists
def writeFile(custIDList, quantList, userList, amountList):
 with open("billable_customers. iterate throughxt", "w") as f:
  for x in range(len(custIDList)):
    # print(custIDList[x],quantList[x])
      custIDList[x] = str(custIDList[x])
      f.write(f"{custIDList[x].rjust(10,'0')}\t" )
      f.write(f"{userList[x]}\t")
      f.write(f"{str(quantList[x])}\t")
      amountList[x] = "${:,.2f}". format(amountList[x])
      f.write(f"{str(amountList[x])}\t\n")

#Uploading the billable_customer.txt to S3
def upload():
  print('*** Uploading file to S3 ***')
  s3_client = boto3.client('s3')
  file = 'billable_customers.txt'
  bucketName = 'siua-bucket'
  objectName = 'TeamBees/billable_customers.txt'
  try:
    response = s3_client.upload_file(file, bucketName, objectName)
    print(response) # No news is good news.
  except ClientError as e:
    print(e)

def main():
  #Uses a select statement to pull all DB info into a tuple 
  customerList = getCustomer()
  custIDList = []
  quantList = []
  userList = []
  amountList = []
  #Looping through to put data in correct list
  for x in customerList:
    quantList.append( x['quantity'])
    userList.append( x['username'])
    custIDList.append( x['customerID'])

  #Calculate amount billable with quantity
  amountBillable(quantList, amountList)

  #Writes the data to an S3 file in the correct format
  writeFile(custIDList, quantList, userList, amountList)

  #Uploads the file to S3 inside of the TeamBees Folder
  upload()


  INTERVAL_SECONDS = 60 # Number of seconds to sleep.
  print("To exit press ctrl + c")
  while True:
    timestamp = datetime.today().strftime('%m/%d/%Y %I:%M:%S %p')
    print(f'Last run: {timestamp}.')
    sleep(INTERVAL_SECONDS)


if __name__ == "__main__":  
  main()