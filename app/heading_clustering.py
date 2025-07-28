from sklearn.cluster import DBSCAN
import numpy as np

def cluster_headings(headings):
    font_sizes = [h['font_size'] for h in headings if 'font_size' in h]

    if not font_sizes:
        return headings  # or [] if you want to skip clustering

    font_sizes_np = np.array(font_sizes).reshape(-1, 1)

    clustering = DBSCAN(eps=0.5, min_samples=1).fit(font_sizes_np)
    labels = clustering.labels_

    for i, h in enumerate(headings):
        h['cluster'] = int(labels[i])

    return headings
