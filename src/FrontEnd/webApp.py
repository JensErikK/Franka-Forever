import time
from flask import Flask, render_template, session, request, url_for, flash, redirect

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def index():
    return redirect(url_for('pick'))


@app.route('/pick', methods=('GET', 'POST'))
def pick():

    if request.method != 'POST':
        return render_template('pick.html')
    
    if request.form['action'] == "Pick Everything":
        print("Will Pick and Place all detected objects")
        return redirect(url_for('executing', command="Pick Everything"))

    elif request.form['action'] == "Execute":
        command = request.form['command']
        print("Executing command: ")
        print(command)
        return redirect(url_for('executing', command=command))

    return redirect(url_for('executing'))

    

@app.route('/executing', methods=('GET', 'POST'))
def executing():

    if request.method == 'GET':
        session['command'] = request.args['command']
        return render_template('executing.html')

    command = session['command']
    if request.method == 'POST' and command:
        print("Executing: ")
        print(command)
        time.sleep(5)
    
    session['command'] = ""
    return redirect(url_for('pick'))