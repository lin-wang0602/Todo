from model import db,User,Todo,Todo_item, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_todo_list(description, notes, categeories):
    todo_list = Todo(
        description = description,
        notes=notes,
        categeories=categeories,
    )
    return todo_list

def get_all_todos():

    all_todos = Todo.query.all()

    return all_todos

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
