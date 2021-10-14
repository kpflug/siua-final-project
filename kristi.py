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
def find_amount(quantity):
  if quantity <= 10:
    amount = 5.00
  elif quantity > 10 and <= 20:
    amount = 4.00
  else:
    amount = 3.00
  print(amount)

def main():
    quantity = int(input("Enter customer quanity: "))
    print(quantity)
    find_amount(quantity)

if __name__ == "__main__":  
  main()

  def amount(quantity):
#   actual_amount = 0 
#   for quantity in 1:
#       if quantity <= 10:
#         amount = 5.00
#       elif quantity > 10 <= 20:
#         amount = 4.00
#       else:
#         amount = 3.00
#     print(quantity, amount)
