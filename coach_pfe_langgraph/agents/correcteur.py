from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from state import CoachState
from tools.mongo_retrievers import get_rag_tools # (On simulera ces outils)

llm_correcteur = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2
)

# On attache MongoDB tools (Normes, Mémoires, Guides) au modèle
rag_tools = get_rag_tools()
llm_with_tools = llm_correcteur.bind_tools(rag_tools)

SYSTEM_PROMPT = """Tu es un agent spécialisé en documentation académique. 
Ton rôle est de répondre aux questions en utilisant les documents vectorisés (guides académiques, mémoires, normes bibliographiques, règles typographiques)."""

def correcteur_node(state: CoachState):
    """Nœud exécutant l'agent Correcteur avec capacité RAG"""
    messages = state["messages"]
    
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}