"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from py4web import URL
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


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

### Define the user account table
db.define_table(
    'account',
    Field('user_email', label="E-mail", default=get_user_email()),
    Field('user_password', default=get_user_password()),
    Field('user_first_name', label="First Name", default=get_user_first_name()),
    Field('user_last_name', label="Last Name", default=get_user_last_name()),
    Field('user_username', label="Username"),
    Field('picture'),
    Field('user_admin', 'integer', default=0),
    Field('newsletter', 'integer', default=0),
)

db.account.id.readable = db.account.id.writable = False
db.account.user_password.writable = db.account.user_password.readable = False
db.account.user_admin.writable = db.account.user_admin.readable = False

### Define Current User Table
db.define_table(
    'current_user',
    Field('account_id', 'reference account'),
)

### Define Video Address table
db.define_table(
    'video',
    Field('video_name', requires=IS_NOT_EMPTY()),
    Field('video_url', requires=IS_URL()),
    Field('creation_time', default=get_time),
    Field('front', 'integer', default=0)
)

db.video.creation_time.writable = db.video.creation_time.readable = False
db.video.front.writable = db.video.front.readable = False

### Define Merch Store table
db.define_table(
    'merch',
    Field('item_cost', 'float', default=0.00),
    Field('item_name', 'string', default="Item Name"),
    Field('item_description', 'string'),
    Field('item_stock', 'integer', default=0),
    Field('item_image', 'upload', default='static/merch_images/in_stock/SmallSticker.png'),
    Field('item_type', 'string')
)

db.define_table(
    'shoppingCart',
    Field('user', 'reference account'),
    Field('merch_list', 'list:reference', default=[]),
    Field('item_count', 'integer'),
)

### Define Comments Table
db.define_table(
    'comment',
    Field('message_body'),
    Field('user_email'),
    Field('video_id', 'reference video'),
    Field('username')
)

### Define Merch Reviews Table
db.define_table(
    'review',
    Field('review_body'),
    Field('review_textless', default=True),
    Field('review_score', 'integer', default=5),
    Field('item_id', 'reference merch'),
    Field('user_email'),
    Field('creation_date', default=get_time)
)

db.commit()
