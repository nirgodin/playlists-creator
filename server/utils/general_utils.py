import random
from typing import List


def build_prompt(prompt_prefix: str, prompt_suffix: str) -> str:
    return f'{prompt_prefix}\n{prompt_suffix}'


def sample_list(n_candidates: int, n_selected_candidates: int) -> List[int]:
    k = min(n_selected_candidates, n_candidates)
    return random.sample(range(0, n_candidates), k)
