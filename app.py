from flask import Flask, request, jsonify
from routes import movie_blue_print;
app = Flask(__name__)

app.register_blueprint(movie_blue_print)



if __name__ == '__main__':
    app.run(debug=True)
