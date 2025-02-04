from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# Charge local environment variables (for development)
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    question = request.form.get("question")
    #Chatbot logic
    answer = f"Recibí tu pregunta: {question}"
    return render_template("index.html", question=question, answers=[{'answer': answer, 'confidence': 'N/A', 'source': 'Local'}])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)