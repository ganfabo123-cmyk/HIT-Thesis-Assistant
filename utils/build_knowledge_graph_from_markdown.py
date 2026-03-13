import re
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime, timezone

# 返回项目根目录路径
def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]

# 默认待解析源文件路径
def default_source_path() -> Path:
    return _project_root() / "parsed_file" /  "HIT_硕士学位论文中期报告_格式与字体字号要求（来自附件doc）.md"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ORDERED_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^\s*>\s?(.*)$")

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
