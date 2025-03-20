from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task Model with Priority and Completed fields
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    completed = db.Column(db.Boolean, default=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()  # Fetch all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    task_priority = request.form['priority']
    if task_content:
        new_task = Task(content=task_content, priority=task_priority)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = request.form['priority']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
