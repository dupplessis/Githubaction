from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Deployed using GitHub Actions Self-Hosted Runner on Ubuntu EC2 + Docker Hub"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)