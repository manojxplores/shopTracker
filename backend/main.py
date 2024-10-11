from flask import Flask, request, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Testing"

if __name__ == "__main__":
    app.run(debug=True)

