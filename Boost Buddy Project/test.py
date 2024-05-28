from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
notes = []
tasks = []

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    task_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completion_time = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('homepage.html', title='Home')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/task')
def task():
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('task'))

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completion_time = datetime.utcnow()
    db.session.commit()
    flash('Task marked as complete.', 'success')
    return redirect(url_for('task'))

@app.route('/create_task', methods=['POST'])
def create_task():
    task_name = request.form['task_name']
    task_description = request.form['task_description']
    task_date = request.form['task_date']
    task_date = datetime.strptime(task_date, '%Y-%m-%dT%H:%M')
    new_task = Task(task_name=task_name, task_description=task_description, task_date=task_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task'))

@app.route('/addtask')
def addtask():
    return render_template('addtask.html')

@app.route('/notes')
def note():
    return render_template('notes.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append(note)
    return redirect(url_for('note'))

@app.route('/delete_note/<int:note_index>', methods=['POST'])
def delete_note(note_index):
    if note_index < len(notes):
        del notes[note_index]
    return redirect(url_for('note'))

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)