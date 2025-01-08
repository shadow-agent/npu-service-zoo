from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate

# Global instances for LLM and Prompt
gpu_llm = None
summarization_prompt = None


def initialize_gpu_llm(llm_model: str = "llama3.1", 
                       temperature: float = 0.2, 
                       request_timeout: int = 600, 
                       max_tokens: int = 300):
    """
    Initializes the GPU-based LLM and the prompt template globally.
    """
    global gpu_llm, summarization_prompt

    if gpu_llm is None:
        gpu_llm = Ollama(
            model=llm_model, 
            temperature=temperature, 
            request_timeout=request_timeout, 
            max_tokens=max_tokens
        )

    if summarization_prompt is None:
        summarization_prompt = PromptTemplate(
            template="""Please summarize the following text in a concise and clear manner. The summary should focus on the main points without adding any additional interpretation or information.

Text to summarize:
{source_text}

Summary:
"""
        )


def summarize_with_gpu(source_text: str, llm_model: str = "llama3.1") -> str:
    """
    Summarizes text using the GPU-based LLM.

    Parameters:
        source_text (str): The text to summarize.

    Returns:
        str: Summarized text.
    """
    if gpu_llm is None or summarization_prompt is None:
        initialize_gpu_llm(llm_model=llm_model)

    # Format the prompt and generate the summary
    full_prompt = summarization_prompt.format(source_text=source_text)
    return gpu_llm.complete(full_prompt).text


def main():
    """
    Main function to execute summarization using summarize_with_gpu.
    """
    test_text = ("인공지능 기술은 현재 빠르게 발전하고 있으며, "
                 "다양한 산업 분야에서 활용되고 있습니다. "
                 "특히 자연어 처리와 컴퓨터 비전 기술은 많은 주목을 받고 있으며, "
                 "이는 기업들이 효율성을 높이고 비용을 절감하는 데 크게 기여하고 있습니다.")
    print(f"Original Text: {test_text}")
    
    try:
        # Perform summarization
        summarized_text = summarize_with_gpu(test_text)
        print(f"Summarized Text: {summarized_text}")
    except Exception as e:
        print(f"An error occurred during summarization: {e}")


if __name__ == "__main__":
    main()