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

from inspect import signature
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

### Admin methods and pages

@action('admin')
@action.uses(db, session, auth.user, 'admin.html')
def admin_index():
    # Gets all admins
    admins = db(db.account.user_admin == 1).select()
    merch_rows = db(db.merch.item_cost != None).select()

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
        vidRows=vidRows,
        merch_rows=merch_rows,
        delete_item_url=URL('delete_item', signer=url_signer)
    )

@action('check_admin', method=["GET"])
@action.uses(db, session)
def check_admin():
    email = get_user_email()
    if email == None:
        return dict(admin=0)
    admin = db(db.account.user_email == email).select().first().user_admin
    return dict(admin=admin)

@action('about')
@action.uses(db, auth, 'about.html')
def about():
    return dict()

### Merch Endpoints

@action('merch')
@action.uses(db, auth, 'merch2.html')
def merch():
    rows = db(db.merch.item_cost != None).select()
    column_counter = 0
    item_counter = 0
    for i in rows:
        item_counter = item_counter + 1
    return dict(
        rows=rows,
        column_counter=column_counter,
        item_counter=item_counter,
        add_to_cart_url=URL('add_to_cart'),
    )



@action('test')
@action.uses(db, auth, 'Testmerch.html')
def merch():
    rows = db(db.merch.item_cost != None).select()
    column_counter = 0
    item_counter = 0
    for i in rows:
        item_counter = item_counter + 1
    return dict(
        rows=rows,
        column_counter=column_counter,
        item_counter=item_counter,
        load_merch_url=URL('load_merch'),
    )

@action('load_merch')
@action.uses(db)
def load_merch():
    rows = db(db.merch.item_cost != None).select().as_list()
    print(rows)
    column_counter = 0
    item_counter = 0
    for i in rows:
        item_counter = item_counter + 1
    return dict(rows=rows,
                column_counter=column_counter,
                item_counter=item_counter)

@action('merch_item/<merch_id:int>')
@action.uses(db, session, 'merch_item.html')
def merch_item(merch_id=None):
    assert merch_id is not None
    item = db(db.merch.id == merch_id).select().first()
    if item == None:
        redirect(URL('merch'))
    return dict(item=item)

@action('edit_merch/<merch_id:int>')
@action.uses(url_signer.verify(), db, session, auth.user, 'edit_merch.html')
def edit_merch(merch_id=None):
    assert merch_id is not None
    if merch_id == -1:
        item = db(db.merch.id).select().first()
        item.id = -1
    else:
        item = db(db.merch.id == merch_id).select().first()
    if item == None:
        redirect(URL('admin'))
    return dict(
        item=item,
        update_item_url=URL('update_item', signer=url_signer)
    )

