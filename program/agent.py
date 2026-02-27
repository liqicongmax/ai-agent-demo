from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
import tools
import os
from dotenv import load_dotenv

def main():
    """
    主函数：通过pydantic-ai接入OpenAI实现AI Agent
    """
    # 加载.env文件
    load_dotenv()
    
    # 从环境变量获取OpenAI API配置
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai_base_url = os.getenv('OPENAI_BASE_URL')
    
    # 验证配置
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY未设置，请在.env文件中配置")
    if not openai_base_url:
        raise ValueError("OPENAI_BASE_URL未设置，请在.env文件中配置")
    
    # 创建OpenAI Provider
    openai_provider = OpenAIProvider(
        api_key=openai_api_key,
        base_url=openai_base_url
    )
    
    # 创建OpenAI模型实例
    model = OpenAIChatModel(
        model_name='glm-4.7',
        provider=openai_provider
    )
    
    # 创建Agent实例，使用自定义的模型
    agent = Agent(
        model=model,
        system_prompt='你是一个智能助手，你可以执行以下任务：\n11. 列出当前目录下的所有文件\n2. 读取文件内容\n3. 重命名文件\n',
        tools=[tools.list_files, tools.read_file, tools.rename_file]
    )
    
    # 测试对话
    print("AI助手已启动,输入'退出'结束对话")
    while True:
        user_input = input("用户: ")
        if user_input == '退出':
            break
        
        try:
            # 同步运行Agent
            result = agent.run_sync(user_input)
            print(f"AI: {result.output}")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    main()
