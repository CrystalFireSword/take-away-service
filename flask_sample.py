from flask import Flask, redirect, url_for, session
from flask import render_template
from flask import request
from login_sample import login_check
from datetime import timedelta
from csv_sample import get_menu, temporary_cart, write_menu, write_customer_data
from order_sample import send_to_cart, calculate_bill_total, delivered_orders_list , find_order_status, text_order_status, current_order_list, payment_text, write_current_order, add_to_orders_pqueue, view_order_by_items
from datetime import datetime
from email_sample import get_order_mail_id
from email_sample_2 import send_mail
app = Flask(__name__)
app.secret_key = 'Thisisthesecretkey'

'''
# For permanent sessions
app.permanent_session_lifetime = timedelta(days=5)
# data can be in days or minutes or anything
'''

@app.route('/')
def home():
    content = ''
    if request.args.get('content'):
        content = request.args.get('content')
    return render_template('index.html', content = content)

@app.route('/order', methods = ['GET', 'POST'])
def order():
    if request.method == 'POST':
        cart_items = send_to_cart(request.form)
        cart_list = temporary_cart(cart_items)
        if cart_list!=-1:
            
            return redirect(url_for('cart', item_list = [cart_list]))
        else:
            return redirect(url_for('cart', item_list = [[]]))
        ### find another way to pass items)list to cart, or render template
        '''
        for x in request.form:
            try:
                if int(request.form[x]):
                    
                    #send_to_cart(x)
            except:
                return redirect(url_for('cart'))
        '''
    return render_template('order.html', item_list = get_menu()[:])

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    if request.method == 'POST':
        cart_items = send_to_cart(request.form)
        cart_list = temporary_cart(cart_items)
        if cart_list!=-1:
            return redirect(url_for('bill', item_list = [cart_list]))
        else:
            return redirect(url_for('cart', item_list = [[]]))
    return render_template('cart.html', item_list = eval(request.args.get('item_list')))

@app.route('/bill', methods = ['GET', 'POST'])
def bill():
    list_to_bill = eval(request.args.get('item_list'))
    print(list_to_bill)
    price, list_after_bill = calculate_bill_total(list_to_bill)
    print(list_to_bill)
    if request.method == 'POST':
        if list_after_bill!=[[]]:
            print(list_to_bill)
            return redirect(url_for('payment', list_to_be_billed=[list_to_bill], price = price))

    return render_template('bill.html', item_list = list_after_bill, total_amount = price)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        # session.permanent = True # for permanent sessions
        user = request.form['EmailId']
        password = request.form['pwd']
        if login_check(user, password):
            session['user'] = user
            return redirect(url_for("user"))
        else:
            return render_template('login.html', content = 'Invalid username or password')
    else:
        if 'user' in session:   # for default login if user if already logged in
            return redirect(url_for('user'))
        return render_template('login.html', content = 'Your username and password are safe with us!')

@app.route("/user", methods = ['GET', 'POST'])
def user():
    if "user" in session:
        user = session['user']
        if request.args.get('content'):
            content = request.args.get('content')
        else:
            content = ''
        if request.method == 'POST':
            button_clicked = request.form['button_clicked']
            if button_clicked == 'view_orders':
                return redirect(url_for('view_orders'))
            if button_clicked == 'update_menu':
                return redirect(url_for('update_menu'))
            if button_clicked == 'delivered_orders':
                return redirect(url_for('delivered_orders'))
            if button_clicked == 'view_by_items':
                return redirect(url_for('view_by_items'))
            if button_clicked == 'logout':
                return redirect(url_for('logout'))
            
        return render_template('admin.html', contents = content)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/track', methods = ['POST', 'GET'])
def track():
    if request.method == 'POST':
        items_list, price, order_status = find_order_status(request.form['order_id'])
        order_status = int(order_status)
        status = 'STATUS:'
        if order_status == -1:
            return render_template('track.html', content = 'Order ID not found')
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
        return redirect(url_for('tracking', order_id = request.form['order_id'], current_status = status, item_list = items_list, total_price = price))
        # 0: order not received, 1: order_received, 2:order_getting_ready, 3:ready, 4:collected
    return render_template('track.html')

@app.route('/tracking')
def tracking():
    try:
        o_id = request.args.get('order_id')
        current_status = request.args.get('current_status')
        items_list = eval(request.args.get('item_list'))
        price = request.args.get('total_price')
    except:
        o_id = None
        current_status = None
        items_list = [[]]
        price = None
        # fix this part of the code in html to carry over order id value
    return render_template('tracking.html', order_id = o_id, status = current_status, item_list = items_list, total_amount = price)

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    
    list_to_bill = request.args.get('list_to_be_billed')
    price = request.args.get('price')
    print(request.args)
    if request.method == 'POST':
         
        email_id = request.form.get('EmailId')
        name = request.form.get('Name')
        if request.form.get('EmailId') == '':
            return render_template('payment.html', total_price = request.args.get('price'), content_to_show = 'Please enter your mail id to continue')
        else:
            order_id = add_to_orders_pqueue(list_to_bill, price)
            write_customer_data(order_id, email_id, name)
            return redirect(url_for('cash', total_price = price, unique_id = order_id, content_to_show = ''))
        
        
    return render_template('payment.html', total_price = request.args.get('price'), content_to_show = '')


