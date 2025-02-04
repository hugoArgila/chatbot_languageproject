import streamlit as st
from dotenv import load_dotenv
import os

# Importar las clases necesarias de Azure
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

def get_answer(question, ai_client, ai_project_name, ai_deployment_name):
    """
    Envía la pregunta al servicio de Azure y devuelve la respuesta.
    """
    response = ai_client.get_answers(
        question=question,
        project_name=ai_project_name,
        deployment_name=ai_deployment_name
    )
    return response

def main():
    # Configuración de la página
    st.set_page_config(page_title="Chatbot con Streamlit", layout="centered")
    st.title("NBA Chatbot")
    st.write("Escribe tu pregunta y presiona 'Enviar' para obtener una respuesta.")

    # Cargar variables de entorno
    load_dotenv()
    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
    ai_key = os.getenv('AI_SERVICE_KEY')
    ai_project_name = os.getenv('QA_PROJECT_NAME')
    ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

    # Verificar que se hayan configurado las variables de entorno
    if not (ai_endpoint and ai_key and ai_project_name and ai_deployment_name):
        st.error("Falta configurar alguna variable de entorno. Revisa el archivo .env.")
        return

    # Crear el cliente de Azure
    credential = AzureKeyCredential(ai_key)
    ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

    # Entrada de la pregunta del usuario
    user_question = st.text_input("Haz tu pregunta:")

    # Botón para enviar la pregunta
    if st.button("Enviar"):
        if user_question.strip() == "":
            st.warning("Por favor ingresa una pregunta.")
        else:
            try:
                response = get_answer(user_question, ai_client, ai_project_name, ai_deployment_name)
                if response.answers:
                    # Mostrar cada respuesta candidata
                    for candidate in response.answers:
                        st.markdown(f"**Respuesta:** {candidate.answer}")
                        st.markdown(f"**Confianza:** {candidate.confidence:.2f}")
                        st.markdown(f"**Fuente:** {candidate.source}")
                        st.write("---")
                else:
                    st.info("No se encontró una respuesta para esa pregunta.")
            except Exception as e:
                st.error(f"Ha ocurrido un error: {e}")

if __name__ == '__main__':
    main()
