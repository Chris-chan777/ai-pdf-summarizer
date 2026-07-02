"""AI PDF Summarizer —— 项目入口

使用方式：
    python run.py

然后在浏览器访问 http://127.0.0.1:5000
"""

from app import create_app

# 调用工厂函数，获得已配置好的 Flask 应用实例
app = create_app()

if __name__ == "__main__":
    # debug=True  → 代码修改后自动重载，同时提供调试页面
    # port=5000   → 默认端口，可自行修改
    app.run(debug=True, port=5000)
