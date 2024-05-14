import logging
from flask import Flask
from routes import movie_blue_print;
app = Flask(__name__)

app.register_blueprint(movie_blue_print)

# Logs Configuration part
formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
app.logger.setLevel(logging.DEBUG)  # Set log level to DEBUG
handler = logging.FileHandler('app.log')  # Log to a file movie_app_logs
handler.setFormatter(formatter)
app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run(debug=True)
