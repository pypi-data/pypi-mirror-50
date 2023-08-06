from flask import Flask
from flask import jsonify,request

app = Flask(__name__)


@app.route('/zabbix', methods=['GET', 'POST'])
def config_zabbix_func(**kwargs):

    return jsonify(request.get_json(True))

@app.route('/')
def test():
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)