import csv

def login_check(username, password):

    '''CHECKS WHETHER LOGIN CREDENTIALS ARE CORRECT'''
    
    with open('login.csv', 'r', newline = '') as f:
        reader = csv.reader(f)
        for content in reader:
            if content[1] == username and content[2] == password:
                return True

