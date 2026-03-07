"""
central_control 模块构建脚本
"""

from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from state import AgentState
from .nodes.think_central_control_node1 import think_central_control_node1
from .nodes.central_control_node1 import central_control_node1
from .nodes.tools import TOOLS


# TODO: 请根据业务需求添加路由函数
# 示例:
# def route_after_node_name(state: AgentState) -> str:
#     """路由函数 - 从 state["messages"] 提取 ToolMessage"""
#     for msg in state["messages"]:
#         if hasattr(msg, "tool_call_id") and hasattr(msg, "content"):
#             tool_name = getattr(msg, "name", None)
#             tool_content = msg.content
#             state["模块名"]["字段名"] = tool_content
#             if tool_name == "xxx_response":
#                 return "target_node"
#     return "default_node"



def build_central_control_graph():
    """构建 central_control 模块的图"""
    workflow = StateGraph(AgentState)

    # TODO: 请根据模块中的节点列表，手动添加节点
    # 示例:
    # workflow.add_node("think_node1", think_node1)
    # workflow.add_node("node1", node1)
    # workflow.add_node("tools", ToolNode(tools=TOOLS))

    # TODO: 请根据节点间的连接关系，手动添加边
    # 示例:
    # workflow.add_edge(START, "think_node1")
    # workflow.add_conditional_edges(
    #     "think_node1",
    #     route_after_think_node1,
    #     {"node1": "node1"}
    # )
    # workflow.add_edge("node1", "tools")
    # workflow.add_conditional_edges(
    #     "node1",
    #     route_after_node1,
    #     {"node1_response": "node1", END: END}
    # )


    # TODO: 设置入口点
    # 示例: workflow.add_edge(START, "first_node")

    # 编译图
    app = workflow.compile()

    return app
