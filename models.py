"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_password():
    return auth.current_user.get('password') if auth.current_user else None

def get_user_first_name():
    return auth.current_user.get('first_name') if auth.current_user else None

def get_user_last_name():
    return auth.current_user.get('last_name') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

print(auth.current_user.get('id'))

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'bird',
    ### TODO: define the fields that are in the json.
    Field('bird_count', 'integer'),
    Field('seen_by', default=get_user_email()),
)

### Define the user account table
db.define_table(
    'account',
    Field('user_email', default=get_user_email()),
    Field('user_password', default=get_user_password()),
    Field('user_first_name', default=get_user_first_name()),
    Field('user_last_name', default=get_user_last_name()),
    Field('user_username'),
    Field('user_profile_image'),
    Field('user_admin', 'integer', default=0),
    )

db.account.id.readable = db.account.id.writable = False
db.account.user_password.writable = db.account.user_password.readable = False
db.account.user_admin.writable = db.account.user_admin.readable = False

db.commit()