@app.route('/cash', methods = ['GET', 'POST'])
def cash():
    price = request.args.get('total_price')
    unique_id = request.args.get('unique_id')
    content_to_show = request.args.get('content_to_show')
    if request.method == 'POST':
        return redirect(url_for('home', content = 'Thank you! You will be notified when your order is ready.' ))
    return render_template('cash.html', total_price = price, unique_id = unique_id, content_to_show = content_to_show)

@app.route('/update_menu', methods = ['GET', 'POST'])
def update_menu():
    if "user" in session:
        if request.method == 'POST':
            item_list = get_menu(1)[1:]
            menu_list_to_write = []
            
            for x in item_list:
                item_final_list = []
                item_final_list.append(x[0])
                if request.form.get(f'Name:{x[0]}'):
                    item_final_list.append(request.form[f'Name:{x[0]}'])
                else:
                    item_final_list.append('')
                if request.form.get(f'Price:{x[0]}'):
                    item_final_list.append(request.form[f'Price:{x[0]}'])
                else:
                    item_final_list.append('')
                
                if request.form.get(f'Availability:{x[0]}'):
                    item_final_list.append(1)
                else:
                    item_final_list.append(0)
                menu_list_to_write.append(item_final_list)
            write_menu(menu_list_to_write)
            return redirect(url_for('user', content = 'Update successful'))
        return render_template('update_menu.html', item_list = get_menu(1)[1:])
    else:
        return redirect(url_for('login'))

@app.route('/view_orders', methods = ['GET', 'POST'])
def view_orders():
    if "user" in session:
        if request.method == 'POST':
            order_list = current_order_list()
            order_list_to_write = []
            delivered_orders = []
            
            for x in order_list:
                order_final_list = []
                order_final_list.extend(x[0:4])
                mail_id, name = get_order_mail_id(x[0])
                if mail_id == '':
                    mail_id = 'akshayalakshmi2310099@ssn.edu.in'
                                    
                if request.form.get(f'Pay:{x[0]}'):
                    order_final_list.append(1)
                else:
                    order_final_list.append(0)
                order_final_list.append(x[5])
                
                if request.form.get(f'OrderDelivered:{x[0]}'):
                    order_final_list[5] = 4
                    status = text_order_status(4)
                    delivery_time = datetime.now()
                    order_final_list.append(x[6])
                    order_final_list.append(delivery_time)
                    delivered_orders.append(order_final_list)
                    send_mail(mail_id, status,x[0], name)
                    continue
                elif request.form.get(f'OrderReady:{x[0]}'):
                    status = text_order_status(3)
                    try:
                        if int(order_final_list[5])!=3:
                            order_final_list[5] = 3
                            send_mail(mail_id, status,x[0], name)
                    except:
                        pass
                elif request.form.get(f'OrderTaken:{x[0]}'):
                    status = text_order_status(2)
                    try:
                        if int(order_final_list[5])!=2:
                            order_final_list[5] = 2
                            send_mail(mail_id, status,x[0], name)
                    except:
                        pass
                    
                elif request.form.get(f'OrderReceived:{x[0]}'):
                    status = text_order_status(1)
                    try:
                        if int(order_final_list[5])!=1:
                            
                            order_final_list[5] = 1
                            send_mail(mail_id, status,x[0], name)
                    except:
                        pass
                    
                elif request.form.get(f'PaymentConfirmed:{x[0]}'):
                    status = text_order_status(10)
                    try:
                        if int(order_final_list[5])!=10:
                            order_final_list[5] = 10
                            send_mail(mail_id, status,x[0], name)
                    except:
                        pass
                    
                
                order_final_list.append(x[6])
                order_list_to_write.append(order_final_list)
            
            write_current_order(delivered_orders, 'delivered_orders.csv')
            write_current_order(order_list_to_write)
            return redirect(url_for('user', content = 'Order Status Updated'))
        order_list = current_order_list()
        return render_template('view_orders.html', order_list = order_list, fun_for_text = text_order_status, payment_text=payment_text)
    else:
        return redirect(url_for('login'))

@app.route('/view_by_items')
def view_by_items():
    if "user" in session:
        return render_template('view_order_by_items.html', item_list = view_order_by_items(), no_total = 1)

@app.route('/order_status/<o_id>')
def order_status(o_id):
    if "user" in session:
        items_list, price, order_status = find_order_status(o_id)
        return render_template('bill.html', item_list = eval(items_list), total_amount = price, no_button = 1, order_id = 'ORDER ID:'+o_id)
    else:
        return redirect(url_for('login'))
        
@app.route('/delivered_orders')
def delivered_orders():
    if "user" in session:
        order_list = delivered_orders_list()
        return render_template('delivered_orders.html', order_list = order_list)
    else:
        return redirect(url_for('login'))


@app.route('/test_dynamic_page')
def dynamic_page():
    return render_template('dyn_con.html', to_display = 'This page is for experimenting and testing')




if __name__ == '__main__':
    app.run()