from flask import Flask, render_template, request, jsonify # type: ignore
from chatbot import chatbot_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("user_input", "")

    response = chatbot_response(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
