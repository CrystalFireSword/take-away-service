#!/usr/bin/python3

import smtplib
from email.message import EmailMessage
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import mimetypes

def send_mail(to_address, status, o_id, name = ''):
    website = ''
    
    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
    smtp.ehlo() 
    smtp.starttls() 
    smtp.login('anikrishofficial@gmail.com', 'fxlk qrka fzpt wwte') 
    msg = EmailMessage()
    msg['Subject'] = f"RISHABH'S ORDER STATUS FOR {o_id}"
    msg['From'] = 'anikrishofficial@gmail.com' 
    msg['To'] = to_address
    
        
    msg.set_content(f'''
    <!DOCTYPE html>
    <html>
        <body>
                
                <p>Hi {name}! We are from Rishabh's Food Court!<br>
                Your ORDER {status}! <br>
                You can track your order on our website {website}using your order id. <br> 
                Order ID: {o_id}<br>
                Thank you! Enjoy your meal! </p>
                <p><img src="cid:image1"/></p>
        </body>
    </html>
    ''', subtype='html')

    msg.make_mixed()
    fp = open('image2.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    to = to_address 
    smtp.sendmail(from_addr="anikrishofficial@gmail.com", 
                to_addrs=to, msg=msg.as_string()) 
    smtp.quit()
    print('Mail sent!')

