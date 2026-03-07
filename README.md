# ThesisTutorAgent

一个具备自主搜索与图谱学习能力的毕业论文智能指导助手，分为知识拓荒、图谱定位、金牌导师三个模块

## 项目结构

```
.
├── main.py                 # 项目入口
├── state.py               # 状态定义
├── config.py              # 配置管理
├── requirements.txt       # 依赖列表
├── modules/               # 模块目录
### knowledgeexplorer
- 描述: 知识拓荒者模块(队员A)：负责联网搜索最新的论文指导资料，并将其提炼为知识点存入图谱
- 输入: queries_about_writing_papers, 
- 输出: knowledge_graph, 

### graphretriever
- 描述: 图谱领航员模块(队员B)：分析用户问题，去系统现有的知识图谱中匹配最对应的指导节点
- 输入: user_query
- 输出: sub_knowledge_graph

### guidancegenerator
- 描述: 金牌导师模块(队员C)：结合匹配到的学术规范和学生的具体困难，生成专属指导长文
- 输入: user_query, sub_knowledge_graph
- 输出: advise

### central_control
- 描述: 中央调度,决定当前应用采取离线学习模式还是指导模式
- 输入: current_instruction, 
- 输出: next_step, 


```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并配置以下环境变量：

```bash
# 使用 OpenAI API
LLM_API_KEY=your_api_key_here
LLM_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# 或使用其他兼容 OpenAI 的 API
# LLM_API_KEY=your_api_key_here
# LLM_URL=https://your-api-endpoint.com/v1
# LLM_MODEL=your-model-name
```

### 3. 运行项目

```bash
python main.py
```

## 模块说明

### knowledgeexplorer
- 描述: 知识拓荒者模块(队员A)：负责联网搜索最新的论文指导资料，并将其提炼为知识点存入图谱
- 输入: queries_about_writing_papers, 
- 输出: knowledge_graph, 

### graphretriever
- 描述: 图谱领航员模块(队员B)：分析用户问题，去系统现有的知识图谱中匹配最对应的指导节点
- 输入: user_query
- 输出: sub_knowledge_graph

### guidancegenerator
- 描述: 金牌导师模块(队员C)：结合匹配到的学术规范和学生的具体困难，生成专属指导长文
- 输入: user_query, sub_knowledge_graph
- 输出: advise

### central_control
- 描述: 中央调度,决定当前应用采取离线学习模式还是指导模式
- 输入: current_instruction, 
- 输出: next_step, 



## 开发指南

### 添加新节点

1. 在对应模块的 `nodes/` 目录下创建新的节点文件
2. 实现节点函数，接收和返回 `AgentState`
3. 在 `build.py` 中添加节点到工作流

### 修改提示词

编辑对应模块的 `prompts.py` 文件中的系统提示词。

### 添加工具

1. 在对应模块的 `tools.py` 中定义工具函数
2. 将工具添加到 `TOOLS` 列表
3. 在节点中使用 `bind_tools()` 绑定工具

## 注意事项

1. 确保所有节点正确处理 `state["messages"]`
2. 条件边函数必须返回目标节点名称或 "END"

---

## 详细开发指导

### 一、状态管理 (state.py)

#### 状态结构说明
- 基本变量: 如 `messages` (消息历史)
- 模块状态: 每个模块对应一个子状态字典

#### 如何定义模块子状态
```python
class ModuleNameState(TypedDict):
    field1: str
    field2: List[str]

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    module_name: ModuleNameState  # 模块状态
```

#### 状态读写
- 读取: `state["模块名"]["字段名"]`
- 写入: 返回增量更新字典 `{"模块名": {"字段名": 值}}`

### 二、工具实现 (tools.py)

#### 工具函数规范
1. 使用 `@tool` 装饰器
2. 通过 `args_schema` 绑定参数模型
3. 返回值必须是字符串

#### result 对象说明
- `result` 是包含工具执行结果的对象
- 常用类型:
  - `str`: 纯文本结果
  - `dict`: 结构化结果
  - `list`: 列表结果
  - 自定义类: 根据业务需求定义

#### 示例
```python
@tool(args_schema=search_model)
def websearchtool(query_string: str) -> str:
    """搜索工具"""
    result = search_api(query_string)
    return str(result)
```

### 三、模型定义 (models.py)

#### 思考模型字段建议
- 采用分布式推理,即为任务划分为多步,每一步对应一个属性


#### 示例
```python
class think_node_name_model(BaseModel):
    step1_analysis: str = Field(description="对任务的分析")
    step2_reasoning: str = Field(description="推理过程")
    step3_conclusion: str = Field(description="得出的结论")
```

### 四、提示词编写 (prompts.py)

#### 提示词内容建议
1. 角色定义: 明确 LLM 扮演的角色
2. 任务描述: 详细说明节点需要完成的任务
3. 输入参数: 说明输入数据的来源和含义
4. 输出格式: 指定输出的格式要求
5. 工具使用: 明确指导 LLM 何时、如何使用工具
6. 约束条件: 说明任务的限制和要求
7. 示例: 提供输入输出的示例

