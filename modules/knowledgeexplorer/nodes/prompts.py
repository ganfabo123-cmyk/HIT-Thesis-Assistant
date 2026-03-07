"""
knowledgeexplorer 模块 - 系统提示词定义
"""

# 系统提示词定义
# TODO: 请根据业务需求填写以下提示词内容
# 格式: "节点名": """提示词内容""",
SYSTEM_PROMPTS = {
    "retrieve_input": """你是一个智能助手，负责处理 retrieve_input 节点的任务。请根据输入提供详细、准确的回应。""",
    "think_retrieve_input": """在执行 retrieve_input 任务之前，请先进行思考和规划。分析当前状态，确定下一步行动，并说明你的推理过程。""",

}


def get_system_prompt(node_name: str) -> str:
    """获取指定节点的系统提示词"""
    return SYSTEM_PROMPTS.get(node_name, "你是一个智能助手，请根据输入提供详细、准确的回应。")
