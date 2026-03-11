"""
retrieve_input 节点定义
"""

from __future__ import annotations

from pathlib import Path
from langchain_core.messages import AIMessage
from state import AgentState

from .tools import build_knowledge_graph_from_markdown, _default_source_path


def retrieve_input(state: AgentState) -> AgentState:
    """
    读取知识库 Markdown 文件并生成知识图谱。
    """
    knowledge_state = state.get("knowledgeexplorer", {})
    queries = knowledge_state.get("queries_about_writing_papers", [])

    source_path = _default_source_path()
    if not source_path.exists():
        error_graph = {
            "metadata": {
                "source_path": str(source_path),
                "error": "source_markdown_not_found",
            },
            "nodes": [],
            "edges": [],
        }
        return {"knowledgeexplorer": {"knowledge_graph": error_graph}}

    markdown = source_path.read_text(encoding="utf-8")
    graph = build_knowledge_graph_from_markdown(markdown, str(source_path), queries=queries)

    summary = (
        f"已从 {source_path.name} 生成知识图谱，"
        f"节点数 {graph['metadata']['node_count']}，"
        f"边数 {graph['metadata']['edge_count']}。"
    )

    return {
        "messages": [AIMessage(content=summary)],
        "knowledgeexplorer": {"knowledge_graph": graph},
    }