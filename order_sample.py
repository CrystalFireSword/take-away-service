import csv
from datetime import date
from data_structures import PQueue, WrapperStack
from datetime import datetime
import datetime as date_time
def send_to_cart(form_response):

    ''' SENDS ITEMS FROM THE INITIAL ORDER TO THE CART'''
    
    cart_items = []
    for item_id in form_response:
        
        try:
            if int(form_response[item_id])>0:
                cart_items.append({item_id:form_response[item_id]})
        except:
            continue
    
    return cart_items

def calculate_bill_total(list_to_bill):

    ''' CALCULATES THE TOTAL PRICE OF ORDERED ITEMS '''
    bill_total = 0
    if list_to_bill != [[]]:
        for x in range(len(list_to_bill)):
            quantity = int(list_to_bill[x][2])
            price = int(list_to_bill[x][3])
            list_to_bill[x].append(quantity*price)
            bill_total+=(quantity*price)
    return bill_total, list_to_bill

def make_len(string, length):

    ''' CONVERTS GIVEN STRING TO A STRING OF GIVEN LENGTH BY ADDING ZEROES BEFORE THE STRING '''
    return_string = string
    while len(return_string)<length:
        return_string = '0'+return_string
    return return_string

def find_order_status(order_id, delivered = True):

    ''' FINDS ORDER STATUS BASED ON ORDER ID '''
    current_order_status = -1
    price = []
    items_list = []
    with open('current_orders.csv', 'r', newline = '') as f:
        ''' CHECKS IF ORDER IS LIVE '''
        r = csv.reader(f)
        for x in r:
            try:
                last_order_id = x[0]
                
                if last_order_id==order_id:
                    
                    items_list = x[1]
                    price = x[3]
                    current_order_status = x[5]
                    break
            except:
                continue
    if not delivered:
        return items_list, price, current_order_status
    
    if items_list == []:
        ''' IF ORDER IS NOT LIVE, CHECKS IN DELIVERED ORDERS '''
        with open('delivered_orders.csv', 'r', newline = '') as f:
            r = csv.reader(f)
            for x in r:
                try:
                    last_order_id = x[0]
                    
                    if last_order_id==order_id:
                        
                        items_list = x[1]
                        price = x[3]
                        current_order_status = x[5]
                        break
                except:
                    continue
    if items_list==[]:
        items_list = [[]]
    return items_list, price, current_order_status

def text_order_status(order_status = -1):
    ''' CONVERTS ORDER STATUS, WHICH IS AN INTEGER, TO TEXT '''
    status = 'STATUS: '
    if order_status == -1:
        return status
    elif order_status == 10:
        status += 'Your payment has been confirmed.'
    elif order_status==0:
        status += 'Your payment has not yet been confirmed.'
    elif order_status==1:
        status += 'We just heard your call! We will work on it!'
    elif order_status==2:
        status += "Your order has been picked! We're getting it ready!"
    elif order_status==3:
        status += 'Your order is ready for delivery! Come, pick it up!'
    elif order_status==4:
        status += 'Your order has been delivered! Visit us again!'
    return status


def current_order_list():
    ''' RETURNS LIST OF LIVE ORDERS '''
    orders = []
    with open('current_orders.csv', 'r') as f:
        r = csv.reader(f)
        for x in r:
            try:
                if x[0] != '':
                    orders.append(x[:7])
            except:
                continue
                
    if orders!=[]:
        return orders[1:]
    else:
        return orders

def payment_text(status = '0'):
    ''' RETURNS TEXT FOR PAYMENT CONFIRMATION, USED IN HTML FILE TO DYNAMICALLY CHECK OR UNCHECK AVAILABILITY BOX '''
    if status == '1':
        return 'Payment not confirmed'
    else:
        return 'Payment confirmed!'

def write_current_order(order_list_to_write, write_to_file = 'current_orders.csv', mode = 'w'):
    ''' WRITES LIST OF CURRENT ORDERS TO THE FILE '''
    if write_to_file == 'current_orders.csv':
        if order_list_to_write == []:
            order_list_to_write = [[]]
        with open(write_to_file, 'w', newline = '') as f:
            writer = csv.writer(f)
            row_to_be_entered = ['orderid','order_items','total_items','total_price','payment_status','order_status', 'order_time']
            rows_to_be_entered = order_list_to_write
            writer.writerow(row_to_be_entered)
            writer.writerows(rows_to_be_entered)
    else:
        ''' USE STACK TO PLACE LATEST DELIVERED ORDER AT THE TOP '''
        ''' NOTE: ALTERNATE APPROACH IS TO USE QUEUES BY FIRST ENQUEUEING THE NEW DELIVERIES, THEN ENQUEUEING
        ORDERS FROM THE ORIGINAL FILE, AND FINALLY DEQUEUEING THE ENTIRE QUEUE AND WRITING EACH ORDER TO THE 
        DELIVERED ORDERS FILE. STACKS HAVE BEEN USED HERE TO SHOW HOW LIFO CAN BE USED TO SHOW LATEST DELIVERED ORDERS FIRST.'''
        final_list_to_write = WrapperStack()

        lis_temp = WrapperStack()    # stack that contains already delivered orders from source file
        try:
            with open(write_to_file, 'r', newline='') as f:
                reader = csv.reader(f)
                for x in reader:
                    try:
                        if x[0]!='' and x[0][0]=='D':
                            lis_temp.push(x)
                    except:
                        continue
        except:
            pass

        while not lis_temp.isEmpty():
            final_list_to_write.push(lis_temp.pop())    # adds existing delivered orders to final stack
        for x in order_list_to_write:
            final_list_to_write.push(x)        # adds freshly delivered orders to the final stack

        with open(write_to_file, 'w', newline='') as f:
            writer = csv.writer(f)
            row_to_be_entered = ['orderid','order_items','total_items','total_price','payment_status','order_status', 'order_time', 'delivery_time']
            writer.writerow(row_to_be_entered)
            if not final_list_to_write.isEmpty():
                row_to_be_entered = final_list_to_write.pop()
            while row_to_be_entered!=['orderid','order_items','total_items','total_price','payment_status','order_status', 'order_time', 'delivery_time'] or not final_list_to_write.isEmpty():
                writer.writerow(row_to_be_entered)
                if not final_list_to_write.isEmpty():
                    row_to_be_entered = final_list_to_write.pop()
                else:
                    break
