from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.tools import RunContext
import tools
import os
from dotenv import load_dotenv
from pathlib import Path

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
        # system_prompt='你是一个智能助手，你可以执行以下任务：\n1. 列出当前目录下的所有文件\n2. 读取文件内容\n3. 重命名文件\n4. 搜索文件（支持递归搜索，使用search_files工具）\n5. 获取项目根目录\n\n重要提示：\n- 当用户要求查看某个目录或文件夹时，请使用enhanced_list_files工具，它会自动处理相对路径\n- 当用户要求搜索文件时，请使用search_files工具，支持递归搜索和通配符\n- 如果路径是相对路径，工具会自动处理从program目录向上查找的问题\n',
        # tools=[tools.list_files, tools.read_file, tools.rename_file]
    )
    
    # 添加增强的文件搜索工具
    @agent.tool
    def search_files(ctx: RunContext, search_path: str, pattern: str = None, recursive: bool = True) -> list:
        """
        搜索指定路径下的文件
        
        参数:
            ctx: 运行上下文
            search_path (str): 搜索路径，支持相对路径和绝对路径
            pattern (str, 可选): 文件名匹配模式，支持通配符，如*.py
            recursive (bool, 可选): 是否递归搜索子目录，默认为True
        
        返回值:
            list: 找到的文件路径列表
        
        异常:
            FileNotFoundError: 搜索路径不存在
            PermissionError: 权限不足
        """
        try:
            # 处理相对路径，如果从program目录运行，需要向上查找
            if not os.path.isabs(search_path):
                # 获取当前工作目录
                current_dir = os.getcwd()
                # 如果在program目录下，向上查找
                if os.path.basename(current_dir) == 'program':
                    search_path = os.path.join(os.path.dirname(current_dir), search_path)
                else:
                    search_path = os.path.join(current_dir, search_path)
            
            # 确保路径存在
            if not os.path.exists(search_path):
                return [f"错误: 路径不存在: {search_path}"]
            
            # 搜索文件
            if recursive:
                # 递归搜索
                if pattern:
                    files = list(Path(search_path).rglob(pattern))
                else:
                    files = list(Path(search_path).rglob('*'))
            else:
                # 非递归搜索
                if pattern:
                    files = list(Path(search_path).glob(pattern))
                else:
                    files = list(Path(search_path).glob('*'))
            
            # 转换为字符串并过滤目录
            result = [str(f) for f in files if f.is_file()]
            return result
            
        except FileNotFoundError:
            return [f"错误: 路径不存在: {search_path}"]
        except PermissionError:
            return [f"错误: 权限不足: {search_path}"]
        except Exception as e:
            return [f"错误: 搜索文件时发生异常: {e}"]
    
    @agent.tool
    def get_project_root(ctx: RunContext) -> str:
        """
        获取项目根目录
        
        参数:
            ctx: 运行上下文
        
        返回值:
            str: 项目根目录的绝对路径
        """
        current_dir = os.getcwd()
        # 如果在program目录下，返回上级目录
        if os.path.basename(current_dir) == 'program':
            return os.path.dirname(current_dir)
        return current_dir
    
    @agent.tool
    def enhanced_list_files(ctx: RunContext, directory: str = None) -> list:
        """
        增强的列表文件功能，支持绝对路径
        
        参数:
            ctx: 运行上下文
            directory (str, 可选): 目录路径，支持相对路径和绝对路径
        
        返回值:
            list: 包含文件名/目录名的列表
        
        异常:
            FileNotFoundError: 目录不存在
            PermissionError: 权限不足
        """
        try:
            # 处理相对路径
            if directory and not os.path.isabs(directory):
                current_dir = os.getcwd()
                if os.path.basename(current_dir) == 'program':
                    directory = os.path.join(os.path.dirname(current_dir), directory)
                else:
                    directory = os.path.join(current_dir, directory)
            
            # 如果未指定目录，使用当前工作目录
            if not directory:
                directory = os.getcwd()
            
            # 列出文件
            items = os.listdir(directory)
            return items
            
        except FileNotFoundError:
            return [f"错误: 目录不存在: {directory}"]
        except PermissionError:
            return [f"错误: 权限不足: {directory}"]
        except Exception as e:
            return [f"错误: 列出文件时发生异常: {e}"]
    
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
