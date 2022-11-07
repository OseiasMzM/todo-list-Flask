from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):

    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    dtainc = db.Column(db.String(25), nullable=False)
    dtaatt = db.Column(db.String(25), nullable=False)

    def __rep__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def home():
    # return render_template("index.html")
    if request.method == 'POST':
        print("Adicionando...")
        task_title = request.form['title']
        task_content = request.form['content']
        
        hora = datetime.today().strftime('%d-%m-%Y %H:%M')
        atualizacao = '' 
        #hora = datetime.today().strftime('%Y-%m-%d')
        
        new_task = Todo(title=task_title,content=task_content, dtainc=hora, dtaatt = atualizacao)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
            print("Task adicionada!")

        except:
            return "There was an error while adding the task"
    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        print("Task deletada!")
        db.session.commit()
        return redirect('/')
        

    except:
        return 'There was an error while deleting that task'


    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        
        task.title = request.form['titlecontent']
        task.content = request.form['content']
        task.dtaatt = datetime.today().strftime('%d-%m-%Y %H:%M')


        try:
            print("Task atualizada!")
            db.session.commit()
            return redirect('/')
           

        except:
            return 'There was an issue while updating that task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    print("[backend] is running...")
    app.run(debug=True)

    # debug = True will make sure the app will run on the development server.
