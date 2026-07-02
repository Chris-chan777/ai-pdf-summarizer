from flask import Blueprint, render_template

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
