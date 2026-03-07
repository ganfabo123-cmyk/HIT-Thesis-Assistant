"""
think_retrieve_input 思考节点
"""

from typing import TypedDict, List, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from state import AgentState
from config import get_llm
from .prompts import get_system_prompt


def think_retrieve_input(state: AgentState) -> AgentState:
    """
    retrieve_input 的思考节点
    """
    # 获取 LLM 并绑定思考工具
    llm = get_llm()
    from .tools import think_retrieve_input_response
    llm_with_tools = llm.bind_tools([think_retrieve_input_response])
    
    # 获取系统提示词
    system_prompt = get_system_prompt("think_retrieve_input")
    
    # 构建消息列表
    # 这里也可以采取和llm节点同样的构建方式,1 从状态获取必要信息构建系统和用户提示词或者 2 直接发送完整历史会话
    messages = [SystemMessage(content=system_prompt),HumanMessage(content='')] + state["messages"]
    
    # 调用 LLM 进行思考
    response = llm_with_tools.invoke(messages)
    
    # 更新状态
    return {"message":["需要新加入状态的消息"],"其余需要新加入状态的值":""}
