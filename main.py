"""
ThesisTutorAgent

一个具备自主搜索与图谱学习能力的毕业论文智能指导助手，分为知识拓荒、图谱定位、金牌导师三个模块

初始输入: queries_about_writing_papers
最终输出: sub_knowledge_graph

使用方法:
    python main.py

【开发指导 - 模块间数据传递】
模块间的数据传递通过状态管理实现。

【使用说明】
1. 数据传递方式: 将需要传递的数据存入 state 的某个属性中
2. 例如: 在模块A中将数据存入 state["模块A"]["输出字段"] = 值
3. 在模块B中从 state["模块A"]["输出字段"] 读取数据
4. 状态管理原则:
   - 每个模块有独立的状态空间 (如 state["informationretrieval"])
   - 模块间通过状态读写进行数据传递
   - 确保前序模块的输出字段与后续模块的输入字段对应

【模块通信函数说明】
在 def route_central_control(state):
    \"\"\"
    自动生成的路由函数 - central_control
    
    根据状态决定路由到哪个分支
    \"\"\"
    # TODO: 实现路由逻辑
    # 根据 state 中的某些字段决定返回哪个分支
    # 返回 "branch_1", "branch_2", ... 或 "default"
    return "default"

 中定义模块间的条件边函数。
这些函数用于:
1. 从前一模块的状态中提取需要传递的数据
2. 将数据传递给后续模块
3. 根据状态决定路由到哪个模块

示例:
```python
def route_after_moduleA(state: AgentState) -> str:
    # 从模块A的状态中提取数据
    module_a_output = state.get("modulea", "").get("output_field", "")

    # 将数据存入下一模块的状态（可选）
    # state["moduleb"]["input_field"] = module_a_output

    # 根据数据决定路由
    if module_a_output:
        return "moduleb"
    return END
```
"""

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from modules.knowledgeexplorer.build import build_knowledgeexplorer_graph
from modules.knowledge_explorer.build import build_knowledge_explorer_graph
from modules.graphretriever.build import build_graphretriever_graph
from modules.guidancegenerator.build import build_guidancegenerator_graph
from modules.central_control.build import build_central_control_graph


def route_central_control(state):
    """自动生成的路由函数 - central_control
    
    根据状态决定路由到哪个分支
    """
    # TODO: 实现路由逻辑
    # 根据 state 中的某些字段决定返回哪个分支
    # 返回 "branch_1", "branch_2", ... 或 "default"
    return "default"



def build_main_graph():
    """构建主图"""
    workflow = StateGraph(AgentState)

    # 添加模块节点
    # 知识拓荒者模块(队员A)：负责联网搜索最新的论文指导资料，并将其提炼为知识点存入图谱
    knowledge_explorer_graph = build_knowledge_explorer_graph()
    workflow.add_node("knowledge_explorer", knowledge_explorer_graph)
    
    # 图谱领航员模块(队员B)：分析用户问题，去系统现有的知识图谱中匹配最对应的指导节点
    graphretriever_graph = build_graphretriever_graph()
    workflow.add_node("graphretriever", graphretriever_graph)
    
    # 金牌导师模块(队员C)：结合匹配到的学术规范和学生的具体困难，生成专属指导长文
    guidancegenerator_graph = build_guidancegenerator_graph()
    workflow.add_node("guidancegenerator", guidancegenerator_graph)
    
    # 中央调度,决定当前应用采取离线学习模式还是指导模式
    central_control_graph = build_central_control_graph()
    workflow.add_node("central_control", central_control_graph)
    


    # 添加模块间边
    workflow.add_edge(START, "knowledge_explorer")
    workflow.add_edge("graph_retriever", "guidance_generator")
    workflow.add_conditional_edges(
        "central_control",
        route_central_control,
        {"default": "graphretriever", "branch_2": "knowledgeexplorer"}
    )


    # 编译图
    app = workflow.compile(checkpointer=MemorySaver())

    return app


def main():
    """主函数"""
    # 构建主图
    app = build_main_graph()

    # 初始状态
    # TODO: 请根据业务需求填写初始状态
    # 格式: {{"字段名": 值, "模块名": {{"字段名": 值}}}
    initial_state = {{
        "queries_about_writing_papers": "test input",

    }}

    # 配置线程（用于持久化和中断恢复）
    config = {"configurable": {"thread_id": "1"}}

    # 运行图
    result = app.invoke(initial_state, config=config)

    # 输出结果
    # TODO: 请根据业务需求自定义输出格式
    print(result)