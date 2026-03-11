"""
knowledgeexplorer 模块 - 工具定义
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from langchain_core.tools import tool
from .models import nodes_generate_model, retrieve_input_response_model, think_retrieve_input_model


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ORDERED_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^\s*>\s?(.*)$")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_source_path() -> Path:
    return _project_root() / "HIT_硕士学位论文中期报告_格式与字体字号要求（来自附件doc）.md"


def _add_node(
    nodes: List[Dict],
    edges: List[Dict],
    node_type: str,
    parent_id: Optional[str],
    title: Optional[str] = None,
    content: Optional[str] = None,
) -> str:
    node_id = f"{node_type}_{len(nodes) + 1}"
    node: Dict = {"id": node_id, "type": node_type}
    if title:
        node["title"] = title
    if content:
        node["content"] = content
    nodes.append(node)
    if parent_id:
        edges.append({"source": parent_id, "target": node_id, "type": "contains"})
    return node_id


def build_knowledge_graph_from_markdown(markdown: str, source_path: str, queries: Optional[List[str]] = None) -> Dict:
    """Parse markdown into a simple knowledge graph structure."""
    nodes: List[Dict] = []
    edges: List[Dict] = []

    lines = markdown.splitlines()
    title = ""
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            title = m.group(2).strip()
            break

    doc_id = _add_node(
        nodes,
        edges,
        "document",
        None,
        title=title or "HIT 中期报告格式与字体字号要求",
        content=None,
    )

    stack: List[tuple[int, str]] = [(0, doc_id)]
    current_parent_id = doc_id

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == "---":
            continue

        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            heading_title = m.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent_id = stack[-1][1] if stack else doc_id
            section_id = _add_node(nodes, edges, "section", parent_id, title=heading_title, content=None)
            stack.append((level, section_id))
            current_parent_id = section_id
            continue

        m = BLOCKQUOTE_RE.match(line)
        if m:
            content = m.group(1).strip()
            if content:
                _add_node(nodes, edges, "note", current_parent_id, content=content)
            continue

        m = ORDERED_RE.match(line)
        if m:
            content = m.group(2).strip()
            if content:
                _add_node(nodes, edges, "item", current_parent_id, content=content)
            continue

        m = BULLET_RE.match(line)
        if m:
            content = m.group(1).strip()
            if content:
                _add_node(nodes, edges, "item", current_parent_id, content=content)
            continue

        _add_node(nodes, edges, "paragraph", current_parent_id, content=stripped)

    metadata = {
        "source_path": source_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "queries": queries or [],
        "node_count": len(nodes),
        "edge_count": len(edges),
    }

    return {"metadata": metadata, "nodes": nodes, "edges": edges}


@tool(args_schema=nodes_generate_model)
def nodes_generate(query: str) -> str:
    """Generate a knowledge graph from the HIT mid-term report format markdown file."""
    source_path = _default_source_path()
    markdown = source_path.read_text(encoding="utf-8")
    graph = build_knowledge_graph_from_markdown(markdown, str(source_path), queries=[query] if query else [])
    return json.dumps(graph, ensure_ascii=False, indent=2)


@tool(args_schema=retrieve_input_response_model)
def retrieve_input_response(response: str) -> str:
    """
     - 响应工具

    Args:
        响应内容

    Returns:
        结构化响应字符串
    """
    # 响应工具：用于强制 LLM 输出结构化数据
    return "Response recorded"


@tool(args_schema=think_retrieve_input_model)
def think_retrieve_input_response(result) -> str:
    """
    retrieve_input 节点的思考工具 - 用于思维链推理
    """
    # TODO: 根据 models.py 中定义的字段，返回结构化的思考结果
    return str(result)


# 工具列表 - 供 LLM 绑定使用
TOOLS = [nodes_generate, retrieve_input_response, think_retrieve_input_response]
