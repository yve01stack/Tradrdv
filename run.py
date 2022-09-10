#! /usr/bin/env python
from app import cli, app, db
from app.models import User, Traducteur, Deal, Contact, Chat, Newsletter
import os

app.secret_key = app.config["SECRET_KEY"]
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Traducteur': Traducteur, 'Deal': Deal, 'Contact': Contact, 'Chat': Chat, 'Newsletter': Newsletter}

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080) 