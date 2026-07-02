import os
from uuid import uuid4

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

from app.utils.pdf_utils import extract_text_from_pdf

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
    pdf_file = request.files.get("pdf_file")
    study_options = request.form.getlist("study_options")

    if pdf_file is None:
        return render_template(
            "error.html",
            message="未找到上传文件，请返回首页重新选择。",
        ), 400

    if not pdf_file.filename:
        return render_template(
            "error.html",
            message="请选择要上传的 PDF 文件。",
        ), 400

    if not pdf_file.filename.lower().endswith(".pdf"):
        return render_template(
            "error.html",
            message="仅支持上传 PDF 文件。",
        ), 400

    original_filename = pdf_file.filename
    safe_filename = secure_filename(original_filename)
    if not safe_filename:
        return render_template(
            "error.html",
            message="文件名无效，请重新选择文件。",
        ), 400

    saved_filename = f"{uuid4().hex}.pdf"
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        saved_filename,
    )
    try:
        pdf_file.save(file_path)
    except Exception:
        current_app.logger.exception("Failed to save uploaded PDF")
        return render_template(
            "error.html",
            message="文件上传失败，请稍后重试。",
        ), 500

    extracted_text = extract_text_from_pdf(file_path)

    return render_template(
        "result.html",
        original_filename=original_filename,
        saved_filename=saved_filename,
        extracted_text=extracted_text,
        study_options=study_options,
    )


@main_bp.app_errorhandler(413)
def file_too_large(error):
    """Show a friendly page when an upload exceeds the size limit."""
    return render_template(
        "error.html",
        message="上传文件过大，请选择不超过 16 MB 的 PDF 文件。",
    ), 413
