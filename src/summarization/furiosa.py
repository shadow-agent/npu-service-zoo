import os
from furiosa_llm import LLM, SamplingParams

# Global instances for LLM and Sampling Parameters
furiosa_llm = None
sampling_params = None


def initialize_furiosa_llm(model_path: str = "/home/elicer/renegade/Llama-3.1-8B-Instruct",
                           devices: str = "npu:1:*", 
                           temperature: float = 0.2, 
                           max_tokens: int = 300):
    """
    Initializes the Furiosa LLM and sampling parameters globally.

    Parameters:
        model_path (str): Path to the LLM artifacts. 
        devices (str): Device string for Furiosa NPU. Default: "npu:1:*".
        temperature (float): Sampling temperature. Default: 0.2.
        max_tokens (int): Maximum number of tokens for generation. Default: 300.
    """
    global furiosa_llm, sampling_params

    if furiosa_llm is None:
        os.environ["RUST_BACKTRACE"] = "full"
        furiosa_llm = LLM.from_artifacts(model_path, devices=devices)

    if sampling_params is None:
        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)


def apply_summarization_template(source_text: str) -> str:
    """
    Creates a prompt for summarization.

    Parameters:
        source_text (str): The text to summarize.

    Returns:
        str: Formatted summarization prompt.
    """
    prompt = f"""Please summarize the following text in a concise and clear manner. 
Focus on the main points without adding any interpretation or extra information.

Text to summarize:
{source_text}

Summary:"""
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful assistant specialized in text summarization tasks.<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


def summarize_with_furiosa(source_text: str) -> str:
    """
    Summarizes text using the Furiosa-based LLM.

    Parameters:
        source_text (str): The text to summarize.

    Returns:
        str: Summarized text.
    """
    if furiosa_llm is None or sampling_params is None:
        initialize_furiosa_llm()

    # Create the summarization prompt
    prompt = apply_summarization_template(source_text)

    # Generate and return the summary
    output_txt = furiosa_llm.generate(prompt, sampling_params)
    return output_txt.outputs[0].text[2:]


def main():
    """
    Main function to execute summarization using summarize_with_furiosa.
    """
    test_text = ("인공지능 기술은 현재 빠르게 발전하고 있으며, "
                 "다양한 산업 분야에서 활용되고 있습니다. "
                 "특히 자연어 처리와 컴퓨터 비전 기술은 많은 주목을 받고 있으며, "
                 "이는 기업들이 효율성을 높이고 비용을 절감하는 데 크게 기여하고 있습니다.")
    print(f"Original Text: {test_text}")

    try:
        # Perform summarization
        summarized_text = summarize_with_furiosa(test_text)
        print(f"Summarized Text: {summarized_text}")
    except Exception as e:
        print(f"An error occurred during summarization: {e}")


if __name__ == "__main__":
    main()