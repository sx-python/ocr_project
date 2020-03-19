from flask import jsonify

from ocr_project import create_app
from settings.default import Config

app = create_app(Config)


@app.route('/')
def index():
    data = {}
    for rule in app.url_map.iter_rules():
        data[rule.endpoint] = rule.rule
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.192.130')
