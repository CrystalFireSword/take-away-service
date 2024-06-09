import csv 

def get_order_mail_id(order_id):
    
    '''RETRIEVES USER'S MAIL ID AND NAME WHEN GIVEN THEIR ORDER ID '''
    
    mail_id = ''
    name = ''
    try:
        with open('customer_id.csv', 'r', newline = '') as f:
            reader = csv.reader(f)
            for x in reader:
                try:
                    if x[0]==order_id:
                        mail_id = x[1]
                        name = x[2]
                        return mail_id, name
                except:
                    continue
    except:
        pass
    return mail_id, name
