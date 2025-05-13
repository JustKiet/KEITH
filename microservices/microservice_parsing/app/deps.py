from app.infrastructure.docloader.loaders import PDFLoader, SpreadsheetLoader
from app.infrastructure.docloader.parsers import ImageParser
from app.infrastructure.docloader.detectors import DoctrDetector
from app.infrastructure.docloader.recognizers import ThaiOCRRecognizer, EnglishRecognizer
from app.infrastructure.openagentkit.modules.openai import AsyncOpenAILLMService
from app.clients.openai_clients import ASYNC_OPENAI_CLIENT
from app.core.config import settings
from typing import Literal

doctr_detector = DoctrDetector()
thai_ocr_recognizer = ThaiOCRRecognizer()
eng_ocr_recognizer = EnglishRecognizer()

def get_async_llm_service() -> AsyncOpenAILLMService:
    return AsyncOpenAILLMService(
        client=ASYNC_OPENAI_CLIENT,
        model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    )

def get_pdf_loader(lang: Literal["th", "en"] = "th") -> PDFLoader:
    if lang == "en":
        # Use English model
        return PDFLoader(
            parser=ImageParser(
                detector=doctr_detector,
                recognizer=eng_ocr_recognizer
            )
        )
    elif lang == "th":
        # Use Thai model
        return PDFLoader(
            parser=ImageParser(
                detector=doctr_detector,
                recognizer=thai_ocr_recognizer
            )
        )

def get_spreadsheet_loader() -> SpreadsheetLoader:
    return SpreadsheetLoader()