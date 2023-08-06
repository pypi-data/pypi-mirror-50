# Created based on bbox.json and test.json
import json
import logging
import numpy as np
import os

from collections import defaultdict

class _GroundAnnotation:
    """Ground truth of objects in each image"""
    def __init__(self):
        self._boxes = np.empty((0, 4), dtype=np.float32)
        self._cls_idxs = np.empty((0,), dtype=np.int32)
        # map of unique cls in image and count
        self._uniq_cls_idx_count_map = defaultdict(int)

    @property
    def boxes(self):
        return self._boxes

    @property
    def classes(self):
        return self._cls_idxs

    @property
    def uniq_classes_count_map(self):
        """returns dict with cls idx and corresponding count"""
        return self._uniq_cls_idx_count_map

    def update_annotation(self, box, cls):
        """
        Args:
            box (ndarray): (1, 4) dimensional 2-D numpy array with [xmin, ymin, xmax, ymax]
            cls (ndarray): 1-D numpy array with class idx ex: [1]
        """
        self._boxes = np.concatenate((self._boxes, box))
        self._cls_idxs = np.concatenate((self._cls_idxs, cls))
        # map of uniq clsses and count
        self._uniq_cls_idx_count_map[cls.item(0)] += 1


class _PredAnnotation:
    """Prediction info of objects in each image"""
    def __init__(self):
        self._boxes = np.empty((0, 4), dtype=np.float32)
        self._cls_idxs = np.empty((0,), dtype=np.int32)
        self._probs = np.empty((0,), dtype=np.float32)

    @property
    def boxes(self):
        return self._boxes

    @property
    def classes(self):
        return self._cls_idxs

    @property
    def probs(self):
        return self._probs

    def update_annotation(self, box, cls, prob):
        """
        Args:
            box (ndarray): (1, 4) dimensional 2-D numpy array with [xmin, ymin, xmax, ymax]
            cls (ndarray): 1-D numpy array with class idx ex: [1]
            prob (ndarray): 1-D numpy array same as cls but with float type
        """
        self._boxes = np.concatenate((self._boxes, box))
        self._cls_idxs = np.concatenate((self._cls_idxs, cls))
        self._probs = np.concatenate((self._probs, prob))

