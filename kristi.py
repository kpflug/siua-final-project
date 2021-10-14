# Billing Engine Module (BEM) and S3

import pymysql # <== need to install dependencies: pip install pymysql
import boto3
from botocore.exceptions import ClientError

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

def getCustomer():
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select * from Customer')
    conn.commit()
    retval = cursor.fetchall()
  return retval

def amountBillable(quantList, amountList): 
   for x in quantList:
     if x >= 1 and x <= 10:
       x = x*5
       amountList.append(x)
     elif x >= 11 and x <= 20:
       x = x*4
       amountList.append(x)
     else:
       x = x*3
       amountList.append(x)
   print(amountList)


def writeFile(custIDList, quantList, userList, amountList):
 with open("billable_customers.txt", "w") as f:
  for x in range(len(custIDList)):
    # print(custIDList[x],quantList[x])
    custIDList[x] = str(custIDList[x])
    f.write(custIDList[x].rjust(10,'0'))
    f.write(' ')
    f.write(userList[x])
    f.write(' ')
    f.write(str(quantList[x]))
    f.write(' ')
    amountList[x] = "${:,.2f}". format(amountList[x])
    f.write(str(amountList[x]))
    f.write("\n")

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

  #Gets all the infomation in DB
  dictCustomer = customerList
  custIDList = []
  quantList = []
  userList = []
  amountList = []

  #Looping through to put data in correct list
  for x in dictCustomer:
    quantList.append( x['quantity'])
    userList.append( x['username'])
    custIDList.append( x['customerID'])
  print(custIDList)
  print(userList) 
  print(quantList) 
  amountBillable(quantList, amountList)

  writeFile(custIDList, quantList, userList, amountList)
  upload()

if __name__ == "__main__":  
  main()