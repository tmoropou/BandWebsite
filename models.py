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

def get_time():
    return datetime.datetime.utcnow()


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
    Field('user_nickname'),
    Field('user_profile_image'),
    Field('user_admin', 'integer', default=0)
    )

db.commit()
