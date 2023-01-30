from app.models import User, Traducteur, Dashbord, Marketing, Pub
from app import scheduler


# @scheduler.task('interval', id='timed_job', minutes=1)
# def timed_job():
#     print('This job is run every three minutes.')

@scheduler.task('cron', id='scheduled_job', week='*', day_of_week='mon-sun', hour=0)
def scheduled_job():
    # Abonnement annuel des traducteur
    traducteurs = Traducteur.query.filter_by(compte_valid=True).all()
    for traducteur in traducteurs:
        traducteur.has_valid_abon()
    
    # Abonnement Marketing
    accounts = Marketing.query.filter_by(compte_valid=True).all()
    for account in accounts:
        account.has_valid_abon()
        
    # Abonnement des client
    clients = User.query.filter((User.offre_statut=='standard') | (User.offre_statut=='premium')).all()
    for client in clients:
        client.has_valid_abon()
    
    this_month = Dashbord.query.filter_by(id=1).first()
    this_month.end_valid_month()

scheduler.start()
