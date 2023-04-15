from flask import (Flask, render_template, request, flash, session,redirect, jsonify)
from model import connect_to_db, db,User,Todo_item,Todo
import crud
import os
from jinja2 import StrictUndefined
from datetime import datetime
from flask_login import LoginManager,login_user,current_user,login_required
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
    user = crud.get_user_by_email(logged_in_email)
    todos = crud.get_all_todos_by_user_id(user.user_id)
    return render_template("all_todos.html",todos=todos)

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
