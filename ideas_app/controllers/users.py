from flask import render_template, redirect, session, request, flash
from ideas_app import app
from ideas_app.models.user import User
from ideas_app.models.post import Post
from ideas_app.models.like import Like
from ideas_app.models.contador_post import Contador_post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "alias" : request.form["alias"],
        "email" : request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    #print('EL ID EN EL REGISTER TIENE VALOR:', id)
    session['user_id'] = id
    return redirect('/bright_ideas')


@app.route('/login', methods=['POST'])
def login():
    user = User.getEmail(request.form['email'])
    #print('USER EN EL LOGIN TIENE:', user)
    if not user:
        flash("Email inválido", "login")
        return redirect('/')
    if user is None or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Contraseña inválida", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/bright_ideas')
'''
@app.route('/bright_ideas')
def bright_ideas():
    return render_template('dashboard.html')
'''

@app.route('/users/<int:id_user>')
def user_view(id_user):
    data={
        "id": id_user
    }
    total_post = Contador_post.get_total_post_by_user(data)
    print('TOTAL DE POST DE ESTE USUARIO++++++++++++: ',total_post)
    total_likes = Contador_post.get_total_likes_by_user(data)
    print('TOTAL DE LIKES DE ESTE USUARIO***********: ',total_likes)


    return render_template('user_view.html', user = User.get_one(data), total_post = Contador_post.get_total_post_by_user(data), total_likes = Contador_post.get_total_likes_by_user(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')