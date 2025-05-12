import re

from typing import List, Dict

def process_results(doc: dict, results: List[str]) -> Dict[str, int]:
    # We modified this function reffering to the following implement by Meta:
    # https://github.com/meta-llama/llama-recipes/blob/v0.0.4
    candidates = results[0]
    target = doc["answer"] + "A"

    # Ignore content before </think> tag, if tag exists.
    if "</think>" in candidates:
        candidates = candidates.split("</think>")[-1]

    # Strict exact match in box.
    box_matches = re.findall(r"\\boxed{([A-D])}|\\boxed{\((([A-D])\)}", candidates)
    last_boxed_match = [m for match in box_matches for m in match if m][-1]

    exact_match = int(last_boxed_match == target)

    # flexible match.



    results = {
        "exact_match": exact_match,
    }
    return results