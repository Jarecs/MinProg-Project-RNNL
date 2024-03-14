import os
from app import create_app
# from flask_script import Manager
from app import db
from app.models import User
from flask.cli import with_appcontext
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# manager = Manager(app)


@click.command('adduser')
@click.argument('email')
@click.argument('username')
@click.option('--admin', is_flag=True, help='Assigns the user as an admin.')
@with_appcontext
def adduser(email, username, admin=False):
    """Register a new user"""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm password: ')
    if password != password2:
        import sys
        sys.exit('Passwords do not match')
    db.create_all()
    user = User(email=email, username=username, password=password, is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print(f'User {username} was registered successfully!')


app.cli.add_command(adduser)

if __name__ == '__main__':
    app.run()
