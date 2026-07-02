STUDY_OPTIONS = (
    {
        "value": "core_summary",
        "label": "核心知识点总结",
        "preview": "这里将根据 PDF 内容生成核心知识点总结。",
        "prompt_instruction": "提炼文档中的核心概念、定义、关系和结论。",
        "default": True,
    },
    {
        "value": "exam_focus",
        "label": "考试重点整理",
        "preview": "这里将根据 PDF 内容整理考试重点。",
        "prompt_instruction": "整理可能用于考试的重点内容和关键细节。",
        "default": True,
    },
    {
        "value": "concept_explanation",
        "label": "名词解释 / 概念解释",
        "preview": "这里将根据 PDF 内容生成重要概念解释。",
        "prompt_instruction": "选择重要名词和概念，并给出清晰解释。",
        "default": False,
    },
    {
        "value": "multiple_choice",
        "label": "选择题练习",
        "preview": "这里将根据 PDF 内容生成选择题练习。",
        "prompt_instruction": "生成选择题练习，并提供答案与简要解析。",
        "default": False,
    },
    {
        "value": "short_answer",
        "label": "简答题练习",
        "preview": "这里将根据 PDF 内容生成简答题练习。",
        "prompt_instruction": "生成简答题练习，并提供参考答案。",
        "default": False,
    },
    {
        "value": "quick_review",
        "label": "考前速记版",
        "preview": "这里将根据 PDF 内容生成考前速记版。",
        "prompt_instruction": "压缩整理为适合考前快速浏览的速记内容。",
        "default": False,
    },
)

STUDY_OPTIONS_BY_VALUE = {
    option["value"]: option for option in STUDY_OPTIONS
}


def get_study_options(values):
    """Return valid options in their configured order."""
    selected_values = set(values)
    return [
        option
        for option in STUDY_OPTIONS
        if option["value"] in selected_values
    ]
