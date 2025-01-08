from metrics.quality_metrics import calculate_bleu_meteor_score, calculate_bert_score
from time import time

def evaluate_translation(result: str, ref_text: str, tgt_lang, elapsed_time: float, active_metrics: list):
    """
    Evaluates translation quality and performance based on the active metrics.

    Parameters:
        result (str): Translated text.
        ref_text (str): Reference text for evaluation.
        elapsed_time (float): Time taken for translation.
        active_metrics (list): List of active metrics (e.g., ["BLEU", "METEOR", "TPS"]).

    Returns:
        dict: A dictionary containing only the enabled metrics and their values.
    """
    metrics = {}

    # Calculate BLEU and METEOR if enabled
    if "BLEU" in active_metrics or "METEOR" in active_metrics:
        try:
            bleu, meteor, num_tokens = calculate_bleu_meteor_score(ref_text, result, tgt_lang)
            if "BLEU" in active_metrics:
                metrics["BLEU"] = bleu
            if "METEOR" in active_metrics:
                metrics["METEOR"] = meteor
            if "tps" in active_metrics:
                metrics["tps"] = num_tokens / elapsed_time if elapsed_time > 0 else 0.0
        except Exception as e:
            print(f"Error calculating BLEU/METEOR: {e}")
            if "BLEU" in active_metrics:
                metrics["BLEU"] = 0.0
            if "METEOR" in active_metrics:
                metrics["METEOR"] = 0.0
            if "tps" in active_metrics:
                metrics["tps"] = 0.0

    # Calculate BERTScore if enabled
    if "BERTScore" in active_metrics:
        try:
            bert_score = calculate_bert_score(ref_text, result, tgt_lang, device="cuda")
            metrics["BERTScore"] = bert_score
        except Exception as e:
            print(f"Error calculating BERTScore: {e}")
            metrics["BERTScore"] = 0.0

    return metrics