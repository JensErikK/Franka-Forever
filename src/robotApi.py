
from CommandExecuter import CommandExecuter
from quart import Quart, jsonify, request


app = Quart(__name__)
app.secret_key = 'super secret key'

@app.route('/execute', methods=['GET'])
async def execute():

    with CommandExecuter() as executer:
        command = request.args.get('command')
        print(f"Command: {command}")
        await executer.Execute(command)

        return jsonify({"message": f"Command execution complete with command: {command}"})

@app.route('/executeloop', methods=['GET'])
async def executeLoop():

    step = int(request.args.get('step'))

    with CommandExecuter() as executer:
        await executer.ExecuteLoopStep(step)

    return jsonify({"message": f"Step in show loop completed: {step}"})
    

if __name__ == "__main__":
    app.run(port=5001)