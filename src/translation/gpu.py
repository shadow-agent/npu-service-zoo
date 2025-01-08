from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate

# Global instances for LLM and Prompt
gpu_llm = None
translation_prompt = None


def initialize_gpu_llm(llm_model: str = "llama3.1", 
                       temperature: float = 0, 
                       request_timeout: int = 600, 
                       max_tokens: int = 200):
    """
    Initializes the GPU-based LLM and the prompt template globally.
    """
    global gpu_llm, translation_prompt

    if gpu_llm is None:
        gpu_llm = Ollama(
            model=llm_model, 
            temperature=temperature, 
            request_timeout=request_timeout, 
            max_tokens=max_tokens
        )

    if translation_prompt is None:
        translation_prompt = PromptTemplate(
            template="""This is an {source_lang} to {target_lang} translation, please provide a single {target_lang} translation for this text in as polite a tone as possible. Do not provide any explanations or text apart from the translation. 
The translation result must be written in {target_lang}.

{source_lang}: {source_text}

{target_lang}:
"""
        )


def translate_with_gpu(source_text: str, 
                       source_lang: str = "Korean", 
                       target_lang: str = "English", llm_model: str = "llama3.1") -> str:
    """
    Translates text using the GPU-based LLM.

    Parameters:
        source_text (str): The text to translate.
        source_lang (str): Source language.
        target_lang (str): Target language.

    Returns:
        str: Translated text.
    """
    if gpu_llm is None or translation_prompt is None:
        initialize_gpu_llm(llm_model=llm_model)

    # Format the prompt and generate the translation
    full_prompt = translation_prompt.format(
        source_lang=source_lang, 
        target_lang=target_lang, 
        source_text=source_text
    )
    return gpu_llm.complete(full_prompt).text


def main():
    """
    Main function to execute translation using translate_with_gpu.
    """
    test_text = "안녕하세요, 우주는 얼마나 넓나요?"
    print(f"Original Text: {test_text}")
    
    try:
        # Perform translation
        translated_text = translate_with_gpu(test_text)
        print(f"Translated Text: {translated_text}")
    except Exception as e:
        print(f"An error occurred during translation: {e}")


if __name__ == "__main__":
    main()