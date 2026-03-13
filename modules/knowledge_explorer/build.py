"""
knowledgeexplorer 模块构建脚本
"""

from langgraph.graph import StateGraph, END, START
from state import AgentState
from .nodes.retrieve_input import retrieve_input


def build_knowledge_explorer_graph():
    """构建 knowledgeexplorer 模块的图"""

    
    workflow = StateGraph(AgentState)
    
    # 请根据模块中的节点列表，手动添加节点
    workflow.add_node("retrieve_input", retrieve_input)

    # 请根据节点间的连接关系，手动添加边
    # 设置入口点
    workflow.add_edge(START, "retrieve_input")
    workflow.add_edge("retrieve_input", END)

    # 编译图
    app = workflow.compile()
    return app