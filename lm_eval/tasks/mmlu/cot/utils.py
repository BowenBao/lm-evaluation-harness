import re

from typing import List, Dict

def process_results(doc: dict, results: List[str], lm_eval_result=None) -> Dict[str, int]:
    # We modified this function reffering to the following implement by Meta:
    # https://github.com/meta-llama/llama-recipes/blob/v0.0.4
    candidates = results[0]
    target = "ABCD"[doc["answer"]]

    # Ignore content before </think> tag, if tag exists.
    if "</think>" in candidates:
        candidates = candidates.split("</think>")[-1]

    # Strict exact match in box.
    box_matches = re.findall(
        r"\\boxed{\(*([A-D])\)*}",
        candidates,
    )
    box_matches = [match for match in box_matches if match]
    last_boxed_match = box_matches[-1] if box_matches else None
    exact_match = int(last_boxed_match == target)

    # Most strict, all results must be same.
    box_match = None
    if box_matches:
        if all([match == box_matches[0] for match in box_matches]):
            box_match = box_matches[0]
        else:
            # print(f"Response: {results[0][-32:]}")
            # print(box_matches)
            pass
    most_strict = int(box_match == target)

    # flexible match
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
    flexible_match = int(last_boxed_match == target)

    best_possible = flexible_match
    if (last_boxed_match not in ["A", "B", "C", "D"]) or (not exact_match and lm_eval_result == target):
        # print("--------------------")
        # print(f"Subject: {doc['subject']}")
        # print(f"Question: {doc['question']}")
        # print(f"Choices: {doc['choices']}")
        # print(f"Response: {results[0]}")
        # print(f"box_matches: {box_matches}, last_boxed_match: {last_boxed_match}, target: {target}")
        # print(f"lm_eval_result: {lm_eval_result}")
        # print(f"exact_match: {exact_match}")
        # Needs human intervention or llm as judge.
        best_possible = 1

    results = {
        "exact_match": exact_match,
        "flexible_match": flexible_match,
        "best_possible": best_possible,
        "most_strict": most_strict,
    }
    return results
