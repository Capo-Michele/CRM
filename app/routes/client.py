from flask import render_template, Blueprint, request, redirect
from app.extensions import db
from app.models import Client
from math import ceil
from flask_login import login_required, current_user

bp = Blueprint('client_page', __name__)


@bp.route('/client', methods=["GET", "POST"])
@login_required
def client():
    
    query = Client.query.filter_by(user_id=current_user.id)    
# Добавление пользователя
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
        user_id = current_user.id
        client_info = Client (deal_name=deal_name, client_name=client_name,contacts=contacts, deal_price=deal_price, currency=currency, stage=stage,deadline=deadline, user_id=user_id)
        db.session.add(client_info)
        db.session.commit()
        return redirect('/client')

    # Поисковая строка
    search = request.args.get('search-field')

    if search:
        query = query.filter(Client.client_name.contains(search))
   
        # return render_template ('clients.html', active_clients=active_clients, inactive_clients=inactive_clients)
        
    
    
# Фильтры
    currency_filter = request.args.get('currency_filter')
    dealstage_filter = request.args.get('dealstage_filter')
    if currency_filter:
        query = query.filter(Client.currency == currency_filter)
        
    if dealstage_filter:
        query = query.filter(Client.stage == dealstage_filter)
    
        
    
# Сортировка
    sorting = request.args.get('price_deadline_time_sorting')
    if sorting == "deal_price_sorting_min_max":
        query = query.order_by(Client.deal_price)
    elif sorting == "deal_price_sorting_max_min":
        query = query.order_by((Client.deal_price.desc()))
    elif sorting == "nearest_dedline":
        query = query.order_by(Client.deadline)
    elif sorting == "farthest_dedline":
        query = query.order_by((Client.deadline.desc()))
    elif sorting == "first_created":
        query = query.order_by(Client.date)
    elif sorting == "last_created":
        query = query.order_by((Client.date.desc()))


# Пагинация
    per_page = int(request.args.get('per_page', 5))
    page = int(request.args.get('page', 1))
    active_total = query.filter(Client.is_active == True).count()
    total_pages = ceil(active_total/per_page)

    active_clients = query.filter(Client.is_active == True).offset((page-1)*per_page).limit(per_page).all()
    inactive_clients = query.filter(Client.is_active == False).all()

    return render_template ('clients.html', 
                            active_clients=active_clients, 
                            inactive_clients=inactive_clients, 
                            page=page, 
                            per_page=per_page, 
                            active_total=active_total, 
                            total_pages=total_pages)



@bp.route('/client/deactivate/<id>', methods=["POST"])
@login_required
def client_deactivate(id):
    
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    client.is_active = False
    db.session.commit()

    return redirect ('/client')


@bp.route('/client/activate/<id>', methods=["POST"])
@login_required
def client_activate(id):
    
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    client.is_active = True
    db.session.commit()

    return redirect ('/client')


@bp.route('/client/delete/<id>', methods=["POST"])
@login_required
def client_del(id):
    
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(client)
    db.session.commit()

    return redirect ('/client')


        


