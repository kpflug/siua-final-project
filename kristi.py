# Billing Engine Module (BEM)
'''
The BEM is written in Python and calculates the amount to bill a customer. When the dollar
amounts for all the customers have been calculated, the BEM saves this information to a text
file located in S3. Customers are aggregated by username preventing duplicate usernames in
the final output file. The BEM runs every 60 seconds until control+c is entered on the
console.

The billing rates for the billing engine are represented in Table 2. If a customer has a total of 5
items their billable amount is: 5 * 5 = $25.00. If a customer has a total of 15 items their billable
amount is: 15 * 4 = $60.00. If a customer has 22 items, their billable amount is:
22 * 3 = $66.00.

Quantity Amount
1-10 $5.00
11-20 $4.00
>20 $3.00
'''

#Variables: customer_id, username, quanity, amount
#three if/then statements to calculuate billing

"""
Overview: Take the customer quantity variable and put it through a loop of if/then statements to match quanity with the correct dollar amount 
"""
import pymysql # <== need to install dependencies: pip install pymysql

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

# def getCustomers(customerId):
#   retval = []
#   conn = createConnection()
#   with conn.cursor(pymysql.cursors.DictCursor) as cursor:
#     cursor.execute('select * from username where id = %s', (customerId)) # personId is substituted for %s.
#     conn.commit()
#     retval = cursor.fetchone()
#   return retval

def getCustomer():
  retval = []
  conn = createConnection()
  with conn.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute('select * from Customer')
    conn.commit()
    retval = cursor.fetchall()
  return retval

def quantityList(customerList):
  print(customerList)

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

def main():
# # Our customer IDs.
#   billableCustomersList = ['123', '456', '789'] # Square brackets indicate a list.

# # Store a file from our customer list into S3.
#   createFileS3(customerList = billableCustomersList, fileHeader = '*** Kristi was here ***', bucketName = 'siua-bucket', keyPath = 'demo/bill_these_customers.txt' )

  #INSERT
  # id = insertDemo('Aggie', 'Cromwell')
  # print(id)

  # id = insertPerson('Billy')
  # print(f"Person Id: {id}.")

  #SELECT
  customerList = getCustomer()
  print(customerList)

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


  


  #append to amount list once the final amounts are totaled 
  # quanityList(usernames)

  # UPDATE
  # updatePerson(1, 'Joey Jr.') # Do the update
  # person = getPerson(1) # Did the update work?
  # print(person)
  pass

if __name__ == "__main__":  
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


