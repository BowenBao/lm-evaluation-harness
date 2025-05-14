import re

from typing import List, Dict

def process_results(doc: dict, results: List[str], lm_eval_result=None) -> Dict[str, int]:
    # We modified this function reffering to the following implement by Meta:
    # https://github.com/meta-llama/llama-recipes/blob/v0.0.4
    candidates = results[0]
    target = "ABCD"[doc["answer"]]

    # # Ignore content before </think> tag, if tag exists.
    # if "</think>" in candidates:
    #     candidates = candidates.split("</think>")[-1]

    # Strict exact match in box.
    # NOTE: potential false positive when model output multiple choices.
    box_matches = re.findall(
        "|".join(
            [
                r"\\boxed{\(*([A-D])\)*.*}",
                r"answer is[\* \t:]*\(*([A-D])\)*",
                r"Answer is[\* \t:]*\(*([A-D])\)*",
                r"ANSWER is[\* \t:]*\(*([A-D])\)*",
                r"answer[\* \t:]*\(*([A-D])\)*",
                r"Answer[\* \t:]*\(*([A-D])\)*",
                r"ANSWER[\* \t:]*\(*([A-D])\)*",
                # r"</think>[\s:\*]*\(([A-D])\)",
            ]
        ),
        candidates,
    )
    box_matches = [m for match in box_matches for m in match if m]
    last_boxed_match = box_matches[-1] if box_matches else None

    exact_match = int(last_boxed_match == target)
    accept_uncertain = exact_match

    if (last_boxed_match not in ["A", "B", "C", "D"]) or (not exact_match and lm_eval_result == target):
        print("--------------------")
        print(f"Subject: {doc['subject']}")
        print(f"Question: {doc['question']}")
        print(f"Choices: {doc['choices']}")
        print(f"Response: {results[0]}")
        print(f"box_matches: {box_matches}, last_boxed_match: {last_boxed_match}, target: {target}")
        print(f"lm_eval_result: {lm_eval_result}")
        print(f"exact_match: {exact_match}")
        # NOTE: Needs human intervention or llm as judge.
        accept_uncertain = 1

    # flexible match.

    results = {
        "exact_match": exact_match,
        "accept_uncertain": accept_uncertain,
    }
    return results
