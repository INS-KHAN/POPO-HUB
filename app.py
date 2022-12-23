from urllib.parse import parse_qs, urlparse

from popocrawler import PopoCrawler
from flask import Flask, jsonify, render_template, request


ppc = PopoCrawler()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/list/")
def list():
    prmts = request.args.to_dict()
    return jsonify(ppc.get_list(prmts["site"], int(prmts["page"])))


if __name__ == "__main__":
    app.run(debug=True)
