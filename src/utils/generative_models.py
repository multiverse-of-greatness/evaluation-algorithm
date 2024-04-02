from src.generative_models.google_model import GoogleModel
from src.generative_models.llm import LLM
from src.generative_models.local_model import LocalModel
from src.generative_models.openai_model import OpenAIModel


def get_generation_model(model_name: str) -> LLM:
    if model_name in ["gemini-1.0-pro-001"]:
        return GoogleModel(model_name)
    elif model_name in ["gpt-3.5-turbo-0125", "gpt-4-turbo-preview"]:
        return OpenAIModel(model_name)
    else:
        return LocalModel(model_name)
