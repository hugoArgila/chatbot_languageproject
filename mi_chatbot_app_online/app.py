import streamlit as st
from dotenv import load_dotenv
import os

# Importar el cliente para QnA
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Importar el cliente para LUIS
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

def get_qna_answer(question, ai_client, ai_project_name, ai_deployment_name):
    """
    Envía la pregunta al servicio de QnA de Azure y devuelve la respuesta.
    """
    response = ai_client.get_answers(
        question=question,
        project_name=ai_project_name,
        deployment_name=ai_deployment_name
    )
    return response

def get_luis_intent_entities(query, luis_client, luis_app_id, luis_slot):
    """
    Envía la consulta al servicio LUIS y devuelve el análisis con la intención y las entidades.
    """
    prediction_response = luis_client.prediction.get_slot_prediction(
        app_id=luis_app_id,
        slot_name=luis_slot,
        query=query,
        verbose=True
    )
    return prediction_response

def main():
    # Configuración de la página
    st.set_page_config(page_title="Chatbot Integrado", layout="centered")
    st.title("Chatbot Integrado: QnA y LUIS")
    st.write("Escribe tu consulta y presiona 'Enviar' para obtener resultados de ambos modelos.")

    # Cargar variables de entorno
    load_dotenv()

    # Variables para el servicio QnA
    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
    ai_key = os.getenv('AI_SERVICE_KEY')
    ai_project_name = os.getenv('QA_PROJECT_NAME')
    ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

    # Variables para el servicio LUIS
    luis_endpoint = os.getenv('LUIS_ENDPOINT')
    luis_key = os.getenv('LUIS_KEY')
    luis_app_id = os.getenv('LUIS_APP_ID')
    luis_slot = os.getenv('LUIS_SLOT', 'Production')

    # Entrada de la consulta
    user_input = st.text_input("Escribe tu consulta:")

    if st.button("Enviar"):
        if user_input.strip() == "":
            st.warning("Por favor ingresa una consulta.")
        else:
            # Procesamiento de QnA
            st.markdown("## Resultados QnA")
            if not (ai_endpoint and ai_key and ai_project_name and ai_deployment_name):
                st.error("Falta configurar alguna variable de entorno para QnA. Revisa el archivo .env.")
            else:
                try:
                    credential = AzureKeyCredential(ai_key)
                    ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
                    qna_response = get_qna_answer(user_input, ai_client, ai_project_name, ai_deployment_name)
                    
                    if qna_response.answers:
                        for candidate in qna_response.answers:
                            st.markdown(f"**Respuesta:** {candidate.answer}")
                            st.markdown(f"**Confianza:** {candidate.confidence:.2f}")
                            st.markdown(f"**Fuente:** {candidate.source}")
                            st.write("---")
                    else:
                        st.info("No se encontró una respuesta para esa pregunta en QnA.")
                except Exception as e:
                    st.error(f"Ha ocurrido un error en QnA: {e}")

            # Separador entre servicios
            st.write("---")

            # Procesamiento de LUIS
            st.markdown("## Resultados LUIS (Intenciones y Entidades)")
            if not (luis_endpoint and luis_key and luis_app_id):
                st.error("Falta configurar alguna variable de entorno para LUIS. Revisa el archivo .env.")
            else:
                try:
                    credentials = CognitiveServicesCredentials(luis_key)
                    luis_client = LUISRuntimeClient(luis_endpoint, credentials)
                    luis_response = get_luis_intent_entities(user_input, luis_client, luis_app_id, luis_slot)
                    
                    # Mostrar la intención principal y su nivel de confianza
                    top_intent = luis_response.prediction.top_intent
                    intent_score = luis_response.prediction.intents[top_intent].score
                    st.markdown(f"**Intención detectada:** {top_intent}")
                    st.markdown(f"**Confianza de la intención:** {intent_score:.2f}")
                    st.write("---")

                    # Mostrar las entidades detectadas (si existen)
                    entities = luis_response.prediction.entities
                    if entities and "$instance" in entities:
                        st.markdown("### Entidades detectadas:")
                        for entity, instances in entities["$instance"].items():
                            for item in instances:
                                entity_text = item.get("text")
                                entity_score = item.get("score", 0)
                                st.markdown(f"- **Entidad:** {entity} | **Valor:** {entity_text} | **Confianza:** {entity_score:.2f}")
                    else:
                        st.info("No se detectaron entidades en la consulta con LUIS.")
                except Exception as e:
                    st.error(f"Ha ocurrido un error en LUIS: {e}")

if __name__ == '__main__':
    main()
