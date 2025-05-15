import re

from typing import List, Dict


def process_results(doc: dict, results: List[str]) -> Dict[str, int]:
    exact_match = []
    target = doc["answer"]

    for candidates in results[0]:
        # # Ignore content before </think> tag, if tag exists.
        # if "</think>" in candidates:
        #     candidates = candidates.split("</think>")[-1]

        # Strict exact match in box.
        box_matches = re.findall(
            r"\\boxed{\(*(\d+)\)*}",
            candidates,
        )
        box_matches = [match for match in box_matches if match]
        last_boxed_match = box_matches[-1] if box_matches else None
        exact_match.append(int(int(last_boxed_match) == int(target)))

    results = {
        "pass@1": sum(exact_match) / len(exact_match),
        "cons@k": float(sum(exact_match) >= (len(exact_match) // 2))
    }
    return results
