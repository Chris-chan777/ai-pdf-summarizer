# AI PDF Summarizer

AI PDF Summarizer 是一个基于 Flask 的 PDF 文档处理 Web 应用。目前支持上传并保存 PDF 文件，为后续的文本解析与 AI 内容总结功能提供基础。

## 技术栈

- Python
- Flask
- Bootstrap 5

## 当前功能

- 通过网页选择并上传 PDF 文件
- 校验上传文件的扩展名
- 安全处理文件名并保存至本地上传目录
- 上传成功后显示文件名和结果页面

## 项目结构

```text
ai-pdf-summarizer/
├── app/
│   ├── static/          # 静态资源
│   ├── templates/       # HTML 模板
│   ├── __init__.py      # Flask 应用工厂
│   └── routes.py        # 页面与上传路由
├── uploads/             # PDF 上传目录（不纳入 Git）
├── config.py            # 应用配置
├── requirements.txt     # Python 依赖
└── run.py               # 项目启动入口
```

## 如何运行

```bash
pip install -r requirements.txt
python run.py
```

启动后访问：`http://127.0.0.1:5000`

## 未来计划

- 提取 PDF 文本内容
- 接入 AI 模型生成文档总结