@action('update_item', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def update_item():
    body = request.json.get('body')
    admin = db(db.account.user_email == get_user_email()).select().first().user_admin
    if admin == 0:
        redirect(URL('index'))
    else:
        if body["id"] == '-1' or body["id"] == -1:
            id = db.merch.insert(
                item_name = body["name"],
                item_cost = body["cost"],
                item_description = body["description"],
                item_stock = body["stock"],
                item_image = body["image_path"],
                item_type = body["type"]
            )
            return dict(id=id)
        else:
            db.merch.update_or_insert((db.merch.id == body.get("id")),
                item_name = body["name"],
                item_cost = body["cost"],
                item_description = body["description"],
                item_stock = body["stock"],
                item_image = body["image_path"],
                item_type = body["type"]
            )
    return 'ok'

@action('delete_item', method=["GET", "POST"])
@action.uses(db, session, url_signer.verify())
def delete_item():
    id = request.params.get('id')
    admin = db(db.account.user_email == get_user_email()).select().first().user_admin
    if admin == 0:
        redirect(URL('index'))
    else:
        db(db.merch.id == id).delete()
    return 'ok'

### Video Endpoints

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
    return dict(
        thevideo=videoURL,
        video_id=frontVideo.id,
        load_comments_url=URL('load_video_comments'),
        add_comment_url=URL('add_comment'),
        delete_comment_url=URL('delete_comment', signer=url_signer),
    )

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
    # Get user account
    user_account = db(db.account.user_email == get_user_email()).select().first()
    return dict(
        user_profile=user_account,
        profile_pic_url=URL('profile_pic', signer=url_signer),
        picture_upload_url=URL('picture_upload', signer=url_signer)
    )

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

@action('profile_pic', method=["GET"])
@action.uses(db, session, auth.user, url_signer.verify())
def profile_pic():
    profile = db(db.account.user_email == get_user_email()).select().first()
    return dict(
        picture = profile.picture
    )

@action('picture_upload', method=["POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def picture_upload():
    uploaded_file = request.body
    db.account.update_or_insert(
        (db.account.user_email == get_user_email()),
        picture = uploaded_file
    )
    profile = db(db.account.user_email == get_user_email()).select().first()
    return "ok"

@action('newsreg')
@action.uses(db, session, auth.user, 'newsletter.html')
def newsreg():
    a = db(db.account.user_email == get_user_email()).select().first()
    if a.newsletter is None:
        a.newsletter = 1
    elif a.newsletter == 0:
        a.newsletter = 1
    else:
        a.newsletter = 0
    a.update_record()
    return dict()


### Comments methods

@action('load_video_comments/<video_id:int>', method=["GET"])
@action.uses(db, session)
def load_video_comments(video_id=None):
    assert video_id is not None
    rows = db(db.comment.video_id == video_id).select().as_list()
    return dict(rows=rows)

@action('add_comment/<video_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user)
def add_comment(video_id=None):
    assert video_id is not None
    if get_user_email() == None:
        redirect(URL('video'))
    user_name = db(db.account.user_email == get_user_email()).select().first().user_username
    db.comment.insert(
        message_body=request.json.get('body'),
        user_email=get_user_email(),
        video_id=video_id,
        username=user_name,
    )
    return 'ok'

@action('delete_comment', method=["GET", "POST"])
@action.uses(url_signer.verify(), db, auth.user)
def delete_comment():
    id = request.params.get('id')
    print(request)
    comment = db(db.comment.id == id).select().first()
    account = db(db.account.user_email == get_user_email()).select().first()
    if (comment.user_email == account.user_email) or (account.user_admin > 0):
        db(db.comment.id == id).delete()
    else:
        return 'rejected'
    return 'ok'


@action('add_to_cart_redirect/<item_id:int>')
@action.uses(db)
def add_to_cart_redirect(item_id=None):
    assert item_id is not None
    cart = db(db.shoppingCart.user == get_user_email()).select().first()
    if cart is None:
        itemList = [item_id]
        db.shoppingCart.insert(user=get_user_email(), merch_list=itemList, item_count=1)
    else:
        item_list = cart.merch_list
        item_list.append(item_list)
        count = cart.item_count + 1
        db(db.shoppingCart.user == get_user_email()).update(merch_list=item_list, item_count=count)
    redirect(URL('merch'))
    return

@action('add_to_cart')
@action.uses(db) #might want to not use verify yet for testing purposes
def add_to_cart():
    user = get_user_email()
    item_id = request.params.get('id')
    assert item_id is not None
    item_ref = db(db.merch.id == item_id).select().first()
    cart = db(db.shoppingCart.user == user).select().first()
    if cart is None:
        list = []
        list.append(item_ref)
        db.shoppingCart.insert(user=get_user_email(), merch_list=list, item_count=1)
    else:
        list = cart.merch_list
        list.append(item_ref)
        count = cart.item_count
        db(db.shoppingCart.user == user).update(merch_list=list, item_count=count + 1)
    return "ok"


@action('delete_from_cart')
@action.uses(db) #might want to not use verify yet for testing purposes
def delete_from_cart():
    #-------------------------
    #NOT IMPLEMENTED DO NOT USE
    #--------------------------

    #user = get_user_email()
    #item_id = request.params.get("item")
    #item_ref = db(db.merch.id == item_id).select()
    #cart = db(db.account.user_email == user).select(db.account.shoppingCart)
    #cart.update_record(items=cart.merch_list.remove(item_ref))
    return "ok"

