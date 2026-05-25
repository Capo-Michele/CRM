from flask import request, redirect, Blueprint, render_template
from app.extensions import db
from app.models import Client 
from flask_login import login_required, current_user

bp = Blueprint('client_edit', __name__)

@bp.route('/client/edit/<id>', methods=["POST", "GET"])
@login_required
def edit(id):
    client = Client.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        
        client.deal_name = request.form.get('deal_name')
        client.client_name =request.form.get('client_name')
        client.contacts = request.form.get('contacts')
        client.deal_price = request.form.get('deal_price')
        if not client.deal_price:
            client.deal_price = 0
        client.currency = request.form.get('currency')
        client.stage = request.form.get('stage')
        client.deadline = request.form.get('deadline')
        db.session.commit()
        return redirect('/client')
    
    return render_template ("client_edit.html", client=client)