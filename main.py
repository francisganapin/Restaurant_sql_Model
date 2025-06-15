import os
import webbrowser
from datetime import date

from flask import (
    Flask, render_template, request,
    session as flask_session,
    redirect, url_for, flash
)
from flask_bcrypt import Bcrypt

from sqlmodel import select, Session as DbaseSession

from function.model import (User, 
                            Kitchen_Stock, 
                            Menu_List, 
                            Order_List,
                            Income_table,
                            Income_Holder,
                            Income_Today, 
                            engine)

from sqlalchemy.orm import selectinload

from datetime import date

from werkzeug.utils import secure_filename






today = date.today()

app = Flask(__name__)


app.secret_key = "sadwq‑dsdw1‑3212‑dsa"  

bcrypt = Bcrypt(app)



@app.route('/login',methods=['GET','POST'])
def login():
    
    if flask_session.get('user_id'):
        return redirect(url_for('stock_list'))
    
    # get the input
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')

        #check user 
        with DbaseSession(engine) as db:
            statement = select(User).where(User.username == username)
            user = db.exec(statement).one_or_none()

        #verify the password
        if user and bcrypt.check_password_hash(user.password, password):
            flask_session.clear()
            flask_session['user_id']  = user.id
            flask_session['username'] = user.username
            flask_session['role']     = user.role.value
            flask_session['image_ur'] = user.image_url

            return redirect(url_for('menu_list'))
        else:
            flash('Invalid username or password was Invalid','error')

    return render_template('login.html')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    flask_session.clear()
    return redirect(url_for('login'))


#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/you-dont-have-permission/403/')
def restrict_access():
    return render_template('403.html', redirect_to=url_for('menu_list'))




@app.route("/menu/list",methods=['GET','POST'])
def menu_list():

    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

    # get image flder
    image_names = os.listdir('static/images')

    # set the page where we at
    page = request.args.get('page',1,type=int) 
    PER_PAGE = 6


    with DbaseSession(engine) as session:
        if role == 'ADMIN':
            stmt = select(Menu_List)
        elif role  in ['EMPLOYEE','VIEWER']:
            stmt = select(Menu_List).where(Menu_List.is_archive == False)

        
        if request.method == 'POST':
            query_name = request.form.get('query_name')
            query_category = request.form.get('query_category')

            print(query_name)

            if query_name:
                stmt = stmt.where(Menu_List.name.ilike(f"%{query_name}%"))

            if query_category:
                if 'ALL' not in query_category:
                   stmt = stmt.where(Menu_List.category == query_category)


        data = session.exec(stmt).all()
            
   
    total = len(data)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_data = data[start:end]

    
    context = {
        'menu_list': paginated_data,
        'username': username,
        'role': role,
        'page':page,
        'images_name': image_names,
        'total_pages': (total + PER_PAGE - 1) // PER_PAGE,
        'today':today
    }

    return render_template('menu_list.html',**context)



@app.route('/menu/list/archive/<int:id>',methods=['GET','POST'])
def menu_list_archive(id):
        # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
     #avoid to viewer to update this
     
    role = flask_session.get('role')
    if role != 'ADMIN':
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    with DbaseSession(engine) as session:
        stmt = session.get(Menu_List, id)

        if request.method == 'POST':
            try:
               value_archive =  request.form.get('value_archive')
               item_name    =   request.form.get('item_name')
               print(item_name)

               stmt.is_archive = int(value_archive)
               session.commit()

               flash(f'Item  {item_name} was archive  successfully', 'success')
            except Exception as e:
                session.rollback()
                flash('Item archive error.', 'error')

    return redirect(url_for('menu_list'))


@app.route("/menu/list/update/<int:id>",methods=['GET','POST'])
def menu_list_update(id):



    # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))

    #avoid to viewer to update this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    
    with DbaseSession(engine) as session:
        stmt = session.get(Menu_List, id)

        if request.method == 'POST':
            try:
                item_name =  request.form.get('item_name')
                price = request.form.get('item_price')
                quantity = request.form.get('item_quantity')
                print(quantity)

                stmt.price = float(price)
                stmt.quantity = int(quantity)
                
                session.commit()
                flash(f'Item {item_name} was updated successfully', 'success')
            except Exception as e:
                session.rollback()
                flash('Item updated error.', 'error')

    return redirect(url_for('menu_list'))


