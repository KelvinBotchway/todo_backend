from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.task

# Route to get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]
    return jsonify(result)

# Route to create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    task = request.json.get('task')

    if not task:
        return jsonify({'error': 'Task is required.'}), 400

    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'id': new_todo.id, 'task': new_todo.task, 'completed': new_todo.completed}), 201

# Route to update a todo
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found.'}), 404

    task = request.json.get('task')
    completed = request.json.get('completed')

    if task is not None:
        todo.task = task
    if completed is not None:
        todo.completed = completed

    db.session.commit()

    return jsonify({'id': todo.id, 'task': todo.task, 'completed': todo.completed})

# Route to delete a todo
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({'error': 'Todo not found.'}), 404

    db.session.delete(todo)
    db.session.commit()

    return '', 204
