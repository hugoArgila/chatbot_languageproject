import streamlit as st
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta, date, timezone
from dateutil.parser import parse as is_date

# Importar los clientes de Azure
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.conversations import ConversationAnalysisClient

def get_qna_answer(question, qna_client, qa_project_name, qa_deployment_name):
    """
    Envía la pregunta al servicio QnA y devuelve la respuesta.
    """
    response = qna_client.get_answers(
        question=question,
        project_name=qa_project_name,
        deployment_name=qa_deployment_name
    )
    return response

def get_conversation_analysis(query, conv_client, conv_project_name, conv_deployment_name):
    """
    Envía la consulta al servicio de análisis de conversaciones y devuelve el resultado.
    """
    # Construir la tarea para el análisis conversacional
    task = {
        "analysisInput": {
            "conversationItem": {
                "text": query,
                "id": "1",
                "participantId": "user"
            }
        },
        "kind": "Conversation",
        "parameters": {
            "projectName": conv_project_name,
            "deploymentName": conv_deployment_name,
            "verbose": True
        }
    }
    result = conv_client.analyze_conversations(task)
    return result

def main():
    st.set_page_config(page_title="Chatbot Integrado", layout="centered")
    st.title("Chatbot Integrado: QnA y Conversation Analysis")
    st.write("Escribe tu consulta y presiona 'Enviar' para obtener resultados de ambos modelos.")

    # Cargar variables de entorno
    load_dotenv()

    # Variables compartidas (endpoint y key)
    service_endpoint = os.getenv('SERVICE_ENDPOINT')
    service_key = os.getenv('SERVICE_KEY')

    # Variables para QnA
    qa_project_name = os.getenv('QA_PROJECT_NAME')
    qa_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

    # Variables para Conversation Analysis
    conv_project_name = os.getenv('CONV_PROJECT_NAME')
    conv_deployment_name = os.getenv('CONV_DEPLOYMENT_NAME')

    # Verificar variables de entorno
    if not (service_endpoint and service_key):
        st.error("Falta configurar el endpoint o la key del servicio en el archivo .env.")
        return

    if not (qa_project_name and qa_deployment_name):
        st.error("Falta configurar el proyecto o deployment para QnA en el archivo .env.")
        return

    if not (conv_project_name and conv_deployment_name):
        st.error("Falta configurar el proyecto o deployment para Conversation Analysis en el archivo .env.")
        return

    # Crear los clientes de Azure
    credential = AzureKeyCredential(service_key)
    qna_client = QuestionAnsweringClient(endpoint=service_endpoint, credential=credential)
    conv_client = ConversationAnalysisClient(endpoint=service_endpoint, credential=credential)

    # Entrada de la consulta
    user_input = st.text_input("Escribe tu consulta:")

    if st.button("Enviar"):
        if user_input.strip() == "":
            st.warning("Por favor, ingresa una consulta.")
        else:
            st.markdown("## Resultados QnA")
            try:
                qna_response = get_qna_answer(user_input, qna_client, qa_project_name, qa_deployment_name)
                if qna_response.answers:
                    for candidate in qna_response.answers:
                        st.markdown(f"**Respuesta:** {candidate.answer}")
                        st.markdown(f"**Confianza:** {candidate.confidence:.2f}")
                        st.markdown(f"**Fuente:** {candidate.source}")
                        st.write("---")
                else:
                    st.info("No se encontró respuesta en QnA.")
            except Exception as e:
                st.error(f"Error en QnA: {e}")

            st.write("---")
            st.markdown("## Resultados Conversation Analysis")
            try:
                conv_result = get_conversation_analysis(user_input, conv_client, conv_project_name, conv_deployment_name)
                # La estructura de la respuesta dependerá de cómo hayas configurado el proyecto de Conversation Analysis.
                # Aquí se muestra una manera genérica de presentar el resultado.
                st.markdown("### Resultado Completo:")
                st.json(conv_result)
            except Exception as e:
                st.error(f"Error en Conversation Analysis: {e}")

if __name__ == '__main__':
    main()
