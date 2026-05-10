from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.rag.retriever import retrieve
from app.rag.generator import generate_answer

# -------------------------
# STATE
# -------------------------
class AgentState(TypedDict):
    query: str
    chat_history: str
    docs: list
    answer: str
    needs_help: bool


# -------------------------
# NODE 1: MEMORY
# -------------------------
def memory_node(state: AgentState):
    # chat_history already passed from backend
    return {"chat_history": state["chat_history"]}


# -------------------------
# NODE 2: RETRIEVAL
# -------------------------
def retrieve_node(state: AgentState):
    docs = retrieve(state["query"])
    return {"docs": docs}


# -------------------------
# NODE 3: GENERATION
# -------------------------
def generate_node(state: AgentState):
    answer = generate_answer(
        query=state["query"],
        docs=state["docs"],
        chat_history=state["chat_history"]
    )
    return {"answer": answer}


# -------------------------
# NODE 4: DECISION (LIGHT)
# -------------------------
def decision_node(state: AgentState):
    query = state["query"].lower()

    # VERY LIGHT heuristic (fast, no extra LLM call)
    problem_keywords = [
        "not working", "error", "issue", "problem",
        "failed", "unable", "can't", "cannot"
    ]

    needs_help = any(k in query for k in problem_keywords)

    return {"needs_help": needs_help}


# -------------------------
# BUILD GRAPH
# -------------------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("memory", memory_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_node("decision", decision_node)

    graph.set_entry_point("memory")

    graph.add_edge("memory", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "decision")
    graph.add_edge("decision", END)

    return graph.compile()


# instantiate once
agent = build_graph()