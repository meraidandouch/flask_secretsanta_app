from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        ' SELECT u.id, u.username as gifter_name, ge.username as giftee_name'
        ' FROM giftee ge JOIN setter s ON s.giftee_id = ge.id'
        ' JOIN user u ON u.id = s.gifter_id where u.username = ? ' ,
        (g.user['username'],)
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        gifted = request.form.get('gifted', "")
        selected = request.form.get('selected', "")
        error1 = None
        error2 = None 
        error3 = None 
        error4 = None
        error5 = None 

        posts = get_db().execute(
            ' SELECT u.id, u.username, ge.username '
            ' FROM giftee ge JOIN setter s ON s.giftee_id = ge.id'
            ' JOIN user u ON u.id = s.gifter_id where u.username = ? ' ,
            (g.user['username'],)
        ).fetchall()
        dupes = get_db().execute(  
            ' SELECT ge.id '
            ' FROM giftee as ge'
            ' WHERE ge.username = ? and ge.selected = "yes"',
            (selected,)
        ).fetchall() 
        num_users = get_db().execute(  
            ' SELECT u.id'
            ' FROM user as u',
        ).fetchall() 

        if gifted == "": # if they did not click radio check box at all 
            error1 = 'Please answer the first question! Clicking yes or no is required.'
        if gifted == "yes" and selected == "NA": # if the user bought a ss gift and did not select a user 
            error2 =  "Please select a name from the dropdown menu if you already bought them a gift!"
        if gifted == "no" and selected != "NA":  # if the user selected a giftee they did not buy a gift for 
            error3 = "You selected a name from the dropdown menu but did not buy someone a gift. Try again."
        if posts: # if the user tries to draw again when they already have their secret santa 
            error4 = "You already have a secret santa! "
        if len(num_users) > 9: 
            error5 = "Max numbers of users reached. You cannot draw again as a secret santa."

        if error1 is not None:
            flash(error1)
        elif error2 is not None:
            flash(error2)
        elif error3 is not None: 
            flash(error3)
        elif error4 is not None: 
            flash(error4)
        elif error5 is not None: 
            flash(error5)
        else: 
            if gifted == "yes" and selected != "NA": # Manual Draw 
                if len(dupes) != 0 :  # If two people bought the same person a gift, prompt the user 
                    flash ("Oh no! It looks like someone already bought this person a gift. Consider drawing a random or discussing with your group.")
                else: 
                    db = get_db()
                    db.execute(
                        'INSERT INTO setter (gifter_id, giftee_id) ' 
                        'SELECT u.id, ge.id ' 
                        'FROM user u, giftee ge ' 
                        'WHERE u.username = ? and ge.username = ? ', 
                        (g.user['username'], selected)
                        )
                    db.commit()   
            else: # Random Draw 
                db = get_db()
                db.execute(
                    'INSERT INTO setter (gifter_id, giftee_id) '
                    'SELECT gifter_name.id, ge.id '
                    'FROM giftee as ge, '
                    ' (SELECT u.username, u.id from user u WHERE u.username = ?) gifter_name '
                    'WHERE ge.selected != "yes" and gifter_name.username != ge.username '
                    'ORDER BY RANDOM() '
                    'LIMIT 1', 
                    (g.user['username'],)
                    )
                db.commit()

            db = get_db()
            db.execute( # After assigning a giftee to a gifter, update the selected column value to yes 
            'UPDATE giftee ' 
            'SET selected = "yes" ' 
            'WHERE giftee.id IN ' 
            '(SELECT giftee_id FROM setter)', 
                    )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
