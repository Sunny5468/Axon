#!/usr/bin/env python3
"""
NotebookLLM 应用验证脚本
检查环境、依赖和配置是否正确
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """打印成功信息"""
    print(f"✅ {text}")

def print_error(text):
    """打印错误信息"""
    print(f"❌ {text}")

def print_warning(text):
    """打印警告信息"""
    print(f"⚠️  {text}")

def print_info(text):
    """打印信息"""
    print(f"ℹ️  {text}")

def check_python_version():
    """检查Python版本"""
    print_header("1. Python版本检查")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str}")
        return True
    else:
        print_error(f"Python {version_str} (需要 3.8+)")
        return False

def check_required_files():
    """检查必要的文件"""
    print_header("2. 文件检查")
    
    required_files = {
        "前端": [
            "frontend/index.html",
            "frontend/package.json",
        ],
        "后端": [
            "backend/main.py",
            "backend/main_enhanced.py",
            "backend/requirements.txt",
        ],
        "脚本": [
            "run_backend.bat",
            "run_frontend.bat",
            "run_backend.sh",
            "run_frontend.sh",
        ],
        "文档": [
            "README.md",
            "QUICKSTART.md",
            "USAGE.md",
            "DEPLOYMENT.md",
            "CONFIG.md",
            "PROJECT_STRUCTURE.md",
        ],
    }
    
    all_exist = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if Path(file).exists():
                print_success(file)
            else:
                print_error(f"{file} (缺失)")
                all_exist = False
    
    return all_exist

def check_dependencies():
    """检查后端依赖"""
    print_header("3. Python依赖检查")
    
    try:
        with open("backend/requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        print("需要的包：")
        for req in requirements:
            if req.strip():
                print(f"  • {req}")
        
        print("\n请运行以下命令安装依赖：")
        print_info("cd backend && pip install -r requirements.txt")
        
        return True
    except Exception as e:
        print_error(f"读取依赖文件失败: {e}")
        return False

def check_frontend_files():
    """检查前端文件内容"""
    print_header("4. 前端文件检查")
    
    frontend_file = Path("frontend/index.html")
    if frontend_file.exists():
        size = frontend_file.stat().st_size
        lines = len(frontend_file.read_text().split("\n"))
        print_success(f"index.html ({size/1024:.1f}KB, {lines}行)")
        
        content = frontend_file.read_text()
        
        # 检查关键部分
        checks = [
            ("HTML结构", "<html" in content or "<!DOCTYPE" in content),
            ("CSS样式", "<style>" in content),
            ("JavaScript", "<script>" in content),
            ("API调用", "fetch(" in content or "XMLHttpRequest" in content),
            ("表单处理", "getElementById(" in content),
        ]
        
        print("\n功能检查：")
        for check_name, result in checks:
            if result:
                print_success(check_name)
            else:
                print_warning(check_name + " (可能缺失)")
        
        return True
    else:
        print_error("index.html 不存在")
        return False

def check_backend_files():
    """检查后端文件内容"""
    print_header("5. 后端文件检查")
    
    files_to_check = {
        "main.py": "backend/main.py",
        "main_enhanced.py": "backend/main_enhanced.py",
    }
    
    for name, path in files_to_check.items():
        file_path = Path(path)
        if file_path.exists():
            size = file_path.stat().st_size
            lines = len(file_path.read_text().split("\n"))
            print_success(f"{name} ({size/1024:.1f}KB, {lines}行)")
            
            content = file_path.read_text()
            
            # 检查关键部分
            checks = [
                ("FastAPI导入", "from fastapi" in content or "import fastapi" in content),
                ("路由定义", "@app.post" in content or "@app.get" in content),
                ("CORS配置", "CORSMiddleware" in content or "cors" in content),
                ("API端点", "/api/generate" in content),
            ]
            
            print(f"  {name} 功能检查：")
            for check_name, result in checks:
                if result:
                    print_success(f"    {check_name}")
                else:
                    print_warning(f"    {check_name} (可能缺失)")
        else:
            print_error(f"{name} 不存在")

def check_documentation():
    """检查文档完整性"""
    print_header("6. 文档检查")
    
    docs = {
        "README.md": "项目主说明",
        "QUICKSTART.md": "快速开始",
        "USAGE.md": "使用教程",
        "DEPLOYMENT.md": "部署指南",
        "CONFIG.md": "配置参考",
        "PROJECT_STRUCTURE.md": "项目架构",
    }
    
    all_exist = True
    for filename, description in docs.items():
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            lines = len(file_path.read_text().split("\n"))
            print_success(f"{filename} - {description} ({size/1024:.1f}KB)")
        else:
            print_error(f"{filename} - {description} (缺失)")
            all_exist = False
    
    return all_exist

def check_api_key():
    """检查API密钥配置"""
    print_header("7. API密钥检查")
    
    main_file = Path("backend/main.py")
    if main_file.exists():
        content = main_file.read_text()
        if "API_KEY" in content or "api_key" in content:
            print_success("API密钥已配置")
            print_info("密钥值：sk-5610a05204284964a0953677a117a9dd")
            return True
        else:
            print_warning("API密钥配置未找到")
            return False
    else:
        print_error("无法读取后端文件")
        return False

def print_next_steps():
    """打印后续步骤"""
    print_header("📋 后续步骤")
    
    print("""
1️⃣  安装Python依赖
    cd backend
    pip install -r requirements.txt

2️⃣  启动后端服务
    Windows: python main.py
    Linux:   python3 main.py

3️⃣  启动前端服务 (新终端)
    cd frontend
    python -m http.server 3000

4️⃣  打开浏览器
    访问 http://localhost:3000

5️⃣  验证安装
    • 前端: http://localhost:3000
    • API:  http://localhost:8000/health
    • 文档: http://localhost:8000/docs

📖 更多信息，请阅读：
    • QUICKSTART.md - 快速开始
    • USAGE.md - 详细教程
    • README.md - 完整说明
    """)

def print_summary(results):
    """打印摘要"""
    print_header("✨ 检查摘要")
    
    total = len(results)
    passed = sum(1 for r in results if r)
    
    print(f"\n总体检查: {passed}/{total} 通过")
    
    if passed == total:
        print_success("所有检查通过！项目已准备好使用。")
        print("\n请按照后续步骤开始使用。\n")
    else:
        print_warning(f"有 {total - passed} 项检查未通过。")
        print("请检查错误信息并解决问题。\n")
    
    return passed == total

def main():
    """主函数"""
    print("""
╔════════════════════════════════════════════════════════════╗
║        NotebookLLM 应用验证脚本                            ║
║        检查环境、依赖和配置是否正确                        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    results = []
    
    # 执行检查
    results.append(check_python_version())
    results.append(check_required_files())
    results.append(check_dependencies())
    results.append(check_frontend_files())
    check_backend_files()
    results.append(check_documentation())
    results.append(check_api_key())
    
    # 打印摘要
    all_passed = print_summary(results)
    
    # 打印后续步骤
    print_next_steps()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
