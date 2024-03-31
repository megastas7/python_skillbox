import logging.config

from flask import Flask, request
from logger_config import dict_config

app = Flask(__name__)

logging.config.dictConfig(dict_config)
server_logger = logging.getLogger("server_logger")


@app.route('/log', methods=['POST'])
def log_post():
    msg = (request.form['levelname'] + " | " +
           request.form['name'] + " | " +
           request.form['asctime'] + " | " +
           request.form['lineno'] + " | " +
           request.form['message'])

    print(msg)
    return 'OK', 200


@app.route('/log', methods=['GET'])
def log_get():
    result = ''
    with open(f'calc.log', 'r') as logs:
        for log in logs.readlines():
            result += f'{log}<br>'
    return result


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(port=5555, debug=True)
