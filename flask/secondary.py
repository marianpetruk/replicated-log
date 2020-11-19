from flask import Flask
from flask_cors import CORS

from flask.sec_views import SecondaryView

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.add_url_rule('/secondary', view_func=SecondaryView.as_view('secondary_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001)
