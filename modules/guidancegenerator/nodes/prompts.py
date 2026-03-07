"""
guidancegenerator 模块 - 系统提示词定义
"""

# 系统提示词定义
# TODO: 请根据业务需求填写以下提示词内容
# 格式: "节点名": """提示词内容""",
SYSTEM_PROMPTS = {

}


def get_system_prompt(node_name: str) -> str:
    """获取指定节点的系统提示词"""
    return SYSTEM_PROMPTS.get(node_name, "你是一个智能助手，请根据输入提供详细、准确的回应。")
