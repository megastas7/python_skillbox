import shlex
import subprocess

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/ps")
def _ps():
    args: list[str] = request.args.getlist('arg')
    arguments_cleaned = [shlex.quote(s) for s in args]
    command_str = f"ps {' '.join(arguments_cleaned)}"
    command = shlex.split(command_str)
    result = subprocess.run(command, capture_output=True)
    output = result.stdout.decode()
    return "<pre>${output}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
