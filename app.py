from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"


app.run()
# app.run(debug=True, host='0.0.0.0', port='80')