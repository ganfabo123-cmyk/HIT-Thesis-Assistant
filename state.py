from typing import TypedDict, Any, Annotated, List, Dict
import operator


class KnowledgeexplorerState(TypedDict):
    """knowledgeexplorer 模块状态"""
    knowledge_graph: dict
    queries_about_writing_papers: list

class GraphretrieverState(TypedDict):
    """graphretriever 模块状态"""
    sub_knowledge_graph: dict
    user_query: str

class GuidancegeneratorState(TypedDict):
    """guidancegenerator 模块状态"""
    advise: str
    sub_knowledge_graph: dict
    user_query: str

class Central_controlState(TypedDict):
    """central_control 模块状态"""
    current_instruction: str
    next_step: str


class AgentState(TypedDict):
    """全局状态定义"""
    user_input: str
    messages: Annotated[list, operator.add]
    knowledgeexplorer: KnowledgeexplorerState
    graphretriever: GraphretrieverState
    guidancegenerator: GuidancegeneratorState
    central_control: Central_controlState
