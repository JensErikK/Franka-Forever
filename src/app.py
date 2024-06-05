
from CommandExecuter import CommandExecuter
from quart import Quart, render_template, jsonify, request
from threading import Thread
import asyncio

app = Quart(__name__)
app.secret_key = 'super secret key'

@app.route('/')
async def index():
    return await render_template('execute.html')

@app.route('/execute', methods=['GET'])
async def execute():

    command = request.args.get('command')

    execution_thread = Thread(target=asyncio.run, args=(execute_on_robot(command),))
    execution_thread.start()

    return jsonify({"message": f"Command exection started with command: {command}"})

@app.route('/executionstatus', methods=['GET'])
async def status():
    return jsonify({"running": CommandExecuter.IsExecuting})

@app.route('/stop', methods=['GET'])
async def stopLoop():
    CommandExecuter.IsLooping = False
    return jsonify({"message": "Execution loop will stop"})
    
async def execute_on_robot(command: str):
    with CommandExecuter() as executer:
        await executer.Execute(command)
    return "Finished"

if __name__ == "__main__":
    app.run()