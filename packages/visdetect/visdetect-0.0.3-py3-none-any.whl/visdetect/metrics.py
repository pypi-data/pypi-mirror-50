import numpy as np

from collections import defaultdict
from functools import partial

class MetricsInfo:
    def __init__(self, iou_threshold, idx_to_cls):
        """Computes avgPrecision(classwise) for a given iou threshold
        Args:
            iou_threshold (float): Used for filtering predicted boxes in metric
                            computations
        """
        # key would be cls label(str) and value is float
        self.class_metrics = dict()

        self.iou_threshold = iou_threshold
        self.idx_to_cls = idx_to_cls
        self.cls_to_idx = dict(map(reversed, idx_to_cls.items()))

        # collects entire test set boxes
        # key is label(str), value as 2-D ndarray
        self.boxes_probs_per_cls = defaultdict(partial(np.ndarray, 0))
        # with bool values (True for TP, False for FP)
        self.tp_fp_per_cls = defaultdict(partial(np.ndarray, 0))

    @property
    def mean_average_precision(self):
        if self.class_metrics is None or len(self.class_metrics) == 0:
            return np.nan

        return np.nanmean(list(self.class_metrics.values()))

    def update_boxes_probs_and_tp_fp(self, curr_cls_id,
                                     curr_boxes_probs,
                                     curr_tp_fp):
        """Updates per class predicted boxes and also tp_fp based on them

        Args:
            curr_cls_id (int): current class idx
            curr_boxes_probs (ndarray): 2-D ndarray of a class boxes of size [num_predicted_boxes, 4] with
                    columns ordered (min_x, min_y, max_x, max_y).
            curr_tp_fp (ndarray): 1-D ndarray with bool values. True for TP prediction, False for FP
        """
        curr_cls_label = self.idx_to_cls[curr_cls_id]

        self.boxes_probs_per_cls[curr_cls_label] = np.concatenate((self.boxes_probs_per_cls[curr_cls_label],
                                                                   curr_boxes_probs))
        self.tp_fp_per_cls[curr_cls_label] = np.concatenate((self.tp_fp_per_cls[curr_cls_label],
                                                             curr_tp_fp))

    def _compute_average_precision(self, precision, recall):
        """Compute average precision per PASCAL VOC 2010 rules

        http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/devkit_doc.html#sec:ap

        Args:
            precision: 1-D ndarray of length M of precision values where
                precision[m] is the precision considering the m+1 samples with the
                highest confidence
            recall: 1-D ndarray containing recall values, in same format as the
                precision argument

        Returns:
            Average precision, i.e., area under the precision-recall curve,
            using VOC 2010 rules. If either precision or recall are None,
            NaN is returned instead.
        """
        if precision is None or recall is None:
            return np.nan

        recall = np.concatenate(([0], recall, [1]))
        precision = np.concatenate(([0], precision, [0]))

        # Preprocess precision to be monotonically non-increasing
        for i in reversed(range(precision.size - 1)):
            precision[i] = np.maximum(precision[i], precision[i + 1])

        indices = np.where(recall[1:] != recall[:-1])[0] + 1
        average_precision = np.nansum(
            (recall[indices] - recall[indices - 1]) * precision[indices])

        return average_precision

    def update_average_precision_percls(self, num_gt_boxes_per_cls):
        """Computes classwise avg precision

        Args:
            num_gt_boxes_per_cls (dict): key as cls_idx(int) and value is count of
                                ground truth boxes of that cls

        """
        for cls_label in self.idx_to_cls.values():
            cls_idx = self.cls_to_idx[cls_label]
            num_gt_boxes = num_gt_boxes_per_cls[cls_idx]
            if num_gt_boxes < 1:
                # If there are no ground truth objects,
                # then recall is undefined. (same as kensho way of computation)
                continue
            # Sort true/false positive labels by confidence
            sorted_idx = np.argsort(-self.boxes_probs_per_cls[cls_label])
            tp_fp = self.tp_fp_per_cls[cls_label][sorted_idx]

            true_positives = tp_fp.astype(np.int32)
            false_positives = 1 - true_positives

            cum_true_positives = np.cumsum(true_positives)
            cum_false_positives = np.cumsum(false_positives)

            precision = \
                cum_true_positives.astype(np.float32) / \
                (cum_true_positives + cum_false_positives)

            recall = cum_true_positives / num_gt_boxes

            self.class_metrics[cls_label] = self._compute_average_precision(precision,
                                                                            recall)

