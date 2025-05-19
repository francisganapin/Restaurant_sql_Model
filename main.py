from flask import Flask, render_template, request,redirect,url_for,flash,get_flashed_messages,jsonify
from sqlmodel import Session, select
from model import Kitchen_Stock,Menu_List,engine
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)

@app.route('/json/stock/list')
def json_menu_list():
    try:
        with Session(engine) as session:
            data = session.exec(select(Kitchen_Stock)).all()
            result = [item.model_dump() for item in data]
        return jsonify(result)
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Session invalid id was not exist", "details": str(e)}), 500

@app.route('/json/stock/list/<int:id>', methods=['GET'])
def json_stock_list_id(id):
    try:
        with Session(engine) as session:
            query = select(Kitchen_Stock).where(Kitchen_Stock.id == id)
            data = session.exec(query).all()
            #if item was not found
            if not data:
                return jsonify({'message':f'No item found with ID {id}'})

            result = [item.model_dump() for item in data]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({"error": "Session invalid id was not exist", "details": str(e)}), 500
    

@app.route('/json/menu/list')
def json_stock_list():
    try:
        with Session(engine) as session:
            data = session.exec(select(Menu_List)).all()
            result = [item.model_dump() for item in data]
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": "Session invalid or database issue", "details": str(e)}), 500






@app.route("/menu/list",methods=['GET','POST'])
def menu_list():
    with Session(engine) as session:
        data = session.exec(select(Menu_List)).all()
    
    if request.method == 'POST':
        query_name = request.form.get('query_name')
        #query_category = request.form.get('query_category')
        # print(query_category)
        print(query_name)

        if query_name:
            data = session.exec(select(Menu_List).where(Menu_List.name.ilike(f"%{query_name}%"))).all()
            
        
        #if query_category:
            #if 'ALL' not in query_category:
                #data = session.exec(select(Menu_List).where(Menu_List.category == query_category)).all()


    return render_template('menu_list.html',menu_list=data)



@app.route("/stock/list",methods=['GET','POST'])
def stock_list():
    with Session(engine) as session:
        data = session.exec(select(Kitchen_Stock)).all()
    
    if request.method == 'POST':
        query_name = request.form.get('query_name')
        query_category = request.form.get('query_category')
        print(query_category)
        print(query_name)

        if query_name:
            data = session.exec(select(Kitchen_Stock).where(Kitchen_Stock.name.ilike(f"%{query_name}%"))).all()
            
        
        if query_category:
            if 'ALL' not in query_category:
                data = session.exec(select(Kitchen_Stock).where(Kitchen_Stock.category == query_category)).all()


    return render_template('stock_list.html',stock_list=data)

if __name__ == '__main__':
    app.run(debug=True)