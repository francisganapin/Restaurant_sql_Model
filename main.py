from flask import (
    Flask, render_template, request,
    session as flask_session,  # <— rename this import
    redirect, url_for, flash
)

from sqlmodel import select, Session as DbaseSession

from function.model import User, Kitchen_Stock, Menu_List,engine


from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)

bcrypt = Bcrypt(app)


app.secret_key = "sadwq‑dsdw1‑3212‑dsa"




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

            return redirect(url_for('stock_list'))
        else:
            flash('Invalid username or password was Invalid','error')

    return render_template('login.html')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route('/logout')
def logout():
    flask_session.clear()
    return redirect(url_for('login'))


#------------------------------------------------------------------------------------------------------------------------------------------------------------------#


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
        stmt = select(Menu_List)

        
        if request.method == 'POST':
            query_name = request.form.get('query_name')

            print(query_name)

            if query_name:
                stmt = stmt.where(Menu_List.name.ilike(f"%{query_name}%"))

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
    }

    return render_template('menu_list.html',**context)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.route("/stock/list",methods=['GET','POST'])
def stock_list():
    #if user was not login go to login page
    if 'user_id' not in flask_session:
        return redirect(url_for('login'))
    
    #get session user
    username = flask_session.get('username')
    role =   flask_session.get('role')

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
        'total_pages': (total + PER_PAGE - 1) // PER_PAGE
    }

    return render_template('stock_list.html',**context)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)