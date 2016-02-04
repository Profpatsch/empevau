from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "It werks. Endpoints: /submit, /stop"

@app.route("/submit", methods=["POST"])
def submit():
    g.mpv.play(request.form["uri"])

@app.route("/stop", methods=["POST"])
def stop():
    g.mpv.stop()

if __name__ == "__main__":
    app.run(debug=True)
