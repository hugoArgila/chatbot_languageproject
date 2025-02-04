from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Importar el cliente de Azure
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Cargar variables de entorno
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Crear el cliente de Azure
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    # Obtener la pregunta del usuario desde el formulario
    user_question = request.form.get("question", "")
    
    # Llamar al servicio de Azure
    try:
        response = ai_client.get_answers(
            question=user_question,
            project_name=ai_project_name,
            deployment_name=ai_deployment_name
        )
        
        # Recoger la respuesta (puedes personalizar el formato de salida)
        answers = []
        for candidate in response.answers:
            answers.append({
                "answer": candidate.answer,
                "confidence": candidate.confidence,
                "source": candidate.source
            })
        
        return render_template("index.html", question=user_question, answers=answers)
    
    except Exception as ex:
        # En caso de error, mostrar el mensaje
        return render_template("index.html", error=str(ex))

if __name__ == "__main__":
    app.run(debug=True)
