from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import CoachState

# Initialisation du modèle Gemini
llm_methodo = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.4
)

# Le Prompt injecté
SYSTEM_PROMPT = """Tu es un méthodologue. Ton rôle est d'aider à structurer et planifier les idées. 
Analyse le message de l'étudiant et propose une méthodologie claire et organisée."""

def methodologue_node(state: CoachState):
    """Nœud exécutant l'agent Méthodologue"""
    messages = state["messages"]
    
    # On injecte le System Prompt s'il n'est pas déjà dans l'historique
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_methodo.invoke(messages)
    
    # On retourne le nouveau message pour l'ajouter à l'état global
    return {"messages": [response]}