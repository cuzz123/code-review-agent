from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
import json, os
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="deepseek-chat",
    model_provider="openai",
    openai_api_key=os.environ["DEEPSEEK_API_KEY"],
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0,
)


def clean_json(raw: str) -> str:
    """清理 LLM 返回的 JSON"""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    if raw.endswith("```"):
        raw = raw.rsplit("\n", 1)[0]
    return raw.strip()


def check_architecture(code: str, filename: str) -> list:
    """架构审查"""
    prompt = f"""你是一个代码架构审查专家。审查以下代码的架构设计。

文件名：{filename}
代码：
{code}

检查以下方面，返回 JSON 数组（每个元素包含 severity / title / description / suggestion）：
1. 是否存在职责不清晰的函数或类
2. 是否存在过度耦合
3. 命名是否合理
4. 函数是否过长

直接返回 JSON 数组，不要加任何其他文字。"""

    response = model.invoke([HumanMessage(content=prompt)])
    raw = clean_json(response.content)
    data = json.loads(raw)

    if isinstance(data, list) and data and "issues" in data[0]:
        return data[0].get("issues", [])
    if isinstance(data, list):
        return data
    return []

def check_security(code: str, filename: str) -> list:
    """安全审查"""
    prompt = f"""你是一个代码安全审查专家。审查以下代码的安全问题。
    
文件名：{filename}
代码：
{code}

检查以下方面，返回 JSON 数组（每个元素包含 severity / title / desctiption/ suggestion ）：
1. SQL 注入
2. 命令注入（shell=True, os.system等）
3. 敏感信息硬编码
4. 不安全的文件操作
5. XSS / CSRF

直接返回 JSON 数组，不要加任何其他文字。"""
    response = model.invoke([HumanMessage(content=prompt)])
    return json.loads(clean_json(response.content))

def check_performance(code: str, filename: str) -> list:
    """性能审查"""
    prompt = f"""你是一个性能优化专家。审查以下代码的性能问题。

文件名：{filename}
代码：
{code}

检查以下方面，返回 JSON 数组（每个元素包含 severity / title / description / suggestion）：
1. 不必要的循环
2. 重复计算
3. 内存泄漏风险
4. 不必要的 I/O 操作

直接返回 JSON 数组，不要加任何其他文字。"""
    response = model.invoke([HumanMessage(content=prompt)])
    return json.loads(clean_json(response.content))

def check_style(code: str, filename: str) -> list:
    prompt = f"""你是一个代码风格审查专家。审查以下代码的风格问题。

文件名：{filename}
代码：
{code}

检查以下方面，返回 JSON 数组（每个元素包含 severity / title / description / suggestion ）：
1. 命名规范（PEP8 / 驼峰 / 下划线）
2. 注释是否充分
3. 代码格式（空格、换行）
4. 未使用的导入或变量

直接返回 JSON 数组，不要加任何其他文字。"""
    response = model.invoke([HumanMessage(content=prompt)])
    return json.loads(clean_json(response.content))