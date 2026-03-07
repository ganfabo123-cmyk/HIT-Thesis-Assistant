"""
retrieve_input 节点定义

"""
from typing import TypedDict, List, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from state import AgentState
from config import get_llm
from .prompts import get_system_prompt

from .tools import nodes_generate

def retrieve_input(state: AgentState) -> AgentState:
    """
    
    """
    llm = get_llm()
    # 获取 LLM 并绑定工具
    # TODO: 请根据本节点需要调用的工具修改下面一行
    # 示例: llm_with_tools = llm.bind_tools([t1, t2, t3])

    from .tools import nodes_generate
    llm_with_tools = llm.bind_tools([nodes_generate])

    # 获取系统提示词
    # TODO: 请确保 prompts.py 中已定义本节点的系统提示词
    system_prompt = get_system_prompt("retrieve_input")

    # 构建消息列表
    # TODO: 请根据业务需求构建消息列表
    # 示例:
    # 消息构建方式一,从状态获取需要的属性后构建系统提示词和用户提示词:
    # topic = 
    # messages = [SystemMessage(content=system_prompt), HumanMessage(content=f"主题: {{topic}}")]
    # 或者把完整历史会话发给模型
    # messages = [SystemMessage(content=system_prompt), HumanMessage(content=f"主题: {{topic}}")] + state["messages"]
    
    messages = [SystemMessage(content=system_prompt), HumanMessage(content=f"xxx")]

    # 调用 LLM
    response = llm_with_tools.invoke(messages)

    # 更新状态
    # TODO: 请根据业务需求将输出写入模块状态

    return {"messages": [SystemMessage(content=system_prompt), HumanMessage(content=f"主题: {{topic}}"),response]}#更新状态,把本次会话新增的变量存到字典中返回,比如消息新增