def assign_order_id():

    ''' ASSIGNS ORDER ID TO THE GIVEN ORDER '''
    
    today = date.today()
    date_str = make_len(str(today.day), 2)
    month_str = make_len(str(today.month), 2)
    year_str = str(today.year)
    last_order_id = f'D{date_str}{month_str}{year_str}0000'   #sample format for order id is without underscore
    try:
        with open('orders_ids_generated.csv', 'r', newline = '') as f:
            r = csv.reader(f)
            f.seek(0)
            for x in r:
                
                try:
                    if x[0][0:9]==f'D{date_str}{month_str}{year_str}':
                        last_order_id = x[0]
                        
                except:
                    continue     
    except:
        pass          
    
    if last_order_id[0:9]==f'D{date_str}{month_str}{year_str}':
        current_order_no = int(last_order_id[-4:])+1
        current_order_no_string = make_len(str(current_order_no), 4)
    else:
        current_order_no_string = '0001'    

    current_order_id = f'D{date_str}{month_str}{year_str}O{current_order_no_string}'
    with open('orders_ids_generated.csv', 'a', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([current_order_id])

    return current_order_id


def add_to_orders_pqueue(order_data, price):

    ''' ADDS ORDERS TO THE PRIORITY QUEUE WHICH GIVES PRIORITY BASED ON NUMBER OF ITEMS '''
    
    payment_status = 0
    order_status = 0
    current_order_id = assign_order_id()
    total_items = 0
    order_time = datetime.now()
    
    try:
        order_data = eval(order_data)
    except:
        pass
    
    for x in order_data:
        total_items+= int(x[2])
    orders = PQueue()
    prev_orders = []
    
    with open('current_orders.csv', 'r') as f:
        r = csv.reader(f)
        for x in r:
            try:
                if x[0] != '' and x[0][0]=='D':
                    if x[0][0:9]!=current_order_id[0:9]:
                        print(x)
                        prev_orders.append(x)
                        continue
                    else:
                        if int(x[2])<=3:
                            orders.enqueue(0, x)
                        else:
                            orders.enqueue(1,x)
            except:
                continue
    row_to_be_entered = [current_order_id, order_data, total_items, price, payment_status, order_status, order_time]
    if total_items<=3:
        orders.enqueue(0,row_to_be_entered)
    else:
        orders.enqueue(1, row_to_be_entered)
    with open('current_orders.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        row_to_be_entered = ['orderid','order_items','total_items','total_price','payment_status','order_status', 'order_time']
        writer.writerow(row_to_be_entered)
        while not orders.isEmpty():
            row_to_be_entered = orders.dequeue()
            writer.writerow(row_to_be_entered)
    print(prev_orders)
    if prev_orders!=[]:
         with open('prev_orders.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            row_to_be_entered = ['orderid','order_items','total_items','total_price','payment_status','order_status', 'order_time']
            writer.writerow(row_to_be_entered)
            for x in range(len(prev_orders)):
                writer.writerow(prev_orders[x])
                
    return current_order_id

def delivered_orders_list():

    ''' RETURNS LIST OF DELIVERED ORDERS '''
    orders = []
    with open('delivered_orders.csv', 'r') as f:
        r = csv.reader(f)
        for x in r:
            try:
                if x[0] != '':
                    orders.append(x[:8])
            except:
                continue
    if orders!=[]:
        return orders[1:]
    else:
        return orders
    

def view_order_by_items():

    ''' GIVEN A NESTED LIST OF DATA LIKE ORDER ID, LIST OF ITEMS ORDER WITH THEIR RESPECTIVE 
        QUANTITY AND SO ON, IT RETURNS A NESTED DICTIONARY CONTAINING ITEM NAME AND TOTAL QUANTITY OF THE ITEM
        ACROSS ORDERS '''
    
    items_dict = {}
    with open('current_orders.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for x in reader:
            try:
                if x[0][0]=='D':
                    
                    items_list = eval(x[1])
                    
                    for item in items_list:
                        if item[0] not in items_dict:
                            items_dict[item[0]] = {'Name':'', 'Total Quantity':'', 'Price Per Item':'', 'Total Price':''}
                            items_dict[item[0]]['Name'] = item[1]
                            items_dict[item[0]]['Total Quantity'] = int(item[2])
                            items_dict[item[0]]['Price Per Item'] = int(item[3])
                            items_dict[item[0]]['Total Price'] = int(item[4])
                        else:
                            items_dict[item[0]]['Total Quantity']+=int(item[2])
                            items_dict[item[0]]['Total Price'] += int(item[4])
                    
                else:
                    pass
            except:
                continue
            

    if items_dict=={}:
        return {}
    else:
        return items_dict
