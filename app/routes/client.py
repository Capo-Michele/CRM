from flask import Flask, render_template, Blueprint, request, redirect
from app.extensions import db
from app.models import Client

bp = Blueprint('client_page', __name__)

@bp.route('/client', methods=["GET", "POST"])
def client():
    if request.method == "POST":
        deal_name = request.form.get('deal_name')
        client_name =request.form.get('client_name')
        contacts = request.form.get('contacts')
        deal_price = request.form.get('deal_price')
        if not deal_price:
            deal_price = 0
        currency = request.form.get('currency')
        stage = request.form.get('stage')
        deadline = request.form.get('deadline')
        client_info = Client (deal_name=deal_name, client_name=client_name,contacts=contacts, deal_price=deal_price, currency=currency, stage=stage,deadline=deadline)
        db.session.add(client_info)
        db.session.commit()
    
    active_clients =  Client.query.filter(Client.is_active == True).all()
    inactive_clients =  Client.query.filter(Client.is_active == False).all()
    return render_template ('clients.html', active_clients=active_clients, inactive_clients=inactive_clients)


@bp.route('/client/deactivate/<id>', methods=["POST"])
def client_deactivate(id):
    
    client = Client.query.filter_by(id=id).first()
    client.is_active = False
    db.session.commit()

    return redirect ('/client')


@bp.route('/client/activate/<id>', methods=["POST"])
def client_activate(id):
    
    client = Client.query.filter_by(id=id).first()
    client.is_active = True
    db.session.commit()

    return redirect ('/client')


@bp.route('/client/delete/<id>', methods=["POST"])
def client_del(id):
    
    client = Client.query.filter_by(id=id).first()
    db.session.delete(client)
    db.session.commit()

    return redirect ('/client')
    

# @bp.route('/client/edit/<id>', methods=["POST", "GET"])
# def edit(id):
#     client = Client.query.filter_by(id=id).first()
#     if request.method == "POST":
        
#         client.deal_name = request.form.get('deal_name')
#         client.client_name =request.form.get('client_name')
#         client.contacts = request.form.get('contacts')
#         client.deal_price = request.form.get('deal_price')
#         if not client.deal_price:
#             client.deal_price = 0
#         client.currency = request.form.get('currency')
#         client.stage = request.form.get('stage')
#         client.deadline = request.form.get('deadline')
#         db.session.commit()
#         return redirect('/client')

   
    return render_template ("client_edit.html", client=client)
    

@bp.route('/client/search', methods=["GET", "POST"])
def client_search():
    if request.method == "POST":
        client_search
    
    active_clients =  Client.query.filter(Client.is_active == True).all()
    inactive_clients =  Client.query.filter(Client.is_active == False).all()
    return render_template ('clients.html', active_clients=active_clients, inactive_clients=inactive_clients)
        

        


