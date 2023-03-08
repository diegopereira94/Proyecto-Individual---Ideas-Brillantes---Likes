from flask import render_template, redirect, session, request, flash
from ideas_app import app
from ideas_app.models.user import User
from ideas_app.models.post import Post
from ideas_app.models.like import Like
from ideas_app.models.contador_post import Contador_post


# ===========AGREGAR UN NUEVO POST=========================
@app.route('/add_new_post', methods=['POST'])
def add_new_post():
    data ={
        "description": request.form["description"],
        "user_id" : session['user_id']
    }
    # VALIDAMOS ANTES DE INSERTAR EN LA BD
    if not Post.validate_post(data): 
        return redirect('/bright_ideas')
    # GUARDA EN LA BASE DE DATOS
    post_id = Post.save(data)
    '''
    data_like ={
        "user_id" : session['user_id'],
        "post_id" : post_id,
        "likes" : 0,
        "iduser_liked" : 0 # Al crear un nuevo post se envía el 'iduser_liked' como cero(0) porque ese campo se utiliza para saber que usuario le da like a un post, 
    }                      # entonces cuando se le de like al post ahí se hace un update para cambiar el estado de 'iduser_liked' al id del usuario actual

    Like.create_like(data_like) # Después de crear un nuevo post, también creamos un nuevo registro en likes con ambos estados en cero
    '''
    return redirect('/bright_ideas')


@app.route('/bright_ideas')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }

    # Traigo todos los post de la base de datos y guardo en la variable 'posts'
    posts = Post.get_all()
    all_likes_by_post =[]

    # Recorre todo lo que tiene posts
    for post in posts:
        id_post = post.id # guardo el id del post de esta iteración

        # Creo un diccionario 'data_post' para después pasar el 'id' del post de esta iteración
        data_post ={
        "id": id_post
        }
        # Traigo la suma de likes de cada post
        cont = Contador_post.get_total_likes_by_post(data_post)
        print('CONT TRAE:', cont)

        # Itera el 'cont' y guarda su valor en la lista 'all_likes_by_post'
        for row in cont:
            all_likes_by_post.append(row)
    print('all_likes_by_post', all_likes_by_post)
    
    return render_template("dashboard.html", user_logueado = User.getId(data), posts = Post.get_all(), like_by_user = Like.get_like_by_user(data), Likes_by_post = all_likes_by_post)



@app.route('/bright_ideas/<int:post_id>')
def show_detail_post(post_id):
    data={
        "id": post_id
    }

    return render_template('detail_post.html', one_post = Post.get_one_post_by_id(data))


@app.route('/delete/<int:post_id>')
def delete(post_id):
    data = {
        "user_id" : session['user_id'],
        "post_id" : post_id,
    }
    Like.destroy(data)
    Post.destroy(data)
    return redirect('/bright_ideas')

