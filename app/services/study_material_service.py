from app.prompt_builder import build_study_material_prompt
from app.services.ai_service import AIServiceError, get_ai_service

INVALID_EXTRACTED_TEXT_MESSAGES = {
    "未提取到文本内容",
    "PDF 文件无法解析，请确认文件未损坏或未加密。",
}
DETAIL_LABELS = {"作用", "影响", "应用"}


class StudyMaterialError(Exception):
    """结构化总结生成错误。"""


class InvalidStudyTextError(StudyMaterialError):
    """PDF 文本不可用。"""


class StudyMaterialAIError(StudyMaterialError):
    """AI 服务不可用或响应格式无效。"""


class StudyMaterialService:
    def __init__(self, config):
        self.config = config
        self.max_input_chars = int(config.get("AI_MAX_INPUT_CHARS", 40000))

    def generate_study_materials(self, extracted_text, selected_options=None):
        if (
            not isinstance(extracted_text, str)
            or not extracted_text.strip()
            or extracted_text.strip() in INVALID_EXTRACTED_TEXT_MESSAGES
        ):
            raise InvalidStudyTextError("PDF 未提取到有效文本，无法生成总结。")

        prompt = build_study_material_prompt(
            extracted_text[: self.max_input_chars], selected_options
        )
        try:
            response = get_ai_service(self.config).generate(
                prompt, selected_options or []
            )
        except AIServiceError as error:
            raise StudyMaterialAIError("AI 服务尚未配置或暂时不可用。") from error
        return self._validate_summary(response)

    @staticmethod
    def _clean_text(value, error_message):
        if not isinstance(value, str) or not value.strip():
            raise StudyMaterialAIError(error_message)
        return value.strip()

    @classmethod
    def _validate_summary(cls, response):
        if not isinstance(response, dict):
            raise StudyMaterialAIError("AI 服务返回了无效的总结结果。")

        core_theme = response.get("core_theme")
        key_conclusion = response.get("key_conclusion")
        main_points = response.get("main_points")
        keywords = response.get("keywords")

        if not isinstance(core_theme, dict):
            raise StudyMaterialAIError("AI 总结的核心主题格式无效。")
        clean_theme = {
            "summary": cls._clean_text(
                core_theme.get("summary"), "AI 总结缺少核心主题。"
            ),
            "explanation": cls._clean_text(
                core_theme.get("explanation"), "AI 总结缺少主题解释。"
            ),
        }

        if not isinstance(main_points, list) or not 3 <= len(main_points) <= 6:
            raise StudyMaterialAIError("AI 总结的主要内容格式无效。")
        clean_points = []
        for point in main_points:
            if not isinstance(point, dict):
                raise StudyMaterialAIError("AI 总结包含无效要点。")
            detail_label = cls._clean_text(
                point.get("detail_label"), "AI 总结缺少要点补充标签。"
            )
            if detail_label not in DETAIL_LABELS:
                raise StudyMaterialAIError("AI 总结的要点补充标签无效。")
            clean_points.append({
                "title": cls._clean_text(
                    point.get("title"), "AI 总结缺少要点标题。"
                ),
                "explanation": cls._clean_text(
                    point.get("explanation"), "AI 总结缺少要点解释。"
                ),
                "detail_label": detail_label,
                "detail": cls._clean_text(
                    point.get("detail"), "AI 总结缺少要点补充说明。"
                ),
            })

        if not isinstance(key_conclusion, dict):
            raise StudyMaterialAIError("AI 总结的关键结论格式无效。")
        clean_conclusion = {
            "conclusion": cls._clean_text(
                key_conclusion.get("conclusion"), "AI 总结缺少关键结论。"
            ),
            "significance": cls._clean_text(
                key_conclusion.get("significance"), "AI 总结缺少现实意义。"
            ),
        }

        if not isinstance(keywords, list) or not 5 <= len(keywords) <= 8:
            raise StudyMaterialAIError("AI 总结的关键词格式无效。")
        clean_keywords = []
        for keyword in keywords:
            if not isinstance(keyword, dict):
                raise StudyMaterialAIError("AI 总结包含无效关键词。")
            clean_keywords.append({
                "term": cls._clean_text(
                    keyword.get("term"), "AI 总结缺少关键词。"
                ),
                "meaning": cls._clean_text(
                    keyword.get("meaning"), "AI 总结缺少关键词含义。"
                ),
            })

        return {
            "core_theme": clean_theme,
            "main_points": clean_points,
            "key_conclusion": clean_conclusion,
            "keywords": clean_keywords,
        }
