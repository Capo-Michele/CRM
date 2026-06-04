from flask import Flask, render_template, Blueprint, request
from app.models import Client
from flask_login import current_user, login_required
from sqlalchemy import func
from app.extensions import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():

    total_deals = Client.query.filter_by(user_id=current_user.id).count()
    active_deals = Client.query.filter_by(user_id=current_user.id, is_active=True).count()
    inactive_deals = Client.query.filter_by(user_id=current_user.id, is_active=False).count()
    won_deals = Client.query.filter_by(user_id=current_user.id, stage="Won").count()
    revenue_rub = db.session.query(func.sum(Client.deal_price)).filter_by(user_id=current_user.id, currency='RUB', stage='Won').scalar() or 0 
    revenue_byn = db.session.query(func.sum(Client.deal_price)).filter_by(user_id=current_user.id, currency='BYN', stage='Won').scalar() or 0
    revenue_eur = db.session.query(func.sum(Client.deal_price)).filter_by(user_id=current_user.id, currency='EUR', stage='Won').scalar() or 0
    revenue_usd = db.session.query(func.sum(Client.deal_price)).filter_by(user_id=current_user.id, currency='USD', stage='Won').scalar() or 0
    revenue_cny = db.session.query(func.sum(Client.deal_price)).filter_by(user_id=current_user.id, currency='CNY', stage='Won').scalar() or 0

    return render_template('main.html', total_deals=total_deals, won_deals=won_deals, active_deals=active_deals, inactive_deals=inactive_deals, 
                           revenue_rub=revenue_rub,
                           revenue_byn=revenue_byn,
                           revenue_eur=revenue_eur,
                           revenue_usd=revenue_usd,
                           revenue_cny=revenue_cny)