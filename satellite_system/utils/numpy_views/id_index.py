from typing import Dict, List

class IdIndex:
    """
    Bijection between IDs and array indices.
    """
    def __init__(self, ids: List[int]):
        ids = list(ids)
        self.id_to_idx: Dict[int, int] = {
            id_: i for i, id_ in enumerate(ids)
        }
        self.idx_to_id: List[int] = ids

    def idx(self, id_: int) -> int:
        return self.id_to_idx[id_]

    def id(self, idx: int) -> int:
        return self.idx_to_id[idx]
