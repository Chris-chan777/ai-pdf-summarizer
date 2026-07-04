STUDY_OPTIONS = (
    {
        "value": "document_summary",
        "label": "AI 结构化总结",
        "preview": "生成核心主题、主要内容、关键结论和关键词。",
        "prompt_instruction": "严格按固定四段式结构总结文档。",
        "default": True,
    },
)


def get_study_options(values):
    """保留兼容接口，仅返回固定的结构化总结选项。"""
    return list(STUDY_OPTIONS)
