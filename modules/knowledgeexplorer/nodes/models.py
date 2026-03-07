"""
knowledgeexplorer 模块 - 工具参数模型定义
"""
from pydantic import BaseModel, Field

class nodes_generate_model(BaseModel):
    """
    
    """
    query: str = Field(description="工具输入参数")


class retrieve_input_response_model(BaseModel):
    """
     - 响应模型
    """
    start_ids:list
    end_ids:list


class think_retrieve_input_model(BaseModel):
    """
    retrieve_input 节点的思考模型 - 用于思维链推理
    """
    step_1:str = Field("开始")

    pass  # TODO: 请根据业务需求定义思考模型的字段