#### 提示词示例
```
你是一个专业的{{角色}}。你的任务是{{任务描述}}。
输入: {{输入参数说明}}
输出要求: {{输出格式要求}}
工具使用:
- 使用 think_{{node_name}} 工具进行思考
- 使用 {{node_name}}_response 工具返回结果
```

### 五、节点实现 (nodes/*.py)

#### 节点类型
1. LLM 节点: 使用 LLM 进行推理
2. 思考节点: 在 LLM 节点前进行思考
3. 工具节点: 执行具体的工具函数

#### 工具绑定方式
- 绑定所有工具: `llm.bind_tools(TOOLS)`
- 绑定指定工具: `llm.bind_tools([tool1, tool2])`
- 使用占位符: `llm.bind_tools([t1, t2, t3])`

#### 消息构建方式
1. 从状态获取必要信息后构建:
   ```python
   topic = state.get("模块名", {}).get("字段名", "")
   messages = [SystemMessage(content=system_prompt), HumanMessage(content=f"主题: {topic}")]
   ```
2. 发送完整历史会话:
   ```python
   messages = [SystemMessage(content=system_prompt)] + state["messages"]
   ```

#### 状态更新
- 直接修改: `state["key"] = value`(messages不能采取这种模式)
- 增量更新: `return {"messages": [response], "模块名": {"字段名": 值}}`

### 六、图构建 (build.py)


#### 节点类型说明
1. LLM 节点: 使用 LLM 进行推理
   - 每个 LLM 节点都有一个对应的思考节点
   - 每个 LLM 节点都伴随后续的工具调用
   - 工具类型: 要么是工具节点，要么是响应工具

2. 工具节点: 统一封装在 "tools" 节点中
   - 所有工具函数都在 tools.py 中定义
   - 使用 `ToolNode(tools=TOOLS)` 包装
   - 实际调用时,不调用Tools,因为它包含全部工具,而我们只需要调用当前节点需要的工具

#### 如何添加节点
```python
# 导入节点函数
from .nodes.{node_name} import {node_name}
from .nodes.think_{node_name} import think_{node_name}

# 添加节点到工作流
workflow.add_node("think_{node_name}", think_{node_name})
workflow.add_node("{node_name}", {node_name})
workflow.add_node("tools", ToolNode(tools=TOOLS))
```

#### 如何添加边
1. 普通边 (无条件):
   ```python
   workflow.add_edge("from_node", "to_node")
   ```

2. 条件边 (需要路由函数):
   ```python
   workflow.add_conditional_edges(
       "from_node",
       route_function_name,
       {"target_node": "target_node", END: END}
   )
   ```

#### 路由函数说明
需要在以下情况添加路由函数:
1. 存在分支 (一个节点有多个出边)
2. 需要在状态中增加变量 (从 ToolMessage 中提取数据)

#### 路由函数示例
```python
def route_after_node_name(state: AgentState) -> str:
    """路由函数 - 从 state["messages"] 提取 ToolMessage 并决定路由"""
    for msg in state["messages"]:
        if hasattr(msg, "tool_call_id") and hasattr(msg, "content"):
            tool_name = getattr(msg, "name", None)
            tool_content = msg.content
            # 将提取的信息存入模块状态
            state["模块名"]["字段名"] = tool_content
            # 根据工具名称决定路由
            if tool_name == "xxx_response":
                return "target_node"
    return "default_node"
```

#### 思考节点说明
- 思考节点属于 LLM 节点的一部分
- 每个 LLM 节点前都有一个思考节点
- 思考节点使用 `think_{node_name}_response` 工具进行思考
- 思考完成后通过路由函数路由到目标 LLM 节点
- 可以选择不加入思考节点

#### LLM 节点的工具调用
每个 LLM 节点都伴随后续的工具调用:
1. 工具节点: 调用实际的工具函数 (如 websearchtool)
2. 响应工具: 返回 LLM 的最终响应
可以选择不加入响应节点,直接将LLM的输出作为最终响应

示例流程:
```
START -> think_{node_name}(可选) -> {node_name} -> tools/{node_name}_response(可选) -> END
```

### 七、模块间数据传递 (main.py)

#### 数据传递方式
将需要传递的数据存入 state 的某个属性中

#### 示例
```python
# 在模块A中将数据存入状态
state["modulea"]["output_field"] = value

# 在模块B中从状态读取数据
module_a_output = state.get("modulea", {}).get("output_field", "")
```

#### 状态管理原则
1. 每个模块有独立的状态空间
2. 模块间通过状态读写进行数据传递
3. 确保前序模块的输出字段与后续模块的输入字段对应

### 八、常见问题

#### API 密钥配置
- 确保在 `.env` 文件中设置了 `LLM_API_KEY`
- 或设置环境变量 `LLM_API_KEY`

#### 工具调用失败
- 检查工具函数是否正确实现
- 确保工具返回字符串类型
- 查看错误日志定位问题

#### 状态管理问题
- 确保状态字段名称正确
- 检查模块状态是否正确定义
- 使用正确的状态读写方式
