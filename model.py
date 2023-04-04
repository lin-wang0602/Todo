from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    todo_lists = db.relationship("Todo", back_populates="users")


    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Todo(db.Model):
    """A Todo list."""

    __tablename__ = 'todo_list'

    todo_list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    description = db.Column(db.String)
    img = db.Column(db.String)
    notes = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))

    users = db.relationship("User", back_populates="todo_lists")
    todo_items = db.relationship("Todo_item", back_populates="todo_lists")
    categories= db.relationship("Category", back_populates="todo_lists")

    def __repr__(self):
        return f'<Todo todo_list_id={self.todo_list_id} description={self.description}>'


class Todo_item(db.Model):
    """A Todo_item."""

    __tablename__ = 'todo_item'

    todo_item_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    todo_item_name = db.Column(db.String, unique=True)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean)
    todo_list_id = db.Column(db.Integer, db.ForeignKey("todo_list.todo_list_id"))


    todo_lists = db.relationship("Todo", back_populates="todo_items")


    def __repr__(self):
        return f'<Todo_item todo_item_id={self.todo_item_id} name={self.todo_item_name}>'

class Category(db.Model):
    "A Category "
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    category_name = db.Column(db.String)

    todo_lists = db.relationship("Todo", back_populates="categories")


def connect_to_db(flask_app, db_uri="postgresql:///todos", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
