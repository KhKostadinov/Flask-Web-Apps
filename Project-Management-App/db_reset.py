from dev import app
from lib.models import *

choice = int(input("""
Select action:
    1) clear all tables
    2) create all tables
"""))

if choice == 1:
    with app.app_context():
        db.drop_all()
elif choice == 2:
    with app.app_context():
        db.create_all()
else:
    print("Incorrect selection!")


