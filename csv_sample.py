import csv
from datetime import date

def get_menu(menu_type = 0):
    ''' RETURNS MENU AS A NESTED LIST '''
    menu = []
    with open('menu.csv', 'r') as f:
        r = csv.reader(f)
        for x in r:
            
            if x[0] != '':
                
                if menu_type == 0:
                    ''' MENU TO BE DISPLAYED TO USER WHILE PLACING ORDER '''    
                    if x[3] == '1':
                        ''' CHECKING AVAILABILITY '''
                        menu.append(x[:3])
                        
                elif menu_type == 1:
                    ''' MENU TO BE DISPLAYED TO ADMIN FOR UPDATION '''
                    menu.append(x[:4])
                
    return menu
menu = get_menu()



def temporary_cart(item_id_list):

    ''' RETURNS THE LIST OF ORDERED ITEMS TO BE TRANSFERRED TO THE CART'''
    menu = get_menu()
    cart_data = []
    item_id_keys = [j for x in item_id_list for j in x]
    for x in menu:
        if x[0] in item_id_keys:
            index_value = item_id_keys.index(x[0])
            # item_id, name, quantity, price
            cart_data.append([x[0], x[1], item_id_list[index_value][x[0]], x[2]])
    if cart_data!=[]:
        return cart_data
    else:
        return -1
    

def write_menu(menu_to_write):

    ''' WRITES ITEMS IN THE MENU AND RELATED INFORMETION INTO THE MENU FILE'''
    
    with open('menu.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        row_to_be_entered = ['Item_no','Item_name','Item_price','Availability']
        rows_to_be_entered = menu_to_write
        writer.writerow(row_to_be_entered)
        writer.writerows(rows_to_be_entered)

def write_customer_data(o_id, e_id, name = ''):

    ''' WRITES CUSTOMER DATA INTO THE FILE '''
    
    with open('customer_id.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([o_id, e_id, name])
