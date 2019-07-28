from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_cors import CORS
import os

# init app
app = Flask(__name__)
CORS(app)

# init base path
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # # stop it from complaining in the console 

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title):
        self.title = title

# Todo Schema
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_created')

# init schema
todo_schema = TodoSchema(strict=True)
todos_schema = TodoSchema(many=True, strict=True)

# Create Single Todo Item
@app.route('/todo', methods=['POST'])
def add_todo():
    title = request.json['title']

    new_todo = Todo(title)

    db.session.add(new_todo)
    db.session.commit()

    return todo_schema.jsonify(new_todo)


# Get Single Todo Item
@app.route('/todo/<id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    return todo_schema.jsonify(todo)


# Get All Todos
@app.route('/todo', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = todos_schema.dump(todos)
    return jsonify(result.data)


# Update Todo
@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    # get the old value
    todo_old = Todo.query.get(id)

    # get the new atribut value
    title = request.json['title']

    # set the new to the old
    todo_old.title = title

    # save to the db
    db.session.commit()

    return todo_schema.jsonify(todo_old)