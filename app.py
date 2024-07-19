from flask import Flask
import app_view

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.register_blueprint(app_view.blueprint)

if __name__ == "__main__":
    app.run(debug=True)
