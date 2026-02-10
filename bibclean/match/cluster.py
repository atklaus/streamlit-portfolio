from typing import Dict, Iterable, List, Tuple

from bibclean.models import Reference


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def choose_canonical(refs: List[Reference], indices: Iterable[int]) -> int:
    idxs = list(indices)
    with_doi = [i for i in idxs if refs[i].doi]
    candidates = with_doi or idxs
    candidates.sort(key=lambda i: (-len(refs[i].raw), refs[i].raw))
    return candidates[0]


def build_clusters(
    refs: List[Reference],
    edges: Iterable[Tuple[int, int, int]],
) -> Tuple[Dict[int, List[int]], Dict[int, int]]:
    uf = UnionFind(len(refs))
    for i, j, _score in edges:
        uf.union(i, j)

    clusters: Dict[int, List[int]] = {}
    for idx in range(len(refs)):
        root = uf.find(idx)
        clusters.setdefault(root, []).append(idx)

    canonical_by_root: Dict[int, int] = {}
    for root, indices in clusters.items():
        canonical_by_root[root] = choose_canonical(refs, indices)

    return clusters, canonical_by_root