class Dataset:
    def __init__(self, gt_file, pred_file, data_root):
        """Initialize dataset for visualization analysis

        Args:
            gt_file (str): path to json file with predictions info (ex: '<path>/bbox.json')
            pred_file (str): path to json file with gt box annoations (ex: '<path>/test.json')
            data_root (str): root directory of the dataset, containing a
                       directory for images, annotations.csv, labels.json,
                       train.json, and test.json
        """

        self.logger = logging.getLogger(__name__)

        # GT info
        # Load class labels from gt file
        with open(gt_file) as gt_json:
            gt_data = json.load(gt_json)

        # -1 to make 0 as start of classes idx
        self._cls_to_idx = {cat['name'].lstrip(): cat['id']-1 for cat in gt_data['categories']}
        self._idx_to_cls = dict(map(reversed, self._cls_to_idx.items()))
        self.classes = list(self._cls_to_idx.keys())

        self._data_root = data_root

        path_to_imgs = self._get_imgs_dir_name()
        # {'1':'<path>/xx.jpg',...}
        self._imgid_to_filename = {img['id']:os.path.join(path_to_imgs, img['file_name'])
                                   for img in gt_data['images']}
        self.all_filenames = list(self._imgid_to_filename.values())
        # files or examples or images mean the same
        self._num_examples = len(gt_data['images'])

        # Load prediction data
        with open(pred_file) as pred_json:
            pred_data = json.load(pred_json)

        # Load annotations
        self.logger.info('Parsing %s', gt_file)
        # {'filename': _GroundAnnotation, ..} , filename = <path>/xx.jpg
        self._gt_annotations = self._load_annotations(gt_data, is_GT=True)

        self.logger.info('Parsing %s', pred_file)
        # {'filename': _PredAnnotation, ..}, filename = <path>/xx.jpg
        self._pred_annotations = self._load_annotations(pred_data, is_GT=False)
        self._adjust_imgs_with_no_pred()

        self._print_statistics()

    @property
    def num_classes(self):
        """Return number of classes, not including the background class."""
        return len(self.classes)

    @property
    def cls_to_idx(self):
        return self._cls_to_idx

    def _get_imgs_dir_name(self):
        """return path to images directory"""
        _,all_dirs,_ = next(os.walk(self._data_root))
        for dir_name in all_dirs:
            # to ignore cache
            if not dir_name.startswith('__') or dir_name.startswith('.'):
                return os.path.join(self._data_root, dir_name)

    def _imgid_to_filename(self, img_id):
        """gives img name along with path ex: <path>/xx.jpg from it's id"""
        return self._imgid_to_filename[img_id]

    def _load_annotations(self, data, is_GT=False):
        """is_GT is bool with True value when data is a GT annotation """
        annotations = data['annotations'] if is_GT else data
        imgwise_ann = {}

        for ann in annotations:
            # filename includes img_name along with <path>
            # cls_idx starts with 0, 1-D np array with single element
            # box in [xmin, xmax, ymin, ymax] format, 2-D np array with (1,4) shape
            # prob is 1D numpy array with single element
            filename, cls_idx, box, prob = self._decode_annotation_box(ann)
            if filename not in imgwise_ann:
                # initialize
                imgwise_ann[filename] = _GroundAnnotation() if is_GT else _PredAnnotation()

            if is_GT:
                imgwise_ann[filename].update_annotation(box, cls_idx)

            else:
                imgwise_ann[filename].update_annotation(box, cls_idx, prob)

        return imgwise_ann

    def _adjust_imgs_with_no_pred(self):
        # for images with 0 predictions
        for filename in self.all_filenames:
            if filename not in self._pred_annotations:
                # initialize to empty boxes
                self._pred_annotations[filename] = _PredAnnotation()

    def generate_data(self, filename):
        """
        Args:
            filename (str): image name along with path. ex: <path>/xx.jpg
        """
        # predictions info
        boxes_pred = self._pred_annotations[filename].boxes
        boxes_pred_probs = self._pred_annotations[filename].probs
        cls_idx_pred = self._pred_annotations[filename].classes

        # gt info
        gt_boxes = self._gt_annotations[filename].boxes
        cls_idx_gt = self._gt_annotations[filename].classes

        return boxes_pred, boxes_pred_probs, cls_idx_pred, gt_boxes, cls_idx_gt

    def _decode_annotation_box(self, annotation):
        """Decode a box from the annotations file.

        Args:
            annotation (dict): contains multiple fields. required here are image_id, category_id, bbox


        Ex. annotation: {"id": 1, "image_id": 1, "category_id": 7, "iscrowd": 0, "area": 69720,
            "bbox": [394.0, 0.0, 280.0, 249.0],
            "segmentation": [[673.0, 248.5, 394.0, 248.5, 393.5, 0.0, 673.0, 0, 673.0, 248.5]],
            "width": 1196, "height": 1600}
        """
        img_id = annotation['image_id']
        filename = self._imgid_to_filename[img_id]
        # -1 to make cls idx start from 0
        box_cls_idx = np.array([annotation['category_id']-1])
        # [x1, y1, w, h]
        box_data = annotation['bbox']
        prob = np.empty(0, dtype=np.float32)

        x_min = box_data[0]
        y_min = box_data[1]
        # w = x2 - x1 + 1
        # h = y2 - y1 + 1
        x_max = x_min + box_data[2] - 1
        y_max = y_min + box_data[3] - 1
        box = np.array([[x_min, y_min, x_max, y_max]])

        if 'score' in annotation:
            prob = np.array([annotation['score']])

        return filename, box_cls_idx, box, prob


    def _gt_class_distribution(self):
        """For distribution of ground truth bounding boxes

        Returns:
            A dict mapping class name to number of ground truth bounding boxes
            in the class.
        """
        # TODO: see if this can be made faster by vectorizing
        boxes_per_class = defaultdict(int)   # dict(zip(self.classes, [0] * self.num_classes))
        for ref in self._gt_annotations:
            cls_idx_count_map = self._gt_annotations[ref].uniq_classes_count_map
            for cls_idx in cls_idx_count_map:
                cls_label = self._idx_to_cls[cls_idx]
                boxes_per_class[cls_label] += cls_idx_count_map[cls_idx]

        # TODO: cache output if performance is an issue
        return boxes_per_class

    def _print_statistics(self):
        # statistics of ground truth annotations
        self.logger.info('Number of classes: %d', len(self.classes))
        self.logger.info('Number of images: %d', self._num_examples)

        boxes_per_class = self._gt_class_distribution()

        # Sort classes by number of examples
        boxes_sorted = sorted(boxes_per_class.items(), key=lambda x: -x[-1])

        self.logger.info(
            'Per class number of boxes:\nTotal\tClass\n' +
            '\n'.join(('{:d}\t{}'.format(
                v, k)
                for k, v in boxes_sorted)))