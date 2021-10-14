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
<<<<<<< HEAD
  main()
=======
  main()


# def find_amount(quantity):
#   if quantity <= 10:
#     amount = 5.00
#   elif quantity > 10 and <= 20:
#     amount = 4.00
#   else:
#     amount = 3.00
#   print(amount)

# def main():
#     quantity = int(input("Enter customer quanity: "))
#     print(quantity)
#     find_amount(quantity)

# if __name__ == "__main__":  
#   main()

  # def amount(quantity):
#   actual_amount = 0 
#   for quantity in 1:
#       if quantity <= 10:
#         amount = 5.00
#       elif quantity > 10 <= 20:
#         amount = 4.00
#       else:
#         amount = 3.00
#     print(quantity, amount)


# # def insertPerson(personName):
#   retval = 0
#   conn = createConnection()
#   with conn.cursor() as cursor:
#     cursor.execute("insert into person (name) values (%s)", (personName)) # personName is substituted for %s.
#     retval = cursor.lastrowid
#     conn.commit()
#   return retval

# def updatePerson(id, name): # Note the order of id and name here doesn't matter.
#   conn = createConnection()
#   with conn.cursor() as cursor:
#     cursor.execute("update person set name = %s where id = %s;", (name, id)) # name, and id is substituted name and id, the order of name and id matters here.
#     conn.commit()

# def insertDemo(firstName, lastName):
#   retval = 0
#   conn = createConnection()
#   with conn.cursor() as cursor:
#     cursor.execute("insert into demo (firstname, lastname) values (%s, %s)", (firstName, lastName))
#     retval = cursor.lastrowid
#     conn.commit()
#   return retval

# #Gets all the infomation in DB
#     dictCustomer = getCustomer()
#     custIDList = []
#     quantList = []
#     userList = []
#         #Looping through to put data in correct list
#     for x in dictCustomer:
#         quantList.append( x['quantity'])
#         userList.append( x['username'])
#         custIDList.append( x['customerID'])
#     print(custIDList)
#     print(userList) 
#     print(quantList)  
# #Connection to DB and pulling all data from customer table   
# def getCustomer():
#     retval = []
#     conn = createConnection()
#     # Querying...
#     with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#         cursor.execute('select * from Customer')
#     conn.commit()
#     retval = cursor.fetchall()
#     return retval


# import boto3
# from botocore.exceptions import ClientError

# def upload():
#   print('*** Uploading file to S3 ***')
#   s3_client = boto3.client('s3')
#   file = 'myfile.txt'
#   bucketName = 'siua-bucket'
#   objectName = 'kristi/myfile.txt'
#   try:
#     response = s3_client.upload_file(file, bucketName, objectName)
#     print(response) # No news is good news.
#   except ClientError as e:
#     print(e)

# def download():
#   print('*** Downloading file from S3 ***')
#   BUCKET_NAME = 'siua-bucket' # replace with your bucket name
#   KEY = 'kristi/myfile.txt' # replace with your object key
  
#   s3 = boto3.resource('s3')
#   s3.Bucket(BUCKET_NAME).download_file(KEY, 'downloaded.txt') #blocking call 

# def delete():
#   print('*** Deleting file from S3 ***')
#   s3 = boto3.resource('s3')
#   s3.Object('siua-bucket', 'kristi/myfile.txt').delete()
    
# def main():
#   # upload()
#   #download()
#   delete()
  
# if __name__ == "__main__":  
#     main()


#   lines = f.readlines()
#         for line in lines:
#             if "PID" in line: 
#                 pidLines.append(line)
#         for line in pidLines:
#             newList = line.split('|')
#             name = newList[5].lower()
#             nameList = name.split('^')
#             formattedName = nameList[1] + ' ' + nameList[0]
#             ssNum = newList[19]
#             if patientDict[ssNum].lower() == formattedName:
#                 print(f"{ssNum} {formattedName.upper()}: OK")
#             else:
#                 print(f"{ssNum} {formattedName.upper()}: No Match!!!")
>>>>>>> 58361bc032a53624e073ea974d37f2ae26ed4c95
