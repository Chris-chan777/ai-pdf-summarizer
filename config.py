import os


class Config:
    """应用基础配置"""
    # --- 密钥 ---
    # Flask 用于 CSRF 保护、Session 签名的密钥。
    # 生产环境务必改为真实随机字符串（可用 os.urandom(24).hex() 生成）。
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"

    # --- 上传目录 ---
    # 获取本文件 (config.py) 所在目录的绝对路径，作为项目根目录。
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # 拼接出 uploads 文件夹的绝对路径，Flask 上传文件时存入此目录。
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # --- 上传限制 ---
    # 单文件最大 16 MB，可根据需要调整。
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 允许的文件扩展名（白名单）。
    ALLOWED_EXTENSIONS = {"pdf"}

    # --- 调试模式 ---
    # 从环境变量读取 DEBUG，便于开发 / 生产切换。
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
