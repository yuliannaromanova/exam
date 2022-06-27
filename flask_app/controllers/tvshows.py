from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.tvshow import Tvshow
from flask_app.models.user import User

@app.route('/new/tvshow')
def new_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_tvshow.html')

@app.route('/create/tvshow', methods=['POST'])
def create_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshow(request.form):
        return redirect('/new/tvshow')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "network": request.form["network"],
        "user_id": session["user_id"],
    }
    Tvshow.save(data)
    return redirect('/')


@app.route('/destroy/tvshow/<int:id>')
def destroy_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    clickedTvshow = Tvshow.get_one(data)
    if clickedTvshow['user_id'] == session['user_id']:
        Tvshow.destroy(data)
        return redirect ('/')
    return redirect('/')


@app.route('/tvshow/<int:id>')
def show_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    return render_template('show_tvshow.html', tvshow = Tvshow.get_one(data))

@app.route('/edit/tvshow/<int:id>')
def edit_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('edit_tvshow.html', edit = Tvshow.get_one(data))

@app.route('/update/tvshow/', methods=['POST'])
def update_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshow(request.form):
        return redirect(request.referrer)
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "id": request.form["id"],
    }
    Tvshow.update(data)
    return redirect('/')


@app.route('/tvshow/<int:id>/like', methods=['GET','PUT'])
def like_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'tvshow_id': id,
        'user_id': session['user_id'],
        
    }

    Tvshow.addLike(data)
    updatedTvshow = Tvshow.getUsersWhoLiked(data)
    updatedData = {
        'tvshow_id': id,
        'likes': updatedTvshow.likes
    }
    Tvshow.update(updatedData)
    tvshows = Tvshow.get_all()
    return render_template('index.html', tvshow=updatedTvshow,  user=User.get_by_id(data), all_tvshows=tvshows)

@app.route('/tvshows/<int:id>/unlike', methods=['GET','PUT'])
def unlike_tvshow(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'tvshow_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    updatedTvshow = Tvshow.getUsersWhoLiked(data)
    
    return render_template('index.html', tvshow=updatedTvshow,  user=User.get_by_id(data))

