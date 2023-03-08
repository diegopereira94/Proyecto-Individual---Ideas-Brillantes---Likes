from flask import render_template, redirect, session, request, flash
from ideas_app import app
from ideas_app.models.user import User
from ideas_app.models.post import Post
from ideas_app.models.like import Like


@app.route('/like/<int:post_id>/<int:user_id>')
def like(post_id,user_id):
    data ={ 
        "user_id" : user_id,
        "post_id" : post_id,
        "likes" : 1,
        "iduser_liked" : session['user_id']
    }
    verificar_si_el_post_no_tiene_like = Like.verificar_si_el_post_no_tiene_like(data)
    print('verificar_si_el_post_no_tiene_like TRAE==========:', verificar_si_el_post_no_tiene_like)
    verificar_si_el_like_pertenece_alusuario = Like.verificar_si_el_like_pertenece_alusuario(data)

    if(verificar_si_el_post_no_tiene_like is not None): # Si el post no tiene like y existe entonces entra
        Like.update(data) # Actualiza el estado de la columna 'likes' a 1
    elif verificar_si_el_like_pertenece_alusuario is not None: # Si el post tiene like y pertenece al usuario actual entonces ENTRA
        Like.update_dislike(data)
    else:
        Like.create_like(data)

    return redirect('/bright_ideas')
