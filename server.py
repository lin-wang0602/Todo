from flask import (Flask, render_template, request, flash, session,redirect, jsonify)
from model import connect_to_db, db,User,Todo_item,Todo,Category
import crud
import os
from jinja2 import StrictUndefined
from datetime import datetime
import requests


app = Flask(__name__)


app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
PEXELS_API_KEY= os.environ['PEXELS_API_KEY']


@app.route('/')
def homepage():

    return render_template ('homepage.html')


@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("You have successfully logout")
    return redirect("/login")

@app.route('/change_password', methods=["GET","POST"])
def change_password():
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    current_password = user.password
    if request.method == "POST":
        current_password = request.form.get("curr_password")
        new_password=request.form.get("new_password")
        if current_password == user.password:
            user.password = new_password
            db.session.commit()
            flash('Updated password suceessfully!')
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Current password is incorrect'})
    else:
        return render_template('change_pass.html')

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Please try again with another email.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/login")


@app.route('/todos')
def detail():
    logged_in_email = session.get("user_email")
    categories =Category.query.all()
    user = crud.get_user_by_email(logged_in_email)
    todos = crud.get_all_todos_by_user_id(user.user_id)
    items = Todo_item.query.all()
    all_completed = {}
    for todo in todos:
        completed = True
        for item in todo.todo_items:
            if not item.completed:
                completed = False
        all_completed[todo] = completed

    return render_template("all_todos.html",todos=todos,categories=categories,items=items,all_completed=all_completed)


@app.route('/todos',methods=["POST"])
def todo_detail():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/login')
    else:
        session["user_email"] = user.email
        flash(f"Welcome! {user.email}!")
        return redirect('/todos')


@app.route('/create/',methods=["GET","POST"])
def create_list():
    logged_in_email = session.get("user_email")
    if request.method == 'POST':
        description = request.form.get("description")
        notes = request.form.get("notes")
        category_name = request.form.get("category")
        image_url=request.form.get('image_url')
        user = crud.get_user_by_email(logged_in_email)
        user_id = user.user_id
        crud.create_todo_list(description=description,
                              notes=notes,
                              category_name=category_name,
                              user_id=user_id,
                              image_url=image_url)
        return redirect('/todos')

    return render_template("create_list.html")

@app.route('/api/pexels/<category>')
def pexels_api(category):
    url = f'https://api.pexels.com/v1/search?query={category}&per_page=4&page=1'
    headers = {'Authorization': PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    return jsonify(response.json())


@app.route('/todos/<todo_list_id>')
def show_todo_details(todo_list_id):

    todo = crud.get_todo_by_id(todo_list_id)
    items = crud.get_todo_items(todo_list_id)
    return render_template('todo_details.html',todo=todo,items=items)

@app.route('/todos/<todo_list_id>/create_item',methods=["GET","POST"])
def create_item(todo_list_id):
    if request.method == 'POST':
        todo_item_name = request.form.get("name")
        due_date = request.form.get('date')
        completed = request.form.get("completed")
        crud.create_items(todo_item_name=todo_item_name,
                          due_date = due_date,
                          completed=completed,
                          todo_list_id=todo_list_id)
        return redirect(f"/todos/{todo_list_id}")

    return render_template("create_items.html",todo_list_id=todo_list_id)

@app.route('/delete_todo/<todo_list_id>', methods=['POST'])
def delete_todo(todo_list_id):
    todo_list = Todo.query.get(todo_list_id)
    todos = Todo_item.query.filter_by(todo_list_id=todo_list_id).all()
    for todo in todos:
        db.session.delete(todo)

    db.session.delete(todo_list)
    db.session.commit()
    return redirect('/todos')


@app.route('/todos/<todo_list_id>/items/<todo_item_id>/update',methods=["GET","POST"])
def update_todo_item(todo_list_id,todo_item_id):
    todo = Todo.query.get(todo_list_id)
    item =Todo_item.query.get(todo_item_id)
    if request.method == "POST":
        item.todo_item_name = request.form.get('name')
        item.due_date = request.form.get('date')
        if request.form.get('completed') == "on":
            item.completed =True
        else:
            item.completed =False
        db.session.commit()
        flash('Updated suceessfully!')
        return redirect(f"/todos/{todo_list_id}")
    return render_template("update.html",item=item,todo=todo)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
