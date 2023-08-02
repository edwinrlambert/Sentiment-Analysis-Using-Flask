
# ? APP.PY

# Importing dependencies.
from flask import Flask
from views import views

# Creating a Flask application and registering the view.
app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

# Run the Flask application.
if __name__ == "__main__":
    app.run(debug=True)