from app.prompt_builder import build_study_material_prompt
from app.services.ai_service import MockAIService
from app.study_options import get_study_options

MAX_EXTRACTED_TEXT_LENGTH = 40000

INVALID_EXTRACTED_TEXT_MESSAGES = {
    "未提取到文本内容",
    "PDF 文件无法解析，请确认文件未损坏或未加密。",
}


class StudyMaterialError(Exception):
    """Base error for study material generation."""


class InvalidStudyTextError(StudyMaterialError):
    """Raised when extracted PDF text cannot be used."""


class StudyTextTooLongError(StudyMaterialError):
    """Raised when extracted text exceeds the current limit."""


def generate_study_materials(
    extracted_text,
    selected_options,
    ai_service=None,
):
    """Generate and validate study materials using the configured service."""
    if (
        not isinstance(extracted_text, str)
        or not extracted_text.strip()
        or extracted_text.strip() in INVALID_EXTRACTED_TEXT_MESSAGES
    ):
        raise InvalidStudyTextError(
            "PDF 未提取到有效文本，无法生成复习资料。"
        )

    if len(extracted_text) > MAX_EXTRACTED_TEXT_LENGTH:
        raise StudyTextTooLongError(
            "PDF 文本超过 40000 字符，暂时无法生成复习资料。"
        )

    option_values = [
        option.get("value")
        for option in selected_options
        if isinstance(option, dict)
    ]
    valid_options = get_study_options(option_values)
    if not valid_options:
        return []

    prompt = build_study_material_prompt(extracted_text, valid_options)
    service = ai_service or MockAIService()

    try:
        response = service.generate(prompt, valid_options)
    except Exception as error:
        raise StudyMaterialError("复习资料生成失败，请稍后重试。") from error

    if not isinstance(response, dict):
        raise StudyMaterialError("复习资料生成结果格式无效。")

    materials = response.get("materials")
    if not isinstance(materials, list):
        raise StudyMaterialError("复习资料生成结果格式无效。")

    options_by_value = {
        option["value"]: option for option in valid_options
    }
    materials_by_type = {}
    for material in materials:
        if not isinstance(material, dict):
            continue

        material_type = material.get("type")
        content = material.get("content_markdown")
        if (
            material_type not in options_by_value
            or not isinstance(content, str)
            or not content.strip()
        ):
            continue

        option = options_by_value[material_type]
        materials_by_type[material_type] = {
            "type": material_type,
            "title": option["label"],
            "content_markdown": content.strip(),
        }

    return [
        materials_by_type[option["value"]]
        for option in valid_options
        if option["value"] in materials_by_type
    ]
