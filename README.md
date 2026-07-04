# AI PDF Summarizer

AI PDF Summarizer 是一个基于 Flask 的 PDF 文档处理 Web 应用。用户可以上传 PDF 文件，系统会安全保存文件、提取文档文本，并在响应式结果页面中展示内容。

项目目前专注于构建清晰、可靠的 PDF 上传与文本提取流程，为后续生成 AI 复习资料奠定基础。

## 项目截图

### 首页上传页面

![首页上传页面](docs/images/home.png)

### PDF 文本提取结果页

![PDF 文本提取结果页](docs/images/result.png)

## 当前功能

- 上传并保存单个 PDF 文件
- 校验文件扩展名并安全处理文件名
- 使用 UUID 生成唯一保存文件名，避免同名文件覆盖
- 使用 PyMuPDF 提取 PDF 文本
- 处理空白、损坏、伪造或加密 PDF
- 显示原始文件名、保存文件名和提取结果
- 使用固定高度滚动区域展示长文本
- 一键复制提取文本
- 使用统一错误页面反馈上传问题
- 选择需要生成的复习资料类型
- 使用 DeepSeek API 生成结构化复习资料
- 支持 Mock AI 作为本地开发回退模式
- 已实现 Prompt 构建、真实 AI 调用和结果校验流程

## 技术栈

- Python
- Flask
- PyMuPDF
- Bootstrap 5
- HTML / CSS / JavaScript

## 项目结构

```text
ai-pdf-summarizer/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # 自定义页面样式
│   │   └── js/
│   │       └── main.js         # 复制文本交互
│   ├── templates/
│   │   ├── base.html           # 基础页面模板
│   │   ├── error.html          # 统一错误页面
│   │   ├── index.html          # PDF 上传页面
│   │   └── result.html         # 文本提取结果页面
│   ├── services/
│   │   ├── ai_service.py       # Mock AI 服务
│   │   └── study_material_service.py # 复习资料生成流程
│   ├── utils/
│   │   └── pdf_utils.py        # PDF 文本提取工具
│   ├── __init__.py             # Flask 应用工厂
│   ├── prompt_builder.py        # AI Prompt 构建
│   ├── study_options.py        # 复习资料选项配置
│   └── routes.py               # 页面与上传路由
├── docs/
│   └── images/                 # 项目截图
├── uploads/                    # 上传文件目录（不纳入 Git）
├── config.py                   # 应用配置
├── .env.example                # 未来 AI 环境变量示例
├── requirements.txt            # Python 依赖
├── run.py                      # 项目启动入口
└── README.md
```

## 运行方法

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

启动后访问：`http://127.0.0.1:5000`

## AI 环境变量

v1.0 使用 DeepSeek API 生成真实复习资料。在 Windows PowerShell 中复制环境
变量示例，然后将占位 Key 替换为自己的 DeepSeek API Key：

```powershell
Copy-Item .env.example .env
```

各变量含义：

- `AI_PROVIDER`：AI 服务类型；真实生成使用 `deepseek`，本地模拟可用 `mock`。
- `AI_API_KEY`：DeepSeek API Key；仅 Mock 模式可留空。
- `AI_MODEL`：DeepSeek 模型名称，例如 `deepseek-chat`。
- `AI_MAX_INPUT_CHARS`：允许发送给 AI 的最大文本字符数。
- `AI_MAX_OUTPUT_TOKENS`：AI 最大输出 Token 数。
- `AI_TIMEOUT_SECONDS`：AI 请求超时时间，单位为秒。

`.env` 包含敏感配置，已被 Git 忽略，禁止提交到 GitHub。未来接入真实
AI 服务后，PDF 提取文本会发送给第三方 AI 服务，请避免上传敏感资料并注意
所选服务商的隐私政策。

## AI 服务说明

- `DeepSeekAIService` 使用 DeepSeek Chat Completion API 生成真实内容。
- `MockAIService` 保留用于无网络的本地开发和测试。
- AI 调用失败时，结果页仍会显示完整 PDF 原文。
- 服务端会过滤非法资料类型，并限制发送给 AI 的文本长度。

## 版本进度

### 当前版本：v1.0

- [x] Flask 项目基础结构
- [x] Bootstrap 5 响应式页面
- [x] PDF 上传与本地保存
- [x] 上传文件名唯一化
- [x] PDF 文本提取
- [x] 异常文件处理
- [x] 长文本滚动展示
- [x] 提取文本复制
- [x] 统一错误页面
- [x] 复习资料类型选择
- [x] 复习资料预览区域
- [x] Mock AI 复习资料生成
- [x] AI 生成流程结构
- [x] AI 配置读取与服务工厂
- [x] AI 服务统一接口和异常类型
- [x] DeepSeek API 接入
- [x] DeepSeek JSON 输出解析
- [x] AI 调用失败降级展示

### 后续计划

- [ ] Markdown 导出
- [ ] 部署上线
