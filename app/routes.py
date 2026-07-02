import os

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

# ---------------------------------------------------------------
# 创建蓝图
# ---------------------------------------------------------------
# Blueprint 是 Flask 中组织路由的容器。
# 参数说明：
#   "main"  → 蓝图名称，Flask 内部用于 URL 生成和调试
#   __name__ → 模块名，Flask 用它定位此蓝图所属的包（app/）
# 后续在 __init__.py 中通过 register_blueprint() 注册生效。
main_bp = Blueprint("main", __name__)


# ---------------------------------------------------------------
# 首页路由
# ---------------------------------------------------------------
@main_bp.route("/")
def index():
    """首页 —— 展示 PDF 上传表单"""
    # render_template() 去 templates/ 目录找 index.html，
    # 用 Jinja2 引擎渲染后返回 HTML 响应给浏览器。
    return render_template("index.html")


@main_bp.route("/upload", methods=["POST"])
def upload():
    """Validate and save an uploaded PDF file."""
    pdf_file = request.files["pdf_file"]

    if not pdf_file or not pdf_file.filename:
        return "No file selected", 400

    if not pdf_file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed", 400

    filename = secure_filename(pdf_file.filename)
    if not filename:
        return "Invalid filename", 400

    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    pdf_file.save(save_path)

    return render_template("result.html", filename=filename)
