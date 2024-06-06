
from CommandExecuter import CommandExecuter
from flask import Flask, jsonify, request


app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/execute', methods=['GET'])
async def execute():

    command = request.args.get('command')

    with CommandExecuter() as executer:
        await executer.Execute(command)

    return jsonify({"message": f"Command execution complete with command: {command}"})

@app.route('/executeloop', methods=['GET'])
async def executeLoop():

    step = request.args.get('step')

    with CommandExecuter() as executer:
        await executer.ExecuteLoopStep(step)

    return jsonify({"message": f"Step in show loop completed: {step}"})
    

if __name__ == "__main__":
    app.run(port=5001)