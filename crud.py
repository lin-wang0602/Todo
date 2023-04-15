from model import db,User,Todo,Todo_item,Category, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user

def get_user_by_id(user_id):

    user = User.query.get(user_id)
    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_todo_list(description, notes,category_name,user_id,image_url):
    category_obj = Category.query.filter_by(category_name=category_name).one()
    todo_list = Todo(
        description = description,
        notes=notes,
        category_id=category_obj.category_id,
        user_id = user_id,
        img=image_url

    )
    db.session.add(todo_list)
    db.session.commit()
    return todo_list

def create_items(todo_list_id,todo_item_name,due_date,completed):
    todo_list=Todo.query.get(todo_list_id)
    item = Todo_item(
        todo_item_name=todo_item_name,
        due_date = due_date,
        completed=completed,
        todo_list_id=todo_list.todo_list_id
    )
    db.session.add(item)
    db.session.commit()
    return item

def get_all_todos():

    all_todos = Todo.query.all()

    return all_todos
def get_todo_by_id(todo_list_id):

    todo_list = Todo.query.get(todo_list_id)
    return todo_list


def get_todo_items(todo_list_id):

    all_items = Todo_item.query.filter_by(todo_list_id=todo_list_id).all()
    return all_items

def get_all_todos_by_user_id(user_id):
    """Return all todo lists for a given user ID."""

    user = get_user_by_id(user_id)
    if user is None:
        return []

    todo_lists = user.todo_lists
    return todo_lists

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
