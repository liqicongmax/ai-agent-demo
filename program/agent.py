from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
import tools
import os

def main():
    """
    主函数：通过pydantic-ai接入OpenAI实现AI Agent
    """
    # 配置OpenAI API
    # 注意：实际使用时请替换为真实的API密钥
    openai_api_key = 'zzzzzz'
    
    # 手动配置OpenAI的URL（可选，如果不设置则使用默认的OpenAI URL）
    openai_base_url = 'https://ark.cn-beijing.volces.com/api/coding/v3'
    
    # 设置环境变量，确保OpenAIProvider能够找到API密钥
    os.environ['OPENAI_API_KEY'] = openai_api_key
    
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
        tools=[tools.list_files, tools.read_file, tools.rename_file]
    )
    
    # 测试对话
    print("AI助手已启动，输入'退出'结束对话")
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
