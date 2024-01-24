
from CommandExecuter import CommandExecuter
from quart import Quart, render_template, session, request, url_for, flash, redirect

app = Quart(__name__)
app.secret_key = 'super secret key'

@app.route('/')
async def index():
    return redirect(url_for('pick'))


@app.route('/pick', methods=('GET', 'POST'))
async def pick():

    if request.method != 'POST':
        return await render_template('pick.html')
    
    form = await request.form

    if form['action'] == "Pick Everything":
        print("Will Pick and Place all detected objects")
        return redirect(url_for('executing', command="Pick Everything"))
    
    if form['action'] == "Reset":
        print("Will Reset Robot to defautl pos")
        return redirect(url_for('executing', command="Reset"))

    elif form['action'] == "Execute":
        command = form['command']
        print("Executing command: ")
        print(command)
        return redirect(url_for('executing', command=command))

    return redirect(url_for('executing'))

    

@app.route('/executing', methods=('GET', 'POST'))
async def executing():

    if request.method == 'GET':
        session['command'] = request.args['command']
        return await render_template('executing.html')

    command = session['command']
    if request.method == 'POST' and command:
        print("Executing: ")
        print(command)
        with CommandExecuter() as executer:
            await executer.Execute(command)
    
    session['command'] = ""
    return redirect(url_for('pick'))

if __name__ == "__main__":
    app.run()