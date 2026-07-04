import os
from uuid import uuid4

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename

from app.services.study_material_service import (
    StudyMaterialError,
    StudyMaterialService,
)
from app.study_options import STUDY_OPTIONS
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
    return render_template("index.html", study_options=STUDY_OPTIONS)



@main_bp.route("/order")
def order():
    """接单入口——提交 PDF 并进入现有结构化处理流程。"""
    return render_template("order.html")

@main_bp.route("/upload", methods=["POST"])
def upload():
    """Validate and save an uploaded PDF file."""
    pdf_file = request.files.get("pdf_file")
    selected_study_options = list(STUDY_OPTIONS)

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
    generated_materials = []
    generation_error = None

    if selected_study_options:
        try:
            study_material_service = StudyMaterialService(
                current_app.config
            )
            generated_materials = (
                study_material_service.generate_study_materials(
                    extracted_text,
                    selected_study_options,
                )
            )
        except StudyMaterialError as error:
            generation_error = str(error)
        except Exception:
            current_app.logger.exception(
                "Unexpected study material generation failure"
            )
            generation_error = "复习资料生成失败，请稍后重试。"

    return render_template(
        "result.html",
        original_filename=original_filename,
        saved_filename=saved_filename,
        extracted_text=extracted_text,
        study_options=selected_study_options,
        generated_materials=generated_materials,
        generation_error=generation_error,
    )



@main_bp.route("/demo")
def demo():
    """展示无需上传或调用 AI 的固定示例结果。"""
    summary = {
        "core_theme": {
            "summary": "生成式人工智能正在重塑学习与知识工作的流程。",
            "explanation": "它能够快速处理大量资料，但高质量应用仍依赖清晰目标、可靠信息和人工复核。",
        },
        "main_points": [
            {
                "title": "AI 提升内容处理效率",
                "explanation": "生成式 AI 可快速完成资料归纳、内容改写和初稿生成。",
                "detail_label": "作用",
                "detail": "显著降低重复劳动，让使用者把时间投入分析与决策。",
            },
            {
                "title": "提示词决定输出质量",
                "explanation": "目标、范围和格式越具体，AI 输出通常越稳定。",
                "detail_label": "影响",
                "detail": "模糊指令容易产生遗漏、偏题或结构不一致的问题。",
            },
            {
                "title": "人工复核不可缺少",
                "explanation": "AI 生成内容可能存在事实偏差，重要结论需要结合原文核验。",
                "detail_label": "应用",
                "detail": "在论文、报告和业务资料中应建立人工审核环节。",
            },
        ],
        "key_conclusion": {
            "conclusion": "合理设定任务边界并保留人工审核，是提升 AI 使用效率与可信度的关键。",
            "significance": "这能让 AI 真正成为可靠的工作助手，而不是未经验证的信息来源。",
        },
        "keywords": [
            {"term": "生成式AI", "meaning": "能够自动生成文本等内容的人工智能技术"},
            {"term": "学习效率", "meaning": "单位时间内理解和掌握知识的效果"},
            {"term": "提示词", "meaning": "用于描述 AI 任务目标和规则的指令"},
            {"term": "知识总结", "meaning": "对资料核心信息进行提炼和重组"},
            {"term": "人工复核", "meaning": "由人员检查 AI 输出的准确性"},
            {"term": "内容可信度", "meaning": "信息真实、可靠并可验证的程度"},
        ],
    }
    return render_template(
        "demo.html",
        summary=summary,
        demo_filename="生成式人工智能与学习效率研究报告.pdf",
    )

@main_bp.app_errorhandler(413)
def file_too_large(error):
    """Show a friendly page when an upload exceeds the size limit."""
    return render_template(
        "error.html",
        message="上传文件过大，请选择不超过 16 MB 的 PDF 文件。",
    ), 413