@app.route("/menu/list/order/<int:id>",methods=['GET','POST'])
def menu_list_order(id):

  
    # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))

    #avoid to viewer to update this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    
    with DbaseSession(engine) as session:
        stmt = session.get(Menu_List, id)


        if request.method == 'POST':
            try:
                item_name =  request.form.get('item_name')
                quantity = int(request.form.get('item_quantity'))
                item_price = float(request.form.get('item_price'))
                table = request.form.get('table_entry')
                print(table)
                print(quantity)


                stmt.quantity = stmt.quantity - quantity
                total_price = item_price * quantity
                # Save order

                #today = date.today()
                #order_date = today.strftime('%Y-%m-%d')  

                stmt2 = Order_List(
                                   menu_id      = id, 
                                   quantity     = quantity,
                                   total        = total_price,
                                   table        = table
                                   #order_date = order_date
                                   )
                
             
               
                session.add(stmt2)
                session.commit()
                
                
                flash(f'Item {item_name} was Order successfully', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Item updated error.{today}', 'error')

    return redirect(url_for('menu_list'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route("/stock/list",methods=['GET','POST'])
def stock_list():


    #if user was not login go to login page
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

    #avoid to viewer to access this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    


    # set the page where we at
    page = request.args.get('page',1,type=int) 

    with DbaseSession(engine) as session:
        
        #get all item does was not archive
        stmt = select(Kitchen_Stock).where(Kitchen_Stock.is_archive == False)
    

        if request.method == 'POST':
            query_name = request.form.get('query_name')
            query_category = request.form.get('query_category')
            print(query_category)
            print(query_name)

            if query_name:
                stmt = stmt.where(Kitchen_Stock.name.ilike(f"%{query_name}%"))
            
            if query_category:
                if 'ALL' not in query_category:
                   stmt = stmt.where(Kitchen_Stock.category == query_category)

        data = session.exec(stmt).all()

    PER_PAGE = 6
    total = len(data)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_data = data[start:end]

    context = {
        'stock_list': paginated_data,
        'username': username,
        'role': role,
        'page': page,
        'total_pages': (total + PER_PAGE - 1) // PER_PAGE,
        'date_condition':today
    }

    return render_template('stock_list.html',**context)



@app.route("/stock/list/update/<int:id>",methods=['GET','POST'])
def stock_list_update(id):



    # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))

    #avoid to viewer to update this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    with DbaseSession(engine) as session:
        stmt = session.get(Kitchen_Stock, id)

        if request.method == 'POST':
            try:
                item_name =  request.form.get('item_name')
                price = request.form.get('item_price')
                quantity = request.form.get('item_quantity')
                print(quantity)

                stmt.price = float(price)
                stmt.quantity = int(quantity)
                
                session.commit()
                flash(f'Item {item_name} was updated successfully', 'success')
            except Exception as e:
                session.rollback()
                flash('Item updated error.', 'error')

    return redirect(url_for('stock_list'))

@app.route('/stock/list/archive/<int:id>',methods=['GET','POST'])
def stock_list_archive(id):
    
        # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
     #avoid to viewer to update this
     
    role = flask_session.get('role')
    if role != 'ADMIN':
        flash('You cannot Edit this','error')
        return redirect(url_for('stock_list'))
    
    with DbaseSession(engine) as session:
        stmt = session.get(Kitchen_Stock, id)

        if request.method == 'POST':
            try:
               value_archive =  request.form.get('value_archive')
               item_name    =   request.form.get('item_name')
               print(item_name)

               stmt.is_archive = int(value_archive)
               session.commit()

               flash(f'Item  {item_name} was archive  successfully', 'success')
            except Exception as e:
                session.rollback()
                flash('Item archive error.', 'error')

    return redirect(url_for('stock_list'))



@app.route('/stock/list/insert/',methods=['GET','POST'])
def stock_list_insert():

    # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
     #avoid to viewer to update this
     
    role = flask_session.get('role')
    if role != 'ADMIN':
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
     

    if request.method == 'POST':
        item_name           =   request.form.get('item_name')
        item_quantity       =   request.form.get('item_quantity')
        item_price          =   request.form.get('item_price')
        item_category       =   request.form.get('item_category')
        item_batch          =   request.form.get('item_batch')
        item_unit           =   request.form.get('item_unit')
        delivery_date       =   request.form.get('item_delivery')
        spoilage_date       =   request.form.get('item_expiry')
        # convert date into date
        delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
        spoilage_date = datetime.strptime(spoilage_date,  '%Y-%m-%d').date()

        try:
            new_item = Kitchen_Stock(
                    quantity        = int(item_quantity),
                    price           = float(item_price ),
                    category        = item_category,
                    batch_code      = item_batch,
                    name            = item_name,
                    unit            = item_unit,
                    delivery_date   = delivery_date,
                    spoilage_date   = spoilage_date,
                    is_archive      = False
                    )
             

            with DbaseSession(engine) as session:
                session.add(new_item)
                session.commit()

                flash(f'Item  {item_name} was added successfully', 'success')

        except Exception as e:

                flash(f'Item {item_name} was Insert error.', 'error')

    return redirect(url_for('stock_list'))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route("/order/list",methods=['GET','POST'])
def order_list():

    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

         
    #avoid to viewer to update this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    with DbaseSession(engine) as session:
        stmt = select(Order_List).options(selectinload(Order_List.menu))
        orders = session.exec(stmt).all()


    context = {
        'username': username,
        'role': role,
        'order_list':orders,
    
        
    }

    return render_template('order_list.html',**context)



@app.route('/order/list/payment', methods=['GET','POST'])
def order_list_payment():

    # avoid who are not login user to update
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
     #avoid to viewer to update this
     
    #avoid to viewer to update this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    

    
    if request.method == 'POST':
        input_table               =   request.form.get('input_table').strip()
        print(input_table)

        input_item_order          =   request.form.get('input_order_list_item','').strip()
        input_payment_type        =   request.form.get('payment_type')
        input_input_income        =   float(request.form.get('input_income'))
        file                      =   request.files.get('input_image_url')


        #when we select input cash image would be cash
        if input_payment_type == 'CASH':
            file_path = 'CASH'

        #save in path
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/payment/',filename)
            file.save(file_path)   

        try:
            new_item = Income_table(
                        order_list_item = input_item_order,
                        payment_type    = input_payment_type,
                        image_url       = file_path,
                        income          = input_input_income
                    )
            
            new_income_holder = Income_Holder(
                    order = new_item
            )

            #this will save our add income by day
            income_now = Income_Today(
                balance = input_input_income
            )

            with DbaseSession(engine) as session:

                stmt = select(Order_List).where(Order_List.table == input_table)
                results = session.exec(stmt)
                table_to_delete = results.all()

                
      
                session.add(new_item)

                session.add(income_now)

                session.add(new_income_holder)
                
                # Delete all matching orders
                for item in table_to_delete:
                    session.delete(item)

                session.commit()
                flash(f'Item Order Payment Success', 'success')
                
        except Exception as e:

                flash(f'Item Order Please Select Payment', 'error')

    return redirect(url_for('order_list'))



#-------------------------------------------------------------------------------------------------------------------#

@app.route("/analytic/list",methods=['GET','POST'])
def analytic_list():

    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #prevent some usier to access this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

    # get image flder
    image_names = os.listdir('static/images')

    # set the page where we at
    page = request.args.get('page',1,type=int) 
    PER_PAGE = 6


    with DbaseSession(engine) as session:
        if role  in ['EMPLOYEE','ADMIN']:

            stmt = select(Income_table)
            data = session.exec(stmt).all()
            
            #this will count all pending order talbe
            stmt2 = select(Order_List).options(selectinload(Order_List.menu))
            orders = session.exec(stmt2).all()

            #print(orders)
            count  = len(set(order.table for order in orders)) # we use this to count only range
            #print(count)
            #this will count all pending order talbe
            stmt3 = session.exec(select(Menu_List).where(Menu_List.quantity == 0)).all()
            out_of_stock = len(stmt3) #this will count out of stock menu

            #this will check the out of stock kitchen stock
            stmt4 = session.exec(select(Kitchen_Stock).where(Kitchen_Stock.quantity == 0)).all()
            out_of_stock_list = len(stmt4)

            stmt5 = session.exec(select(Income_Holder)).all()
            life_time_order = len(stmt5)

            #this wil lget all data that are equal today our income
            stmt6 = select(Income_Today).where(Income_Today.transaction_date == date.today())
            data2 = session.exec(stmt6).all()


        if request.method == 'POST':
            query_date = request.form.get('query_date')

            if query_date:
                stmt = stmt.where(Income_table.order_date.ilike(f"%{query_date}%"))

    




    income_today_holder = []

    for item2 in data2:
        income_today_holder.append(item2.balance)

    income_holder = []

    for item in data:
        print(item.income) 
        income_holder.append(item.income)

    
   
    total = len(data)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_data = data[start:end]

    
    context = {
        'income_today':sum(income_today_holder),
        'total_income': sum(income_holder),
        'income_table': paginated_data,
        'username': username,
        'role': role,
        'page':page,
        'images_name': image_names,
        'total_pages': (total + PER_PAGE - 1) // PER_PAGE,
        'today':today,
        'count':count,
        'out_of_stock':out_of_stock,
        'out_of_stock_list':out_of_stock_list,
        'life_time_order':life_time_order
    }

    return render_template('analytics.html',**context)

@app.route('/analytic/list/payment/<int:_id>',methods=['GET','POST'])
def view_payment_analytic(_id):

    
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #prevent some usier to access this
    role = flask_session.get('role')
    if role not in ['ADMIN', 'EMPLOYEE']:
        flash('You cannot Edit this','error')
        return redirect(url_for('restrict_access'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

    print(role)

    with DbaseSession(engine) as session:
        stmt = select(Income_table).where(Income_table.id == _id)
        results = session.exec(stmt).all()

    context = {
        'image_picture':results,
        'role':role,
        'username':username
    }

    return render_template('analytic_payment_picture.html',**context)


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/menu/list')
    app.run(debug=True)