import csv

def login_check(username, password):
    with open('login.csv', 'r', newline = '') as f:
        reader = csv.reader(f)
        for content in reader:
            if content[1] == username and content[2] == password:
                return True

# for x in range(5):
#     username = input('username:')
#     password = input('password:')

#     valid = login_check(username, password)
#     if valid:
#         print('Login successful!')
#     else:
#         print('Login ID or password is incorrect.')

        
