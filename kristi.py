import pymysql # <== need to install dependencies: pip install pymysql
import boto3
from botocore.exceptions import ClientError
from time import sleep
from datetime import datetime

def createConnection():
  retval = None  
  USER = 'sia-db-user'
@@ -18,36 +21,32 @@ def getCustomer():
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select * from Customer')
    cursor.execute('select customerID, username,  sum(quantity) as quantity from Customer group by username order by customerID asc;')
    conn.commit()
    retval = cursor.fetchall()
  return retval

def amountBillable(quantList, amountList): 
   for x in quantList:
     if x >= 1 and x <= 10:
       x = x*5
       amountList.append(x)
       amountList.append(x * 5)
     elif x >= 11 and x <= 20:
       x = x*4
       amountList.append(x)
       amountList.append(x * 4)
     else:
       x = x*3
       amountList.append(x)
   print(amountList)
       amountList.append(x * 3)


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
      custIDList[x] = str(custIDList[x])
      f.write(f"{custIDList[x].rjust(10,'0')}\t" )
      f.write(f"{userList[x]}\t")
      f.write(f"{str(quantList[x])}\t")
      amountList[x] = "${:,.2f}". format(amountList[x])
      f.write(f"{str(amountList[x])}\t\n")

def upload():
  print('*** Uploading file to S3 ***')
  s3_client = boto3.client('s3')
@@ -59,6 +58,8 @@ def upload():
    print(response) # No news is good news.
  except ClientError as e:
    print(e)


def main():
  #Uses a select statement to pull all DB info into a tuple 
  customerList = getCustomer()
@@ -73,11 +74,24 @@ def main():
    quantList.append( x['quantity'])
    userList.append( x['username'])
    custIDList.append( x['customerID'])
  print(custIDList)
  print(userList) 
  print(quantList) 

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