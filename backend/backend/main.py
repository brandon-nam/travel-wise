from flask import Flask

app = Flask(__name__)


def main() -> None:
    app.run(host='0.0.0.0', port=3203)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    main()
