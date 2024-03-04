from time import sleep

from google.generativeai import GenerationConfig, GenerativeModel
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from loguru import logger

from src.config import MODEL


class GoogleGenerativeAI:
    def __init__(self) -> None:
        self.model = GenerativeModel(MODEL)
        self.safety_setting = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

    def generate(self, prompt: str, temperature: float = 0) -> str:
        logger.debug("Initiated chat with Google Generative AI API.")
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=temperature
                ),
                safety_settings=self.safety_setting
            )
            logger.debug("Completed chat with Google Generative AI API.")
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            logger.error(f"Error: {e}")
            logger.info("Retrying....")
            sleep(3)
            return self.generate(prompt, temperature)
