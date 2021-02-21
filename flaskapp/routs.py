from flask import render_template, request, flash, redirect, url_for, abort
from flaskapp import app, db, bcrypt
from flaskapp.dbmodels import Users, Posts, Contact
from datetime import datetime
from flaskapp import params
import os
import secrets
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.forms import Regestrationform, Loginform, updateform, Postform, Edit_post_form


@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    posts = Posts.query.filter_by().all()[0:params['number_post']]
    return render_template('index.html', params=params, posts=posts)


# saving image
def save_img(form_img_file):
    rendom_hex = secrets.token_hex(8)
    _, f_name, f_ext = os.path.split(form_img_file)
    img_fn = rendom_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/img/profile_pic', img_fn)
    form_img_file.save(img_path)
    return img_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = updateform()
    if request.method == 'POST' and form.validate_on_submit():
        if form.img_file.data:
            pic_file = save_img(form.img_file.data)
            current_user.img_file = pic_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.ph_no = form.ph_no.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('you details has been updated successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.ph_no.data = current_user.ph_no
        form.about_me.data = current_user.about_me
    posts = Posts.query.filter_by(user_id=current_user.id).all()
    user_ppic = url_for('static', filename='img/profile_pic/'+current_user.img_file)
    return render_template('account.html', params=params, posts=posts,
                           form=form, user_ppic=user_ppic, title='My Account')


@app.route('/about')
def about():
    return render_template('about.html', params=params, title='About')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        ph_no = request.form.get('ph_no')
        message = request.form.get('message')
        # form = contact_form
        # entry = Contact(name=form.name, email=form.email, message=form.message, ph_no=form.ph_no, date=datetime.now())
        entry = Contact(name=name, email=email, message=message, ph_no=ph_no, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash(f"Thanks dawg Your message has been received ", 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', params=params, title='Contact us')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Regestrationform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data, ph_no=form.ph_no.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your are registered successfully ", 'success')
        return redirect(url_for('login'))

    return render_template('register.html', params=params, form=form, title='Register on TheSuccor')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Loginform()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash('logged in  successfully', 'success')
        else:
            flash('wrong username or password', 'danger')
    return render_template('login.html', params=params, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/example')
def example():
    return render_template('example1.html', params=params)


@app.route('/post/<string:post_slug>', methods=['GET'])
def in_post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post, title='Post')


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = Postform()
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        postentry = Posts(title=title, content=content, slug=slug, user_id=current_user.id)
        db.session.add(postentry)
        db.session.commit()
        flash('your post has been created', 'success')
        return redirect(url_for('new_post'))
    return render_template('new_post.html', params=params, form=form, title='New Post')


@app.route('/account/edit_post/<string:sno>', methods=['GET', 'POST'])
@login_required
def edit_post(sno):

    post = Posts.query.filter_by(sno=sno).first()
    if post.user_id != current_user.id:
        abort(403)

    form = Edit_post_form()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        slug= request.form.get('slug')

        post = Posts.query.filter_by(sno=sno).first()
        post.title = title
        post.content = content
        post.slug = slug
        db.session.commit()
        flash('post edited successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content

    return render_template('edit_post.html', params=params, posts=post, form=form, sno=sno,  title='Register on TheSuccor')


@app.route('/delete/<string:sno>', methods=['GET', 'POST'])
@login_required
def delete_post(sno):
    post = Posts.query.filter_by(sno=sno).first()
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted successfully', 'success')
    return redirect(url_for('account'))


# @app.route('/back')
# @login_required
# def back():
#     return render_template('account.html', params=params)

# if confirmed: