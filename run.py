"""AI PDF Summarizer - 项目入口

使用方式：
    python run.py

然后在浏览器访问 http://127.0.0.1:5000
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=5000)
