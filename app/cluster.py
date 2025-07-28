from collections import defaultdict
from sklearn.cluster import DBSCAN
import numpy as np

from .config import HEADING_LEVELS

def cluster_headings(blocks):
    headings = []
    blocks_by_page = defaultdict(list)
    for b in blocks:
        blocks_by_page[b["page"]].append(b)

    for page, page_blocks in blocks_by_page.items():
        candidates = [b for b in page_blocks if b["size"] > 8]
        if not candidates:
            continue

        y_coords = np.array([[b["y0"]] for b in candidates])
        clustering = DBSCAN(eps=15, min_samples=1).fit(y_coords)

        clusters = defaultdict(list)
        for idx, label in enumerate(clustering.labels_):
            clusters[label].append(candidates[idx])

        top_lines = []
        for cluster_blocks in clusters.values():
            cluster_blocks.sort(key=lambda b: (-b["size"], not b["bold"]))
            top_lines.append(cluster_blocks[0])

        unique_sizes = sorted(set(b["size"] for b in top_lines), reverse=True)
        level_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes[:HEADING_LEVELS])}

        for b in top_lines:
            level = level_map.get(b["size"])
            if level:
                headings.append({
                    "level": level,
                    "text": b["text"],
                    "page": b["page"] + 1
                })
    return headings
