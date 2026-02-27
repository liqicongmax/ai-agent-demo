import os

def read_file(file_path):
    """
    读取单个文件的内容
    
    参数:
        file_path (str): 文件路径
    
    返回值:
        str: 文件内容
    
    异常:
        FileNotFoundError: 文件不存在
        PermissionError: 权限不足
        IOError: 其他IO异常
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"错误: 文件不存在: {file_path}")
        raise
    except PermissionError:
        print(f"错误: 权限不足: {file_path}")
        raise
    except IOError as e:
        print(f"错误: 读取文件时发生IO错误: {e}")
        raise

def list_files(directory=None):
    """
    列出指定目录下的所有文件和子目录
    
    参数:
        directory (str, 可选): 目录路径，默认为当前工作目录
    
    返回值:
        list: 包含文件名/目录名的列表
    
    异常:
        FileNotFoundError: 目录不存在
        PermissionError: 权限不足
        NotADirectoryError: 指定路径不是目录
    """
    try:
        if directory is None:
            directory = os.getcwd()
        items = os.listdir(directory)
        return items
    except FileNotFoundError:
        print(f"错误: 目录不存在: {directory}")
        raise
    except PermissionError:
        print(f"错误: 权限不足: {directory}")
        raise
    except NotADirectoryError:
        print(f"错误: 指定路径不是目录: {directory}")
        raise

def rename_file(old_path, new_name):
    """
    重命名指定文件
    
    参数:
        old_path (str): 原文件路径
        new_name (str): 新文件名
    
    返回值:
        bool: 操作成功状态
    
    异常:
        FileNotFoundError: 原文件不存在
        FileExistsError: 目标文件已存在
        PermissionError: 权限不足
        IOError: 其他IO异常
    """
    try:
        # 获取原文件所在目录
        directory = os.path.dirname(old_path)
        if directory == '':
            directory = os.getcwd()
        # 构建新文件路径
        new_path = os.path.join(directory, new_name)
        # 执行重命名操作
        os.rename(old_path, new_path)
        return True
    except FileNotFoundError:
        print(f"错误: 原文件不存在: {old_path}")
        raise
    except FileExistsError:
        print(f"错误: 目标文件已存在: {new_path}")
        raise
    except PermissionError:
        print(f"错误: 权限不足")
        raise
    except IOError as e:
        print(f"错误: 重命名文件时发生IO错误: {e}")
        raise
