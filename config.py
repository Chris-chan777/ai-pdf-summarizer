import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_int_env(name, default):
    """Read an integer environment variable with a safe default."""
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


class Config:
    """应用基础配置"""
    # --- 密钥 ---
    # Flask 用于 CSRF 保护、Session 签名的密钥。
    # 生产环境务必改为真实随机字符串（可用 os.urandom(24).hex() 生成）。
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"

    # --- 上传目录 ---
    # 获取本文件 (config.py) 所在目录的绝对路径，作为项目根目录。
    BASE_DIR = BASE_DIR

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

    # --- AI 服务配置 ---
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "mock")
    AI_API_KEY = os.environ.get("AI_API_KEY", "")
    AI_MODEL = os.environ.get("AI_MODEL", "mock-model")
    AI_MAX_INPUT_CHARS = get_int_env("AI_MAX_INPUT_CHARS", 40000)
    AI_MAX_OUTPUT_TOKENS = get_int_env("AI_MAX_OUTPUT_TOKENS", 4000)
    AI_TIMEOUT_SECONDS = get_int_env("AI_TIMEOUT_SECONDS", 60)
