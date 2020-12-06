from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Class Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Main page / Index of the webapp
@app.route('/')
def index():
    print('Servering up the index page')
    #Show all Todo items
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('index.html', todo_list=todo_list)

# About page # TODO: Update later.
@app.route('/about')
def about():
    print('Servering up the about page')
    return "About"

#Adding new items to your plate
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

#Updating the todo items on your list
@app.route('/update/<int:todo_id>')
def update(todo_id):
    #find and update the item in the database.
    item = Todo.query.filter_by(id=todo_id).first()
    item.complete = not item.complete
    db.session.commit()
    return redirect(url_for("index"))

# Delte! the item from the todo list
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    #find and update the item in the database.
    item = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

if __name__  == "__main__":
    db.create_all()

    #Sample code for creating an item in the database
    # new_todo = Todo(title="todo 1", complete=False)
    # db.session.add(new_todo)
    # db.session.commit()
    app.run(host='0.0.0.0')
