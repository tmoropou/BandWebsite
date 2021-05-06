"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user_password

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():
    ## TODO: Show to each logged in user the birds they have seen with their count.
    # The table must have an edit button to edit a row, and also, a +1 button to increase the count
    # by 1 (this needs to be protected by a signed URL).
    # On top of the table there is a button to insert a new bird.

    db.account.update_or_insert(user_email=get_user_email(),
                                user_password=get_user_password())

    return dict()

@action('admin')
@action.uses(db, session, auth.user, 'admin.html')
def index():
    admin = "max.nibler@gmail.com"
    user = get_user_email()
    #send user back to home page if not admin
    if admin != user:
        redirect(URL('index'))
    return dict(
        admin=admin,
        url_signer=url_signer
    )

@action('adminButton')
@action.uses(db, session, auth.user, url_signer.verify())
@action('about')
@action.uses(db, auth, 'about.html')
def about():
    print('admin method')
    redirect(URL('admin'))
    return dict()

@action('merch')
@action.uses(db, auth, 'merch.html')
def about():
    return dict()

# This is an example only, to be used as inspiration for your code to increment the bird count.
# Note that the bird_id parameter ...
@action('capitalize/<bird_id:int>') # the :int means: please convert this to an int.
@action.uses(db, auth.user, url_signer.verify())
# ... has to match the bird_id parameter of the Python function here.
def capitalize(bird_id=None):
    assert bird_id is not None
    bird = db.bird[bird_id]
    db(db.bird.id == bird_id).update(bird_name=bird.bird_name.capitalize())
