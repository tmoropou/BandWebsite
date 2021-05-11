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
from .models import get_user_email, get_user_password, get_user_first_name, get_user_last_name
from py4web.utils.form import Form, FormStyleBulma

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth, 'index.html')
def index():

    db.account.update_or_insert(user_email=get_user_email(),
                                user_password=get_user_password(),
                                user_first_name=get_user_first_name(),
                                user_last_name=get_user_last_name())

    return dict(url_signer=url_signer)

@action('admin')
@action.uses(db, session, auth.user, 'admin.html')
def admin_index():
    # Gets all admins
    admins = db(db.account.user_admin == 1).select()

    # Checks if user is one of the admins
    userIsAdmin = False
    for admin in admins:
        if admin.user_email == get_user_email():
            userIsAdmin = True
    if userIsAdmin == False:
        redirect(URL('index'))

    # Get all videos
    vidRows = db(db.video.id > 0).select()

    return dict(
        admin=admin,
        url_signer=url_signer,
        vidRows=vidRows
    )

@action('about')
@action.uses(db, auth, 'about.html')
def about():
    return dict()

@action('merch')
@action.uses(db, auth, 'merch.html')
def merch():
    return dict()

@action('video')
@action.uses(db, auth, 'video.html')
def video():
    frontVideo = db(db.video.front==1).select().first()
    if frontVideo == None:
        print("Error: no video flagged for front in DB")
        redirect(URL('index'))
    else:
        videoURL = frontVideo.video_url
    # food = "https://www.youtube.com/embed/qEkmd1IXq-Y"
    # overview = "https://www.youtube.com/embed/2nfYTyUnfM0"
    return dict(thevideo=videoURL)

@action('add_video', method=['GET', 'POST'])
@action.uses(db, session, auth.user, 'add_video.html')
def add_video():
    admins = db(db.account.user_admin == 1).select()

    # Checks if user is one of the admins
    userIsAdmin = False
    for admin in admins:
        if admin.user_email == get_user_email():
            userIsAdmin = True
    if userIsAdmin == False:
        redirect(URL('index'))

    form = Form(db.video, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('admin'))
    return dict(form=form)

@action('bump_video/<video_id:int>', method=['GET', 'POST'])
@action.uses(db, session, auth.user, url_signer.verify())
def bump_video(video_id=None):
    assert video_id is not None
    # Set current front video to 0
    frontVideo = db(db.video.front == 1).select().first()
    if frontVideo != None:
        db.video.update_or_insert(
            (db.video.id == frontVideo.id) &
            (db.video.video_name == frontVideo.video_name),
            front = 0
        )
    # Set new front video to 1
    newFrontVideo = db(db.video.id == video_id).select().first()
    db.video.update_or_insert(
        (db.video.id == newFrontVideo.id) &
        (db.video.video_name == newFrontVideo.video_name),
        front = 1
    )
    redirect(URL('admin'))

@action('delete_video/<video_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete_video(video_id=None):
    assert video_id is not None
    db(db.video.id == video_id).delete()
    redirect(URL('admin'))

@action('profile', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'profile.html')
def profile():
    # Get users first name
    rows = db(db.account.user_email == get_user_email()).select()
    row = rows[0]
    name = row.user_first_name

    p = db(db.account.user_email == get_user_email()).select()
    x = p[0]

    p = db.account[x.id]

    return dict(name=name, row=row)

@action('edit_profile', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit_profile.html')
def edit_profile():
    # Get users first name
    rows = db(db.account.user_email == get_user_email()).select()
    row = rows[0]
    name = row.user_first_name

    p = db(db.account.user_email == get_user_email()).select()
    x = p[0]

    p = db.account[x.id]
    form = Form(db.account, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted:
        redirect(URL('profile'))

    return dict(form=form, name=name)
