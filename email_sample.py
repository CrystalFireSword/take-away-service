from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os
import csv 

def get_order_mail_id(order_id):
    mail_id = ''
    name = ''
    try:
        with open('customer_id.csv', 'r', newline = '') as f:
            reader = csv.reader(f)
            for x in reader:
                if x[0]==order_id:
                    mail_id = x[1]
                    name = x[2]
                    return mail_id, name
    except:
        pass
    return mail_id, name



def send_mail(to_address, status, o_id):
    website = ''
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    smtp.ehlo() 
    smtp.starttls() 
    smtp.login('anikrishofficial@gmail.com', 'fxlk qrka fzpt wwte') 
    msg = MIMEMultipart() 
    msg['Subject'] = f"RISHABH'S ORDER STATUS FOR {o_id}"
    text = f'''Hi! {status}! \n You can track your order on our website using your order id. \n Order ID: {o_id} \n Website Link: {website} \n Thank you! Enjoy your meal!'''
    msg.attach(MIMEText(text))
    ImgFileName = r'C:\Users\aksha\food_delivery\static\rishabhs_pic.png'
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    to = to_address 
    smtp.sendmail(from_addr="anikrishofficial@gmail.com", 
                to_addrs=to, msg=msg.as_string()) 
    smtp.quit()
    print('Mail sent!')
