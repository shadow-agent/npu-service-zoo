import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from bert_score import score
from nltk.tokenize import word_tokenize
from janome.tokenizer import Tokenizer
from kiwipiepy import Kiwi
from nltk.translate.meteor_score import meteor_score


def tokenize(text, lang):
    if lang == "English":
        # 영어: NLTK word_tokenize
        return word_tokenize(text)
    elif lang == "Korean":
        # 한국어: Kiwi 형태소 분석기
        kiwi = Kiwi()
        tokens = kiwi.tokenize(text)
        return [token.form for token in tokens]  # 형태소만 추출
    elif lang == "Japanese":
        # 일본어: Janome 형태소 분석기
        tokenizer = Tokenizer()
        return [token.surface for token in tokenizer.tokenize(text)]
    else:
        raise ValueError(f"Unsupported language: {lang}")
    
    
def calculate_bleu_meteor_score(reference: str, candidate: str, tgt_lang: str = "English"):
    """
    Calculates BLEU and METEOR scores between a reference and a candidate translation.

    Parameters:
        reference (str): The reference (ground truth) text.
        candidate (str): The candidate (generated) translation.
        tgt_lang (str): Target language for tokenization (default: "English").

    Returns:
        tuple: BLEU score, METEOR score, and number of tokens.
    """
    try:
        # 텍스트를 토큰화
        reference_tokens = tokenize(reference, tgt_lang)
        candidate_tokens = tokenize(candidate, tgt_lang)
        smoothing_function = SmoothingFunction().method1
        num_tokens = len(candidate_tokens)

        # BLEU 지표 계산
        bleu = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing_function)

        # METEOR 지표 계산
        meteor = meteor_score([reference_tokens], candidate_tokens)

        # 모든 값을 반환
        return round(bleu, 4), round(meteor, 4), num_tokens

    except Exception as e:
        print(f"Error in calculate_bleu_meteor_score: {e}")
        # 기본값 반환 (0, 0, 0) 에러 상황 처리
        return 0.0, 0.0, 0


def calculate_bert_score(reference: str, candidate: str, tgt_lang: str = "English", device: str = "cuda") -> float:
    """
    Calculates BERTScore between a reference and a candidate translation.

    Parameters:
        reference (str): The reference (ground truth) text.
        candidate (str): The candidate (generated) translation.
        tgt_lang (str): Target language name (e.g., "English", "Korean", "Japanese").
        device (str): Device for computation ("cuda" for GPU, "cpu" for CPU).

    Returns:
        float: BERTScore (F1 score).

    Raises:
        ValueError: If the provided language is not supported.
    """
    # Best bert model (@2024.12.30)
    bert_model="microsoft/deberta-xlarge-mnli"
    
    # Map target language to ISO code
    lang_map = {
        "English": "en",
        "Korean": "ko",
        "Japanese": "ja",
    }
    
    if tgt_lang not in lang_map:
        raise ValueError(f"Unsupported language '{tgt_lang}'. Supported languages are: {list(lang_map.keys())}")
    
    # Get ISO code
    lang = lang_map[tgt_lang]
    
    # Calculate BERTScore
    P, R, F1 = score([candidate], [reference], lang=lang, model_type=bert_model, device=device)
    return round(F1.item(), 4)