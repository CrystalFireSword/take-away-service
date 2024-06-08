import csv
from datetime import date

# with open('login.csv', 'w', newline = '') as f:
#     writer = csv.writer(f)
#     row1 = ['userid', 'username', 'password']
#     rows_to_be_entered = ['001', 'XYZ', 'ABC']
#     writer.writerow(row1)
#     writer.writerow(rows_to_be_entered)

def get_menu(menu_type = 0):
    menu = []
    with open('menu.csv', 'r') as f:
        r = csv.reader(f)
        for x in r:
            
            if x[0] != '':
                
                if menu_type == 0:
                    
                    if x[3] == '1':
                        
                        menu.append(x[:3])
                        
                elif menu_type == 1:
                    menu.append(x[:4])
                
    return menu
menu = get_menu()
#print(menu)


def temporary_cart(item_id_list):
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
    '''
    with open('current_cart.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        rows_to_be_entered = cart_data
        writer.writerows(rows_to_be_entered)
    '''

def write_menu(menu_to_write):
    with open('menu.csv', 'w', newline = '') as f:
        writer = csv.writer(f)
        row_to_be_entered = ['Item_no','Item_name','Item_price','Availability']
        rows_to_be_entered = menu_to_write
        writer.writerow(row_to_be_entered)
        writer.writerows(rows_to_be_entered)

def write_customer_data(o_id, e_id, name = ''):
    with open('customer_id.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([o_id, e_id, name])