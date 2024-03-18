import shlex
import subprocess
from flask import Flask
app = Flask(__name__)


@app.route("/uptime", methods=["GET"])
def uptime():
    command_str = f"uptime"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True).stdout
    return f"Current uptime is {result}"


if __name__ == "__main__":
    app.run(debug=True)