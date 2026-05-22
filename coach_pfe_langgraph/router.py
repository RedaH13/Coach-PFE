from langgraph.graph import StateGraph, END
from state import CoachState
from utils.logger import log_telegram_message
from agents.methodologue import methodologue_node
from agents.correcteur import correcteur_node

def route_message(state: CoachState):
    """L'équivalent de ton nœud Switch n8n"""
    last_message = state["messages"][-1].content.lower()
    
    # Logique du Switch n8n
    if "/methodo" in last_message:
        return "methodologue"
    elif "/correct" in last_message:
        return "correcteur"
    else:
        # Fallback
        return "methodologue" 

# Graph
workflow = StateGraph(CoachState)

# On ajoute les nœuds (minds)
workflow.add_node("methodologue", methodologue_node)
workflow.add_node("correcteur", correcteur_node)

# Le point d'entrée : On logue le message, puis on route
def entry_logger_node(state: CoachState):
    log_telegram_message(state)
    return state # just le log

workflow.add_node("entry_logger", entry_logger_node)
workflow.set_entry_point("entry_logger")

# La logique de routage conditionnel
workflow.add_conditional_edges(
    "entry_logger",
    route_message,
    {
        "methodologue": "methodologue",
        "correcteur": "correcteur"
    }
)

# Fin de l'exécution
workflow.add_edge("methodologue", END)
workflow.add_edge("correcteur", END)

# Compilation du graphe
app = workflow.compile()