def _bbox_area(box):
    """Calculate the area of a box.

    Args:
        box: tensor of box coordinates (x1, y1, x2, y2)

    Returns:
        The area of the box
    """
    return (box[2] - box[0]) * (box[3] - box[1])


def assign_to_highest_overlap_numpy(sources: np.ndarray, targets: np.ndarray):
    """Assign boxes from sources to targets based on highest IoU overlap

    Output indices of target boxes for which each sources box has the highest
    intersection-over-union overlap.

    Note that in case of ties the identity of the return value
    is not guaranteed.

    Args:
        sources: 2-D ndarray of boxes of size [num_sources, 4] with
            columns ordered (min_x, min_y, max_x, max_y)
        targets: 2-D ndarray of boxes of size [num_targets, 4] with same
            column order as sources

    Returns:
        A tuple of two ndarrays:
        assignments: 1-D ndarray of size num_sources specifying indices of
            assignment from sources to targets. assignments[i] == j indicates
            that i-th box in sources has been assigned to the j-th
            box in targets. assignments[i] == -1 indicates that there were no
            target boxes.
        assigned_overlaps: 1-D ndarray of overlaps between the i-th source box and the
            assignment[i]-th target box.
    """
    # predicted related
    num_sources = sources.shape[0]
    # gt box related
    num_targets = targets.shape[0]

    if num_targets == 0:
        return -np.ones((num_sources, num_targets), dtype=np.int64), \
               np.zeros((num_sources, num_targets), dtype=np.float32)

    # Compute overlaps between sources and targets
    overlaps = bbox_overlaps_numpy(sources, targets)

    assignments = np.argmax(overlaps, axis=1)
    assigned_overlaps = overlaps[np.arange(overlaps.shape[0]), assignments]

    return assignments, assigned_overlaps


def bbox_overlaps_numpy(
        boxes: np.ndarray,
        queries: np.ndarray) -> np.ndarray:
    """Calculate overlaps of query_boxes vs. all bboxes

    For each query, compute intersection-over-union overlap with each box.

    Args:
        boxes: ndarray of shape [N, 4] containing N boxes with
            columns ordered (min_x, min_y, max_x, max_y)
        queries: ndarray of shape [K, 4] containing K query boxes with same
            column order as boxes.

    Returns:
        ndarray of overlaps of shape [N, K] such that overlaps[i, j] is the
        IoU overlap between box i and query j.
    """
    num_boxes = boxes.shape[0]
    num_queries = queries.shape[0]

    overlaps = np.zeros((num_boxes, num_queries), dtype=np.float)
    for k in range(num_queries):
        query_area = _bbox_area(queries[k, :])
        box_areas = (boxes[:, 2] - boxes[:, 0]) * \
                    (boxes[:, 3] - boxes[:, 1])

        intersection_widths = np.maximum(
            np.minimum(boxes[:, 2], queries[k, 2]) -
            np.maximum(boxes[:, 0], queries[k, 0]),
            0)

        intersection_heights = np.maximum(
            np.minimum(boxes[:, 3], queries[k, 3]) -
            np.maximum(boxes[:, 1], queries[k, 1]),
            0)

        # Intersection areas
        ia = intersection_heights * intersection_widths

        query_overlap = ia / (box_areas + query_area - ia)
        overlaps[ia > 0, k] = query_overlap[ia > 0]

    return overlaps