"""
配置模块

本模块集中管理所有配置信息，包括：
1. LLM 模型配置
2. API 密钥管理
3. 模型参数设置

使用方法:
    from config import get_llm
    llm = get_llm()
"""

import os
from langchain_openai import ChatOpenAI


# 加载 .env 文件中的环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[config] 已加载 .env 文件")
except ImportError:
    print("[config] 未安装 python-dotenv，跳过 .env 文件加载")
except Exception as e:
    print(f"[config] 加载 .env 文件失败: {e}")


def get_llm():
    """获取 LLM 模型实例

    使用环境变量配置的 API 信息

    环境变量说明:
    - LLM_API_KEY / OPENAI_API_KEY: API 密钥 (二选一)
    - LLM_URL: API 端点 (默认: https://api.openai.com/v1)
    - LLM_MODEL: 模型名称 (默认: gpt-4o-mini)
    - USE_OLLAMA: 是否使用 Ollama (设为 true 时启用)
    - OLLAMA_MODEL: Ollama 模型名称
    - OLLAMA_BASE_URL: Ollama 服务地址
    """
    # 从环境变量获取 API 配置
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("LLM_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # 检查 API 密钥是否设置
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise ValueError(
            "API 密钥未设置！请设置以下环境变量之一:\n"
            "  - LLM_API_KEY\n"
            "  - OPENAI_API_KEY\n"
            "或者修改 .env 文件中的 API 密钥"
        )

    print(f"[get_llm] 正在初始化 LLM...")
    print(f"[get_llm] 模型: {model}")
    print(f"[get_llm] API 端点: {base_url}")

    # 使用 OpenAI API，添加超时设置
    return ChatOpenAI(
        model=model,
        temperature=0.7,
        api_key=api_key,
        base_url=base_url,
        timeout=60,  # 设置 60 秒超时
        max_retries=2  # 设置最大重试次数
        
    )
