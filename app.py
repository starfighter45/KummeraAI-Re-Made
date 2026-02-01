from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    api_key = data.get("api_key")
    message = data.get("message")
    history = data.get("history")

    if not api_key:
        return jsonify({"reply": "Please enter your API key first."})

    try:
        client = OpenAI(api_key=api_key)

        messages = history + [{"role": "user", "content": message}]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
