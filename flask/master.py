from flask import Flask
from flask_cors import CORS

from flask.views import MessageView

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.add_url_rule('/message', view_func=MessageView.as_view('message_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
