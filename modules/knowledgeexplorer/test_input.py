"""
knowledgeexplorer 模块 - 测试输入文件

用于测试 knowledgeexplorer 模块的独立运行。
用户只需修改 TEST_INPUT 字典中的值，然后运行此文件即可测试模块。
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from state import AgentState, KnowledgeexplorerState
from modules.knowledgeexplorer.build import build_knowledgeexplorer_graph


# ============================================
# 测试输入配置 - 请修改以下字典中的值
# ============================================
TEST_INPUT = {
    "knowledge_graph": {},  # dict
    "queries_about_writing_papers": [],  # list
}


def run_module_test():
    """运行模块测试"""
    # 构建模块图
    app = build_knowledgeexplorer_graph()
    
    # 构建初始状态
    initial_state = AgentState(
        messages=[],
        knowledgeexplorer=TEST_INPUT
    )
    
    # 运行模块
    print(f"正在运行 knowledgeexplorer 模块...")
    print(f"初始输入: {TEST_INPUT}")
    print("-" * 50)
    
    result = app.invoke(initial_state)
    
    print("-" * 50)
    print(f"模块运行完成!")
    print(f"最终状态: {result}")
    
    return result


if __name__ == "__main__":
    run_module_test()
