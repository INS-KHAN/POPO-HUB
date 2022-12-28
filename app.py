from popocrawler import PopoCrawler
from flask import Flask, jsonify, render_template, request

ppc = PopoCrawler()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list/")
def list():
    prmts = request.args.to_dict()
    return jsonify(ppc.get_list(prmts["site"], int(prmts["page"])))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
