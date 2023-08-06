'''
1 to 7 category id info goes here

1 - only TP's (same cls pred, gt) and corresponding pred boxes, gt boxes are no more used for inter class analysis
2 - same cls pred, gt with overlap less than required threshold but overlap>0
3 - pred, gt belong to same cls and have sufficient overlap but there is other pred with higher overlap
4 - Pred and gt are of different class but have overlap > IoU threshold. so just changing one label makes the pair TP
5 - Pred and gt are of different class but that's the maximum IoU that prediction can get with ground truths (but IoU<IoU threshold).
If the max IoU with same class
then ignore that prediction.
the boxes that have max IoU with that of same class.
6 - Prediction that didn't had IoU with any GT of same class. (do not have same class ground truth in the image or
overlap of prediction with same class ground truth is zero)
6' - Prediction with 0 IoU with both same class gt and other class gt
7 - GT not assigned. No Predictions of same class in the image or overlap of predictions with same cls
    with this ground truth is < IoU threshold

Total gt boxes = 1+7
Total pred boxes = 1+2+3+4+5+6*
number of (6*) = countof(6) - [countof(4) + countof(5)]

python run_analysis.py --predictions ~/Downloads/bbox.json --gt ~/Downloads/test.json --data_root ~/Downloads/abi_13labels_21june19 --output ~/Desktop/
#Pillow==2.2.1
'''
import csv
import cv2
import errno
import heapq
import io
import json
import logging
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import warnings

from collections import defaultdict
from glob import glob
from PIL import Image
from tqdm import tqdm
from visdetect import config
from visdetect import metrics as metrics_lib
from visdetect import plots as global_plots

warnings.filterwarnings("ignore")

class VisDetection:
    def __init__(self, cls_to_idx, data_root, tb_dir, vis_config=None):
        """ Initialize vis dashboard for fine grained analysis of TP, FP, FN

        Args:
            cls_to_idx (dict): Class label to index mapping. Index 0 should be normal class
                        and no BG class here.
            data_root (str): root directory of the training dataset, containing examples directory,
                        annotations.csv, labels.json, train.json, and test.json
            tb_dir (str): directory to save tensorboard files
            vis_config (config.VisConfig): configuration instance that is used for some outputs of
                        this tool (ex: ground annotations likely wrong annotated, predictions
                        likely not annotated)

        Provides analysis for 7 fine grained error types. Definitions follow below
        Intra-class types: (pair of pred, gt of same cls)
        1 - TP
        2 - FP with not sufficient overlap
        3 - FP with sufficient overlap but confidence less than some other predicted box

        Inter-class types: (pair of pred, gt with different cls)
        4 - FP with sufficient IoU with a GT box of other cls. so just changing pred cls makes the pair TP :)
        5 - FP with insufficient IoU with a GT box of other cls. However, that's the max IoU pred box can have
            with any GT
        Note: If a pair satisfies 5 but pred, gt has same cls then it would be counted in type 2 and not as
              type 5 error

        Other: (pair with only one of pred or gt is available)
        6 - FP prediction with no IoU with GT of same cls as prediction. This happens either when GT do not exists
            in the image or IoU=0 with GT box
        7 - FN implies gt box not predicted. This can happen when no predictions of same class
            in the image or overlap of predictions with same cls ground truth is < IoU threshold

        Extra/Special:
        6*/6p - FP which is a subset of type 6. It's for predictions with 0 IoU with both same class or different
            class gt boxes.

        Note: type1 + type2 + type3 + type4 + type5 + type6* = total predicted boxes
            where, type6* = type6 - (type4 + type5)
            type 6 is the predictions with IoU=0 with same gt class, while
            type 6* is the prediction with IoU=0 with either same gt class/different class gt. i.e. NO IoU with any
            of the gt boxes

        """
        # does not include BG class.
        self.total_classes = len(cls_to_idx)
        self.cls_to_idx = cls_to_idx
        self.idx_to_cls = dict(map(reversed, cls_to_idx.items()))

        # tensorboard log setup
        self.tb_dir = tb_dir
        if not os.path.exists(self.tb_dir):
            os.makedirs(self.tb_dir)

        # config updates
        self.vis_config = vis_config

        if vis_config is None:
            self.vis_config = config.VisConfig()

        self.data_root = data_root

        self.logger = logging.getLogger(__name__)

        # global metrics
        # matrix[i][j] = number of observations known to be in class i
        # but predicted to be as class j
        # initial (0) indicates normal cls (not reserved for BG)
        self.global_confusion_matrix = np.zeros(
            shape=(self.total_classes,
                   self.total_classes),
            dtype=np.int64)

        # 7 fine grained error categories/types over entire test set
        self.global_catwise_total = defaultdict(int)

        # predicted objects distribution over 7 category error types
        # {class_id: {cat_id:count,..}, ..}
        self.global_clswise_cat_errors = defaultdict(lambda: defaultdict(int))

        # For type 6 overall conf distribution
        # In visualizations, conf distribution is shown only for type 6
        self.conf_points = np.linspace(0, 1, 11, dtype=np.float32)
        self.conf_dist_for_type6 = defaultdict(int)

        # For type 6 cls-wise conf distribution
        # {class_id: {conf_ref:count,..}, ..}
        # In visualizations, conf distribution is shown only for type 6
        self.conf_dist_for_type6_clswise = defaultdict(lambda: defaultdict(int))
        # self.conf_dist_for_type6 = dict((p, 0) for p in self.conf_points)

        # predicted and gt boxes
        self.pred_boxes_per_class = defaultdict(int)
        self.gt_boxes_per_class = defaultdict(int)
        self.pred_boxes_total = 0
        self.gt_boxes_total = 0

        # all type errors over entire test set
        # each pair in it also has filename
        self.cat_pairs_global = defaultdict(list)

        # vis merged pairing after cv2 edits
        self.cat_imgs_merged_global = defaultdict(list)

        self.require_filtering = True if vis_config.filter_pairs_of_error_type else False
        if self.require_filtering:
            # int between 1 to 7
            self.filter_pair_type = vis_config.filter_pairs_of_error_type
            # keys are image basename
            # values are list of dicts ex: [{'box': pred_box, 'label': pred_cls_label},...]
            # selected based on confidence threshold
            # here values would be either 'gt' or 'pred' object details based on
            # vis_config.filter_object_type
            self.filtered_boxes_given_type = defaultdict(list)
            # 'gt' or 'pred'
            self.filter_object_type = vis_config.filter_object_type
            self.conf_for_type_filtering = vis_config.conf_for_type_filtering

        # To find mAP, classwise precision metrics
        self.metrics_info = metrics_lib.MetricsInfo(self.vis_config.iou_threshold,
                                                    self.idx_to_cls)
        # initialize all fine grained errors
        self._initialize_fg_errors()

    @property
    def get_mean_average_precision(self):
        """Computes classwise avg precision if it's not
        computed earlier. Later, computes mAP (float)"""
        if not self.metrics_info.class_metrics:
            # classwise average precision
            self.metrics_info.update_average_precision_percls(self.gt_boxes_per_class)

        return self.metrics_info.mean_average_precision

    def _tb_create_summary_writer(self, filename, type):
        """Creates a FileWriter for current image/filename

        Args:
            filename (str): image basename i.e. without path info
            type (str): 'Global' or 'Local'

        Returns:
            tb_writer(tf.summary.FileWriter): to create event files for tensorboard
                                        visualization

        """
        logdir = os.path.join(self.tb_dir, type)
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        tb_writer = tf.compat.v1.summary.FileWriter(os.path.join(logdir, filename),
                                                    flush_secs=5)

        return tb_writer

    def _tb_log_global_allclass_metrics(self, metric_name,
                                        cm_figure,
                                        tab,
                                        tb_writer):
        """Shows global metrics (evaluation over entire test set) like confusion matrix,
        overall distribution of all 7 error types, classwise distribution of 7 error types.

        Args:
            metric_name (str): Tag name to be added for current matplotlib plot
            cm_figure (cv2 Image): The Figure instance from matplotlib pyplot (plt.figure)
            tab (str): 'allclass' or 'classwise' to display corresponding metrics under that
                    specific tab on tensorboard
            tb_writer (tf.summary.FileWriter): to create event files for tensorboard
                                        visualization

        """
        cm_summaries = []

        with io.BytesIO() as byte_io:
            cm_figure.savefig(byte_io, format='png', bbox_inches='tight')
            png_buffer = byte_io.getvalue()

        # Create an Image object
        cm_summary = tf.compat.v1.Summary.Image(encoded_image_string=png_buffer)

        # Create a Summary value
        cm_summaries.append(tf.compat.v1.Summary.Value(tag='Global_{}/{}'.format(tab, metric_name),
                                                                        image=cm_summary))

        # Create and write Summary
        summary = tf.compat.v1.Summary(value=cm_summaries)
        tb_writer.add_summary(summary)


    def _tb_log_objects_of_img(self, all_results, tb_writer):
        """ Shows local metrics like (image-wise original object and prediction grouping into 7 types
        __Main__ tab contains original image with gt annotations, original image with predicted boxes
        (green indicate TP, red for FP)
        Tabs on TB for Type_1 to Type_7 shows respective pairs in that groups

        Args:
            all_results (dict): contains categorywise mapping of cropped boxes. This is used for
                  tensorboard vis. Each key has the content for each tab on tensorboard (ex: _Main_,
                  Type_1, Type_2 etc..).
                  9 keys are 'ground_img', 'pred_img', 1 to 7
                  values as list of corresponding cropped images
                  values of 'ground_img' and 'pred_img' would be single valued as its just orig img
                  with some box labels.
                  values of 1 to 7 keys would contain all merged (gt, pred) cropped img pairs.
            tb_writer (tf.summary.FileWriter): to create event files for tensorboard
                                        visualization

        """
        if not all_results:
            return

        for cat_id in list(['ground_img', 'pred_img']+list(range(1, 8))):
            # hard coded to make comprehensible ordering on tensorboard
            if cat_id in ('ground_img', 'pred_img'):
                # for tensorboard tab name
                tag = '_Main_'
            else:
                tag = 'Type_{}'.format(cat_id)

            img_summaries = []
            images = all_results[cat_id]

            for i, img in enumerate(images, start=1):
                # print ('img=', img.shape, img.dtype)
                # Write the image to a string
                with io.BytesIO() as byte_io:
                    img_crop_pil = Image.fromarray(img)
                    img_crop_pil.save(byte_io, format="PNG")
                    png_buffer = byte_io.getvalue()

                # Create an Image object
                img_summary = tf.compat.v1.Summary.Image(encoded_image_string=png_buffer)

                if tag=='_Main_':
                    # ground or pred as a image sub tag
                    i = cat_id.split('_')[0]
                # Create a Summary value
                img_summaries.append(tf.compat.v1.Summary.Value(tag='{}/{}'.format(tag, i),
                                                      image=img_summary))

            # Create and write Summary
            summary = tf.compat.v1.Summary(value=img_summaries)
            tb_writer.add_summary(summary)
        tb_writer.close()

    def _tb_log_objects_all_imgs(self, cat_pairs_merged_imgs, tb_writer):
        """ Shows global pairings under tabs on TB for Type_1 to Type_7 with respective pairs in those types

        Args:
            cat_pairs_merged_imgs (dict): contains categorywise mapping of cropped boxes. This is used for
                  tensorboard vis. Each key has the content for each tab on tensorboard (ex: Type_1,
                  Type_2 etc..).
                  7 keys from 1 to 7
                  values as list of corresponding cropped images
                  values of 1 to 7 keys would contain all merged (gt, pred) cropped img pairs.
            tb_writer (tf.summary.FileWriter): to create event files for tensorboard
                                        visualization

        """
        if not cat_pairs_merged_imgs:
            return

        for cat_id in range(1, 8):
            # hard coded to make comprehensible ordering on tensorboard
            tag = 'Type_{}'.format(cat_id)

            img_summaries = []
            images = cat_pairs_merged_imgs[cat_id]
            file_seen_count = defaultdict(int)

            for filename, img in images:
                img_basename = filename.split('/')[-1]
                file_seen_count[filename]+=1
                # Write the image to a string
                with io.BytesIO() as byte_io:
                    img_crop_pil = Image.fromarray(img)
                    img_crop_pil.save(byte_io, format="PNG")
                    png_buffer = byte_io.getvalue()
                # Create an Image object
                img_summary = tf.compat.v1.Summary.Image(encoded_image_string=png_buffer)
                # Create a Summary value
                img_summaries.append(tf.compat.v1.Summary.Value(tag='{}/{}/{}'.format(tag,
                                                                                      img_basename,
                                                                                      file_seen_count[filename]),
                                                                                      image=img_summary))
            # Create and write Summary
            summary = tf.compat.v1.Summary(value=img_summaries)
            tb_writer.add_summary(summary)
        tb_writer.close()

    def perform_global_analysis(self):
        """Write all global stats (both classwise and allclass)
        Creates filtered_annotations.csv if requested
        """
        self.logger.info('Running Global Visual Analysis...')
        # All class #
        tab = 'metrics_Allclass'
        tb_writer = self._tb_create_summary_writer(tab, 'Global')
        fig_cm = global_plots.get_confusion_matrix_plt(self.global_confusion_matrix,
                                                       self.cls_to_idx,
                                                       normalize=False)

        fig_errors = global_plots.get_error_dist_plt(self.global_catwise_total,
                                                     self.gt_boxes_total,
                                                     self.pred_boxes_total,
                                                     self.conf_dist_for_type6)

        fig_map = global_plots.get_map_plt(self.metrics_info.class_metrics,
                                           self.get_mean_average_precision,
                                           self.metrics_info.iou_threshold)

        # write as tb events
        # allclass metric 1
        self._tb_log_global_allclass_metrics('m1_confusion_matrix', fig_cm, tab, tb_writer)
        # allclass metric 2
        self._tb_log_global_allclass_metrics('m2_error_distributions', fig_errors, tab, tb_writer)
        # allclass metric 3: mAP with clswise avg precision
        self._tb_log_global_allclass_metrics('m3_mAP', fig_map, tab, tb_writer)

        tb_writer.close()

        # Classwise / Per-class #
        tab = 'metrics_Classwise'
        tb_writer = self._tb_create_summary_writer(tab, 'Global')
        for cls_idx in range(self.total_classes):
            fig_cls_errors = global_plots.get_error_dist_plt(self.global_clswise_cat_errors[cls_idx],
                                                             self.gt_boxes_per_class[cls_idx],
                                                             self.pred_boxes_per_class[cls_idx],
                                                             self.conf_dist_for_type6_clswise[cls_idx])
            curr_cls_name = self.idx_to_cls[cls_idx]
            # per-class error distributions
            self._tb_log_global_allclass_metrics(curr_cls_name, fig_cls_errors, tab, tb_writer)

        # Compute TopK global predictions #
        # For each error category type, create k global examples for tb
        k = self.vis_config.number_of_objects_per_error_global
        cat_pairs_idx_global_topk = dict()

        # contains categorywise mapping of cropped boxes/rois.
        # keys from 1 to 7
        # values as list of corresponding cropped images
        # values would contain all merged (gt, pred) cropped img pairs.
        # similar to all_results except no 'ground_img', 'pred_img' keys
        cat_pairs_merged_imgs = defaultdict(list)
        # pairs before actually merging
        # before reading with cv2
        # topk version of cat_pairs_global
        cat_pairs_global_topk = dict()
        cat_pairs_global_pbar = tqdm(self.cat_pairs_global.items())
        for err_type, pairs in cat_pairs_global_pbar:
            cat_pairs_global_pbar.set_description("Identifying top roi pairs for each error type:")
            # err_type is an int ranging from 1 to 7
            # pair (tuple): contains (filename, predicted box, gt box,
            # confidence, IoU, cls_pred_idx, cls_gt_idx)
            # only cat_pairs_global has filename as an element in its pairs
            conf_idx_in_pair = 3
            # idx_pair_tuple (idx, (pair)) ex:( 0, (filename, predicted box, gt box,
            #                   confidence, IoU, cls_pred_idx, cls_gt_idx) )
            cat_pairs_idx_global_topk[err_type] = [idx_pair_tuple[0] for idx_pair_tuple in heapq.nlargest(k,
                                                                    enumerate(self.cat_pairs_global[err_type]),
                                                                    key=lambda tup: tup[1][conf_idx_in_pair])]

            if not self.vis_config.analyse_only_global_metrics:
                # use the merged pairs already created in local analysis
                cat_pairs_merged_imgs[err_type] = [self.cat_imgs_merged_global[err_type][idx] for idx in
                                                   cat_pairs_idx_global_topk[err_type]]
            else:
                # to create k merged pairs now for each err type
                cat_pairs_global_topk[err_type] = [self.cat_pairs_global[err_type][idx] for idx in
                                                   cat_pairs_idx_global_topk[err_type]]

        if not cat_pairs_merged_imgs:
            self.logger.info("Seems like local analysis is turned off. Creating visual roi pairs now using openCV...")
            cat_pairs_merged_imgs = _create_all_image_vis_results_only_rois(self.idx_to_cls,
                                                                            cat_pairs_global_topk)
        tb_writer.close()
        # write topk global pairs per error type
        tab = 'Pairings'
        tb_writer = self._tb_create_summary_writer(tab, 'Global')
        self._tb_log_objects_all_imgs(cat_pairs_merged_imgs, tb_writer)
        tb_writer.close()

        if self.require_filtering:
            # creates filtered_annotations.csv
            self.logger.info('Creating filtered_annotations.csv')
            output_dir = os.path.abspath(os.path.join(self.tb_dir, '../'))
            filtered_objects_csv(self.filtered_boxes_given_type, output_dir)
            self.logger.info('Total filtered objects = {}'.format(len(self.filtered_boxes_given_type.values())))
            self.logger.info('Saved filtered objects '
                        'annotation file (filtered_annotations.csv) '
                        'at {}'.format(output_dir))


    def _tb_log_objects_global(self, all_results, tb_writer):
        """ Over entire testset, picks objects globally.

        Args:
            all_results (dict): contains categorywise mapping of cropped boxes/rois. This is used for
                  tensorboard vis. Each key has the content for each tab on tensorboard (ex: _Main_,
                  Type_0 etc..).
                  9 keys are 'ground_img', 'pred_img', 1 to 7
                  values as list of corresponding cropped images
                  values of 'ground_img' and 'pred_img' would be single valued as its just orig img
                  with some box labels.
                  values of 1 to 7 keys would contain all merged (gt, pred) cropped img pairs.
            tb_writer (tf.summary.FileWriter): to create event files for tensorboard
                                        visualization

        """
        if not all_results:
            return

        for cat_id in (list(['ground_img', 'pred_img'])+list(range(1, 8))):
            # hard coded to make comprehensible ordering on tensorboard
            if cat_id in ('ground_img', 'pred_img'):
                # for tensorboard tab name
                tag = '_Main_'
            else:
                tag = 'Type_{}'.format(cat_id)

            img_summaries = []
            images = all_results[cat_id]

            for i, img in enumerate(images, start=1):
                # print ('img=', img.shape, img.dtype)
                # Write the image to a string
                with io.BytesIO() as byte_io:
                    img_crop_pil = Image.fromarray(img)
                    img_crop_pil.save(byte_io, format="PNG")
                    png_buffer = byte_io.getvalue()

                # Create an Image object
                img_summary = tf.compat.v1.Summary.Image(encoded_image_string=png_buffer)

                if tag=='_Main_':
                    # ground or pred as a image sub tag
                    i = cat_id.split('_')[0]
                # Create a Summary value
                img_summaries.append(tf.compat.v1.Summary.Value(tag='{}/{}'.format(tag, i),
                                                      image=img_summary))

            # Create and write Summary
            summary = tf.compat.v1.Summary(value=img_summaries)
            tb_writer.add_summary(summary)

    def _initialize_fg_errors(self):
        """Initializes all 7 fine grained category error types
           both for allclass scenario and clswise errors
        """
        # for overall error stats
        for cat_id in range(1, 8):
            self.global_catwise_total[cat_id] = 0

        # for cls-wise error stats
        for cls_id in range(self.total_classes):
            for cat_id in range(1, 8):
                self.global_clswise_cat_errors[cls_id][cat_id] = 0

        # for type6 error confidence distribution
        for ref_pt in self.conf_points:
            self.conf_dist_for_type6[ref_pt] = 0

        for cls_id in range(self.total_classes):
            for ref_pt in self.conf_dist_for_type6:
                self.conf_dist_for_type6_clswise[cls_id][ref_pt] = 0

    def _update_statistics(self, cat_pairs_img,
                           cls_idx_pred,
                           cls_idx_ground,
                           filename):
        """Updates Global stats like confusion matrix, type 6 errors with high confidence etc

        Args:
            cat_pairs_img (dict): categories/error types(int) as keys and list of error pairs as values
            cls_idx_pred (ndarray): 1-D ndarray of length M of predicted class labels where
                  M is equal to total predicted boxes
            cls_idx_ground (ndarray): 1-D ndarray of length N of predicted class labels where
                  N is equal to total ground truth boxes
            filename (str): image name without path info
        """
        # pred and gt boxes count
        self.pred_boxes_total += cls_idx_pred.shape[0]
        self.gt_boxes_total += cls_idx_ground.shape[0]

        # count stats
        for pred_idx in cls_idx_pred:
            self.pred_boxes_per_class[pred_idx] += 1
        for gt_idx in cls_idx_ground:
            self.gt_boxes_per_class[gt_idx] += 1

        # error metric stats for vis
        for cat_id, pairs in cat_pairs_img.items():
            self.global_catwise_total[cat_id] += len(pairs)
            for pair in pairs:
                pair_with_fname = (filename,) + pair
                self.cat_pairs_global[cat_id].append(pair_with_fname)
                self._update_clswise_cat_errors(pair, cat_id)
                if self.require_filtering and cat_id==self.filter_pair_type:
                    # image name after ignoring the path
                    img_basename = filename.split('/')[-1]
                    self._update_filtered_objects(img_basename, pair)
                if cat_id == 6:
                    self._update_pred_likely_not_ann(pair)
                # only when sufficient IoU exists
                # between predicted and ground truth for confusion matrix
                if cat_id in (1, 3, 4):
                    self._update_cmatrix(pair)

    def _update_filtered_objects(self, img_basename, pair):
        """ Updates filtered objects which are used in creating new annotations.csv

        Args:
            img_basename (str): image name without path info
            pair (tuple): contains (predicted box, gt box, confidence, IoU, cls_pred_idx, cls_gt_idx)

        """
        # object type to pair idx
        object_type_to_idx = {'pred':0, 'gt':1}
        idx = object_type_to_idx[self.filter_object_type]
        box = pair[idx].tolist()
        conf = pair[2]
        if not conf:
            # mostly type 7 cases
            conf = 0.0
        cls_idx = pair[idx-2]
        cls_label = self.idx_to_cls[cls_idx]
        if conf >= self.conf_for_type_filtering:
            self.filtered_boxes_given_type[img_basename].append({'box': box,
                                                                 'label': cls_label
                                                                })

    def _update_pred_likely_not_ann(self, pair):
        """ Updates type 6 category error for global stats

        Args:
            pair (tuple): contains (predicted box, gt box, confidence, IoU, cls_pred_idx, cls_gt_idx)

        """
        pred_conf = pair[2]
        pred_cls_idx = pair[-2]

        # For confidence distribution of type 6 errors
        nearby_point = min(self.conf_points, key=lambda x:abs(x-pred_conf))
        self.conf_dist_for_type6[nearby_point] += 1
        self.conf_dist_for_type6_clswise[pred_cls_idx][nearby_point] += 1

    def _update_clswise_cat_errors(self, pair, cat_id):
        """For each predicted cls, represents 1 to 7 error counts

        Args:
            pair (tuple): contains (predicted box, gt box, confidence, IoU, cls_pred_idx, cls_gt_idx)
            cat_id (int): Error type. A digit between [1, 7] (both ends included)

        """
        gt_cls_idx = pair[-1]
        pred_cls_idx = pair[-2]
        if pred_cls_idx.size:
            # Not category 3 error
            self.global_clswise_cat_errors[pred_cls_idx][cat_id] += 1
        else:
            # pred_cls_idx would be empty for all type 7 errors
            # Category 7 error
            assert cat_id==7, "Expected type 7 error but got error type: {:d}".format(cat_id)
            self.global_clswise_cat_errors[gt_cls_idx][cat_id] += 1

    def _update_cmatrix(self, pair):
        """Updates confusion matrix based on individual pairs

        Args:
            pair (tuple): contains (predicted box, gt box, confidence, IoU, cls_pred_idx, cls_gt_idx)

        """
        gt_cls_idx = pair[-1]
        pred_cls_idx = pair[-2]

        self.global_confusion_matrix[gt_cls_idx][pred_cls_idx] += 1

    def perform_perimg_analysis(self, boxes_pred,
                                boxes_pred_probs,
                                cls_idx_pred,
                                gt_boxes,
                                cls_idx_ground,
                                filename):
        """Creates pairing of pred and gt boxes into 7 category error types.
        Updates global stats and creates cropped image pairs with some text
        description on them.

        Args:
            boxes_pred (ndarray): 2-D ndarray of boxes of size [num_predicted_boxes, 4] with
                  columns ordered (min_x, min_y, max_x, max_y)
            boxes_pred_probs (ndarray): 1-D ndarray of length M of confidence score where
                  M is equal to total predicted boxes
            cls_idx_pred (ndarray): 1-D ndarray of length M of predicted class labels where
                  M is equal to total predicted boxes
            gt_boxes (ndarray): 2-D ndarray of boxes of size [num_groundtruth_boxes, 4] with same
                  column order as sources
            cls_idx_ground (ndarray): 1-D ndarray of length N of predicted class labels where
                  N is equal to total ground truth boxes
            filename (str): path+image_basename.

        Returns:
            all_results (dict): contains categorywise mapping of cropped boxes. This is used for
                  tensorboard vis. Each key has the content for each tab on tensorboard (ex: _Main_,
                  Type_0 etc..).
                  9 keys are 'ground_img', 'pred_img', 1 to 7
                  values as list of corresponding cropped images with text descriptions on them
                  values of 'ground_img' and 'pred_img' would be single valued as its just orig img
                  with some box labels.
                  values of 1 to 7 keys would contain all merged (gt, pred) cropped img pairs.

            #pred_likely_not_ann (list): contains category 6 errors with confidence > threshold
            #      each item would be a dict {'box': pred_box, 'label': pred_cls_label_name}

        """
        iou_threshold = self.vis_config.iou_threshold

        # first class is index 0. BG is assigned -1
        # also stores clswise probs, tp_fp for map computation later
        cat_pairs_img = _map_pred_to_ground_imgwise(boxes_pred,
                                                    boxes_pred_probs,
                                                    cls_idx_pred,
                                                    gt_boxes,
                                                    cls_idx_ground,
                                                    iou_threshold,
                                                    self.metrics_info)



        # update global metrics based on current image
        # confusion matrix and error counts
        self._update_statistics(cat_pairs_img,
                                cls_idx_pred,
                                cls_idx_ground,
                                filename)

        # local (curr img) metrics
        if not self.vis_config.analyse_only_global_metrics:
            # also need local metrics (img-wise analysis)
            # ground_img, pred_img, error-category-wise (7 error types) results
            all_results = _create_per_image_vis_results(boxes_pred,
                                                        cls_idx_pred,
                                                        gt_boxes,
                                                        cls_idx_ground,
                                                        filename,
                                                        self.idx_to_cls,
                                                        cat_pairs_img,
                                                        iou_threshold)
            for err_type in all_results:
                if not isinstance(err_type, int):
                    # 'ground_img', 'pred_img'
                    continue
                # update merged pairs
                self.cat_imgs_merged_global[err_type]+=all_results[err_type]

            # TB vis
            # image name after ignoring the path
            img_basename = filename.split('/')[-1]
            tb_writer = self._tb_create_summary_writer(img_basename, 'Local')
            self._tb_log_objects_of_img(all_results, tb_writer)
            tb_writer.close()

def _map_pred_to_ground_clswise(boxes_pred_cls,
                                boxes_pred_probs_cls,
                                gt_boxes_cls,
                                cls_pred,
                                cls_gt,
                                iou_threshold,
                                metrics_info):
    """ This does two steps based on classwise labels/predictions for one image
             1. One to One mapping pair(both with same class label) for predicted boxes and ground truth
             2. Responsible for categories- 1,2,3,6,7 (ones with same class/no box in predictions or ground truth)
             3. Assign one of the above 5 seven categories to each pair

    Args:
        boxes_pred_cls (ndarray): 2-D ndarray of a class boxes of size [num_predicted_boxes, 4] with
                    columns ordered (min_x, min_y, max_x, max_y).
        boxes_pred_probs_cls (ndarray): 1-D ndarray of length M of confidence score where
                    M is equal to total predicted boxes and all boxes of same class.
        gt_boxes_cls (ndarray): 2-D ndarray of a class boxes of size [num_targets, 4] with same
                    column order as boxes_pred_cls.
        cls_pred (ndarray): 1-D ndarray with class idx for pred_boxes
        cls_gt (ndarray): 1-D ndarray with class idx for gt_boxes
        iou_threshold (float): threshold for overlap checks
        metrics_info (metrics_lib.MetricsInfo): instance with access to classwise precision etc.

    Returns:
        cat_pairs_cls (dict): with keys as category id and values as list of tuples where
                each tuple has 6 elements (predicted box, gt box, confidence, IoU, cls_pred_idx, cls_gt_idx).
                If prediction do not have a pair then gt box would be empty and zero IoU.
                If prediction have a pair then both should be of same class/label.
        further_eval_pred (ndarray): 1-D ndarray of bool values that tells whether a predicted
                box should be used for other categorizations. TP's are ignored from further
                categorization.
        further_eval_gt (ndarray): 1-D ndarray of bool values that tells whether a ground truth
                box should be used for other categorizations. ground boxes corresponding to
                TP's are ignored from further categorization.
    """

    # Sort same class boxes by confidence
    sorted_idx = np.argsort(-boxes_pred_probs_cls)
    boxes_pred_cls_sorted = boxes_pred_cls[sorted_idx, :]
    boxes_pred_probs_cls_sorted = boxes_pred_probs_cls[sorted_idx]
    cls_pred_sorted = cls_pred[sorted_idx]

    cat_pairs_cls = defaultdict(list)
    num_boxes_pred = boxes_pred_cls_sorted.shape[0]
    num_boxes_gt = gt_boxes_cls.shape[0]

    # tells if a box should be considered for future categorizations
    further_eval_pred = np.ones(num_boxes_pred, dtype=np.bool_)
    further_eval_gt = np.ones(num_boxes_gt, dtype=np.bool_)

    tp_fp_for_map = np.zeros(num_boxes_pred, dtype=np.bool_)

    if num_boxes_gt < 1:
        # no gt boxes
        # all predictions would belong to category 6
        gt_boxes_cls_empty = gt_boxes_cls.reshape(num_boxes_pred, 0)
        cls_gt_empty = cls_gt.reshape(num_boxes_pred, 0)
        overlaps = np.zeros(num_boxes_pred, dtype=np.float32)
        all_pairs = list(zip(boxes_pred_cls_sorted, gt_boxes_cls_empty,
                             boxes_pred_probs_cls_sorted, overlaps,
                             cls_pred_sorted, cls_gt_empty))
        cat_pairs_cls[6] += all_pairs
        # update for mAP computation
        metrics_info.update_boxes_probs_and_tp_fp(cls_pred_sorted[0],
                                                  boxes_pred_probs_cls_sorted,
                                                  tp_fp_for_map)

        return cat_pairs_cls, further_eval_pred, further_eval_gt


    is_gt_box_assigned = np.zeros(num_boxes_gt, dtype=np.bool_)

    assignments, overlaps = \
        metrics_lib.assign_to_highest_overlap_numpy(boxes_pred_cls_sorted, gt_boxes_cls)

    for i in range(assignments.size):
        pair = [(boxes_pred_cls_sorted[i],
                 gt_boxes_cls[assignments[i]],
                 boxes_pred_probs_cls_sorted[i],
                 overlaps[i],
                 cls_pred_sorted[i],
                 cls_gt[assignments[i]])]

        if overlaps[i] >= iou_threshold:
            if not is_gt_box_assigned[assignments[i]]:
                # pred is TP. Prediction of category 1
                tp_fp_for_map[i] = True
                further_eval_pred[i] = False
                further_eval_gt[assignments[i]] = False
                is_gt_box_assigned[assignments[i]] = True
                cat_pairs_cls[1]+=pair
            else:
                # prediction of category 3
                # enough IoU but gt already assigned to
                # high confidence prediction
                cat_pairs_cls[3]+=pair

        elif overlaps[i]>0:
            # prediction of category 2
            cat_pairs_cls[2]+=pair

        else:
            # IoU = 0. Prediction of Category 6
            pair = [(boxes_pred_cls_sorted[i],
                     np.empty(0, dtype=np.float32),
                     boxes_pred_probs_cls_sorted[i],
                     overlaps[i],
                     cls_pred_sorted[i],
                     np.empty(0, dtype=np.int64))]

            cat_pairs_cls[6]+=pair

    # update for mAP computation
    metrics_info.update_boxes_probs_and_tp_fp(cls_pred_sorted[0],
                                              boxes_pred_probs_cls_sorted,
                                              tp_fp_for_map)

    not_gt_box_assigned = is_gt_box_assigned == False
    left_gt_boxes_cls = gt_boxes_cls[not_gt_box_assigned, :]
    left_gt_cls = cls_gt[not_gt_box_assigned]

    # GT boxes with less IoU overlap threshold
    # (but there exists a pred with same cls in the image)
    # -> category 7
    num_left_boxes_gt = left_gt_boxes_cls.shape[0]
    # reshape for zip
    boxes_pred_cls_empty = np.empty(0).reshape(num_left_boxes_gt, 0)
    boxes_pred_probs_cls_empty = np.empty(0).reshape(num_left_boxes_gt, 0)
    overlaps = np.zeros(num_left_boxes_gt, dtype=np.float32)
    cls_pred_empty = np.empty(0, dtype=np.int64).reshape(num_left_boxes_gt, 0)

    all_pairs = list(zip(boxes_pred_cls_empty, left_gt_boxes_cls,
                         boxes_pred_probs_cls_empty, overlaps,
                         cls_pred_empty, left_gt_cls))

    cat_pairs_cls[7] += all_pairs

    return cat_pairs_cls, further_eval_pred, further_eval_gt

def _map_pred_to_ground_imgwise(boxes_pred,
                                boxes_pred_probs,
                                cls_idx_pred,
                                gt_boxes,
                                cls_idx_ground,
                                iou_threshold,
                                metrics_info):
    """ This does two steps on an image level
             1. One to One mapping pair of predicted boxes and ground truth
             2. Assign one of the seven categories to each pair

    Args:
        boxes_pred (ndarray): 2-D ndarray of boxes of size [num_sources, 4] with
            columns ordered (min_x, min_y, max_x, max_y)
        boxes_pred_probs (ndarray): 1-D ndarray of length M of confidence score where
            M is equal to total predicted boxes
        cls_idx_pred (ndarray): 1-D ndarray of length M of predicted class labels where
            M is equal to total predicted boxes
        gt_boxes (ndarray): 2-D ndarray of boxes of size [num_targets, 4] with same
            column order as sources
        cls_idx_ground (ndarray): 1-D ndarray of length N of predicted class labels where
            N is equal to total ground truth boxes
        iou_threshold (float): Threshold for overlap checks
        metrics_info (metrics_lib.MetricsInfo): instance with access to classwise precision etc.

    Returns:
        cat_pairs_img (dict): keys as category id (int between 1 to 7) and values as
                list of tuples where each tuple has 4 elements (predicted box(2-D),
                gt box(2-D), confidence(1-D), IoU(1-D), pred cls idx(1-D),gt cls idx(1-D)).
                If prediction do not have a pair then gt box would be empty and zero IoU.
    """
    boxes_further_eval_pred_img = np.empty(0).reshape(0,4)
    boxes_prob_further_eval_pred_img = np.empty(0)
    boxes_further_eval_gt_img = np.empty(0).reshape(0,4)
    cls_idx_further_pred_img = np.empty(0, dtype=np.int64)
    cls_idx_further_gt_img = np.empty(0, dtype=np.int64)

    cat_pairs_img = defaultdict(list)

    uniq_cls_idx = np.unique(np.concatenate((cls_idx_pred, cls_idx_ground)))

    for cls_idx in uniq_cls_idx:
        cls_boxes_mask = cls_idx_pred == cls_idx
        cls_gt_boxes_mask = cls_idx_ground == cls_idx

        boxes_pred_cls = boxes_pred[cls_boxes_mask, :]
        boxes_pred_probs_cls = boxes_pred_probs[cls_boxes_mask]
        num_boxes_pred = boxes_pred_cls.shape[0]
        gt_boxes_cls = gt_boxes[cls_gt_boxes_mask, :]
        cls_pred = cls_idx_pred[cls_boxes_mask]
        cls_gt = cls_idx_ground[cls_gt_boxes_mask]

        if num_boxes_pred >= 1:
            cat_pairs_cls, further_eval_pred_cls, further_eval_gt_cls = \
                _map_pred_to_ground_clswise(boxes_pred_cls,
                                            boxes_pred_probs_cls,
                                            gt_boxes_cls,
                                            cls_pred,
                                            cls_gt,
                                            iou_threshold,
                                            metrics_info)
            _add_cls_pairs_to_img(cat_pairs_img, cat_pairs_cls)

        else:
            # all GT boxes of this cls go to category 7
            # no prediction with same cls
            num_boxes_gt = gt_boxes_cls.shape[0]
            # reshape for zipping
            boxes_pred_cls_empty = boxes_pred_cls.reshape(num_boxes_gt, 0)
            boxes_pred_probs_cls_empty = boxes_pred_probs_cls.reshape(num_boxes_gt, 0)
            cls_pred_empty = cls_pred.reshape(num_boxes_gt, 0)

            further_eval_pred_cls = np.ones(num_boxes_pred, dtype=np.bool_)
            further_eval_gt_cls = np.ones(num_boxes_gt, dtype=np.bool_)

            overlaps = np.zeros(num_boxes_gt, dtype=np.float32)
            all_pairs = list(zip(boxes_pred_cls_empty, gt_boxes_cls, boxes_pred_probs_cls_empty,
                                 overlaps, cls_pred_empty, cls_gt))
            cat_pairs_img[7] += all_pairs

        # Only TP pred, gt boxes are eliminated from further analysis
        boxes_further_eval_pred_img = np.concatenate((boxes_further_eval_pred_img,
                                                      boxes_pred_cls[further_eval_pred_cls, :]))
        boxes_prob_further_eval_pred_img = np.concatenate((boxes_prob_further_eval_pred_img,
                                                           boxes_pred_probs_cls[further_eval_pred_cls]))
        boxes_further_eval_gt_img = np.concatenate((boxes_further_eval_gt_img,
                                                    gt_boxes_cls[further_eval_gt_cls, :]))

        cls_idx_further_pred_img = np.concatenate((cls_idx_further_pred_img,
                                                   cls_pred[further_eval_pred_cls]))
        cls_idx_further_gt_img = np.concatenate((cls_idx_further_gt_img,
                                                 cls_gt[further_eval_gt_cls]))

    # For each predicted box, consider the maximum area with gt boxes
    # If max area exists with same cls then ignore it
    # as it's already added to either 2 or 3 category
    # returns max area for a pred box with all gt boxes
    assignments, overlaps = metrics_lib.assign_to_highest_overlap_numpy(boxes_further_eval_pred_img,
                                                                        boxes_further_eval_gt_img)

    # gt boxes for inter class (mappings of different cls) analysis
    # after removing ones responsible for TP's
    # num_boxes_gt_left = boxes_further_eval_gt_img.shape[0]

    # For category 4 and 5
    for i in range(assignments.size):
        # ignore if max area is with same cls box
        if cls_idx_further_pred_img[i]!=cls_idx_further_gt_img[assignments[i]]:
            pair = [(boxes_further_eval_pred_img[i],
                     boxes_further_eval_gt_img[assignments[i]],
                     boxes_prob_further_eval_pred_img[i],
                     overlaps[i],
                     cls_idx_further_pred_img[i],
                     cls_idx_further_gt_img[assignments[i]])]

            if overlaps[i] >= iou_threshold:
                # pred is FP of category 4
                # This prediction has max IoU with this ground truth
                cat_pairs_img[4] += pair

            elif overlaps[i] > 0:
                # prediction of category 5
                cat_pairs_img[5] += pair

            # pred with max IoU=0 already added to category 6
            # so skip

    return cat_pairs_img


def _add_cls_pairs_to_img(cat_pairs_img, cat_pairs_cls):
    """
    Adds classwise pairs into overall image pairs

    Args:
        cat_pairs_img (dict): dict with keys as category id and values as list of tuples where
                each tuple has 4 elements (predicted box, gt box, confidence, IoU).
        cat_pairs_cls (dict): dict with keys as category id and values as list of tuples with
                same format as above.

    """
    for cat_id, pairs in cat_pairs_cls.items():
        cat_pairs_img[cat_id] += pairs


def _draw_text_in_image(img, text, txt_align,
                        add_border=False,
                        border_info=None):
    """ Creates a border at the bottom and writes text on it
    adds border if add_border=True

    Args:
        img (cv2 Image): image generated from cv2.imread operation
        text (str): text to write on image
        txt_align (str): 'top' or 'bottom'. all text added on top would be
                aligned to centre of img. all text added on bottom would be
                aligned to left of img
        add_border (bool): tells whether to add border to image
        border_info (tuple): contains coordinates info for border (top,bottom,left,right)

    Returns:
        img_after_txt (cv2 Image): image after couple of cv2 image operations

    """
    assert txt_align != 'top' or 'bottom', "currently only top and bottom " \
                                           "alignment of text is supported"

    # top are mostly labels so small size works
    font_size = 0.5
    thickness = 1
    # white
    color = (255,255,255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    top_border, bottom_border, left_border, right_border = (0, 0, 0, 0)

    text_width_max = 0
    text_height_max = 0
    for i, text_inline in enumerate(text.split('\n')):
        text_width_inline, text_height_inline = cv2.getTextSize(text_inline, font, font_size, thickness)[0]
        text_width_max = max(text_width_inline, text_width_max)
        text_height_max += text_height_inline

    # min gap between two lines of text
    delta = 15

    if add_border:
        assert border_info is not None, "border info is not provided"
        top_border, bottom_border, left_border, right_border = border_info
        black = [0, 0, 0]
        img_width = img.shape[1]

        # pads such that text fits the roi
        left_border = max(int((text_width_max-img_width)/2), left_border)
        right_border = max(int((text_width_max-img_width)/2), right_border)
        if txt_align == 'top':
            top_border = max(top_border, text_height_max)
        elif txt_align == 'bottom':
            bottom_border = max(bottom_border, text_height_max)

        img_with_border = cv2.copyMakeBorder(img, top_border, bottom_border,
                                             left_border, right_border,
                                             cv2.BORDER_CONSTANT, value=black)

    img_before_txt = img_with_border if add_border else img
    img_before_txt_height, img_before_txt_width = img_before_txt.shape[:2]

    # init values for vertical position to draw text
    v_pos_top = int(top_border/2) if top_border else delta
    v_pos_bottom = int(img_before_txt_height - (bottom_border*0.8))

    for i, text_inline in enumerate(text.split('\n')):
        text_width_inline, text_height_inline = cv2.getTextSize(text_inline, font, font_size, thickness)[0]
        if txt_align == 'top':
            centre_pt = (int((img_before_txt_width-text_width_inline)/2), v_pos_top)
            cv2.putText(img_before_txt, text_inline, centre_pt, font, font_size, color, thickness)
            v_pos_top += text_height_inline
            v_pos_top += delta

        elif txt_align == 'bottom':
            left_pt = (int(delta/2), v_pos_bottom)
            cv2.putText(img_before_txt, text_inline,
                        left_pt, font, font_size,
                        color, thickness)
            v_pos_bottom += text_height_inline
            v_pos_bottom += delta

    # in-place image editing
    img_after_txt = img_before_txt

    return img_after_txt

def _draw_text_merge_draw_text(gt_roi,
                               pred_roi,
                               confidence,
                               pred_iou,
                               pred_label,
                               gt_label):
    """Draws text(cls label info) on individual cropped rois,
       merges both pred, gt and later draws text(iou, pred_prob info)

     Args:
         gt_roi (cv2 Image): cropped gt box location in original image
         pred_roi (cv2 Image): cropped pred box location in original image
         confidence (str): original float value in '{}%' format ex: '0.50%'.
                 would be '0.00%' when box is empty.
         pred_iou (str): original float value in '{}' format ex: '0.5'
         pred_label (str): predicted label name. would be 'NA' if box is empty
         gt_label (str): ground truth label name. would be 'NA' if box is empty

     Returns:
         pred_gt_map_full_with_headline (cv2 Image): image with text embedded in it

    """

    gt_roi_with_border_txt = _draw_text_in_image(gt_roi, gt_label,
                                                 txt_align='top',
                                                 add_border=True,
                                                 border_info=(30,0,0,0))

    pred_roi_with_border_txt = _draw_text_in_image(pred_roi, pred_label,
                                                   txt_align='top',
                                                   add_border=True,
                                                   border_info=(30,0,0,0))

    max_h = max(gt_roi_with_border_txt.shape[0], pred_roi_with_border_txt.shape[0])
    sum_w = gt_roi_with_border_txt.shape[1] + pred_roi_with_border_txt.shape[1]

    # screen to place the two rois
    screen_height = int(1.5 * max_h)
    screen_width = int(1.5 * sum_w)
    pred_gt_map_full = np.zeros((screen_height,screen_width,3), dtype=np.float32)

    # rest over space into 3 parts(left, mid, right)
    # 1(left) is gt and 2(right) is pred
    x1_left = int((screen_width - sum_w)/3)
    x1_right = x1_left + gt_roi_with_border_txt.shape[1]
    x_delta = x1_left
    x2_left = x1_right + x_delta
    x2_right = x2_left + pred_roi_with_border_txt.shape[1]

    y1_top = y2_top = int((screen_height-max_h)*3/4)
    y1_bottom = y1_top + gt_roi_with_border_txt.shape[0]
    y2_bottom = y2_top + pred_roi_with_border_txt.shape[0]

    pred_gt_map_full[y1_top:y1_bottom, x1_left:x1_right] = gt_roi_with_border_txt
    pred_gt_map_full[y2_top:y2_bottom, x2_left:x2_right] = pred_roi_with_border_txt

    headline = 'IoU: ' + pred_iou + '\n' + \
               'Confidence: ' + confidence


    pred_gt_map_full_with_headline = _draw_text_in_image(pred_gt_map_full,
                                                         headline,
                                                         'top',
                                                         add_border=True,
                                                         border_info=(40,0,0,0))

    return pred_gt_map_full_with_headline.astype(np.uint8)


def _get_text_to_write_gt(filename, cls_idx_ground, idx_to_cls):
    """ Generates text about gt box to write on image

    Args:
        filename (str): current image name. contains path + img name
        cls_idx_ground (ndarray): 1-D ndarray of ground truth boxes idx
        idx_to_cls (dict): Mapping between class idx (int) and class label (str)

    Returns:
        text (str): text about gt box to write on the image

    """
    # 0 is assigned to normal class
    # BG classes are not included as they are assigned idx -1
    gt_curr_classes = np.unique(cls_idx_ground)
    gt_curr_labels = np.array([idx_to_cls[idx] for idx in gt_curr_classes])
    # last substring of original image name
    basename = filename.split('/')[-1][-50:]
    text = "Image: ..." + basename + " \n" + \
           "Total unique classes: "+ str(gt_curr_classes.size) + " " + \
           "(" + ", ".join(gt_curr_labels) + ")" + "\n" + \
           "Total boxes: "+ str(cls_idx_ground.size)

    return text

def _get_text_to_write_all_pred(cls_idx_pred,
                                idx_to_cls,
                                tp_count,
                                fp_count,
                                iou_threshold):
    """ Generates text about pred box to write on image

    Args:
        cls_idx_pred (ndarray): 1-D ndarray of predicted boxes idx
        idx_to_cls (dict): Mapping between class idx (int) and class label (str)
        tp_count (int): true positive count in the curr image predictions
        fp_count (int): false positive count in the curr image predictions
        iou_threshold (float): threshold to filter predicted boxes

    Returns:
        text (str): text about pred box to write on the image

    """
    # 0 is assigned to normal class
    # BG classes are not included as they are assigned idx -1
    pred_curr_classes = np.unique(cls_idx_pred)
    pred_curr_labels = np.array([idx_to_cls[idx] for idx in pred_curr_classes])
    text = "Total unique classes: "+ str(pred_curr_classes.size) + " " + \
           "(" + ", ".join(pred_curr_labels) + ")\n" + \
           "IoU threshold = "+ str(iou_threshold) + "\n" + \
           "TP = {} (GREEN), FP = {} (RED)".format(tp_count, fp_count)

    return text

def _put_all_boxes_gt(temp_gt_img, gt_boxes):
    """Keep all gt boxes on single image
    all boxes would be in green

    Args:
        temp_gt_img (cv2 Image): a copy of original image
        gt_boxes (ndarray): 2-D ndarray of boxes of size [num_sources, 4] with
                columns ordered (min_x, min_y, max_x, max_y)

    Returns:
        temp_gt_img (cv2 Image): Original image with ground truth
                bounding boxes on it

    """

    green = (0,255,0)
    for bbgt in gt_boxes:
        x1,x2,x3,x4 =  map(int, bbgt)
        temp_gt_img = cv2.rectangle(temp_gt_img,
                                    (x1, x2),
                                    (x3, x4),
                                    green,
                                    2)

    return temp_gt_img

def _put_all_boxes_pred(temp_pred_img, boxes_pred, cat_pairs_img):
    """Keep all predictions on single image
    TP's gets green and FP's gets red

    Args:
        temp_pred_img (cv2 Image): a copy of original image
        boxes_pred (ndarray): 2-D ndarray of boxes of size [num_predictions, 4] with
            columns ordered (min_x, min_y, max_x, max_y)
        cat_pairs_img (dict): with keys as 1 to 7 category error types. Values as
                    list of pairs. Each pair contains (predicted box, gt box,
                    confidence, IoU, cls_pred_idx, cls_gt_idx)

    Returns:
        temp_pred_img (cv2 Image): Original image with predicted bounding boxes on it
        tp_count (int): true positive count in the curr image predictions
        fp_count (int): false positive count in the curr image predictions
    """

    green = (0,255,0)
    light_red = (255,0,0) #(30,30,255)
    # draw Pred annotations on image
    tp_fp = np.zeros(boxes_pred.shape[0], dtype=np.bool_)
    # TP predictions
    for pair in cat_pairs_img[1]:
        # category 1 contains only TP's
        bbpred = pair[0]
        tp_idx = np.equal(bbpred, boxes_pred).all(axis=1)
        tp_fp[tp_idx] = True
        x1,x2,x3,x4 =  map(int, bbpred)
        temp_pred_img = cv2.rectangle(temp_pred_img,
                                      (x1, x2),
                                      (x3, x4),
                                      green,
                                      2)
    # FP predictions
    fp_mask = tp_fp == False
    boxes_pred_fp = boxes_pred[fp_mask,:]
    fp_count = boxes_pred_fp.shape[0]
    tp_count = boxes_pred.shape[0]-fp_count
    for bbpred in boxes_pred_fp:
        x1,x2,x3,x4 =  map(int, bbpred)
        temp_pred_img = cv2.rectangle(temp_pred_img, (x1, x2),
                                      (x3, x4), light_red, 2)

    return temp_pred_img, tp_count, fp_count

def _create_per_image_vis_results(boxes_pred,
                                  cls_idx_pred,
                                  gt_boxes,
                                  cls_idx_ground,
                                  filename,
                                  idx_to_cls,
                                  cat_pairs_img,
                                  iou_threshold):
    """
    creates images with
        1. gt annotations
        2. all pred annotations
        3. category-wise 1:1 mapping

    Args:
        boxes_pred (ndarray): 2-D ndarray of boxes of size [num_sources, 4] with
                  columns ordered (min_x, min_y, max_x, max_y)
        cls_idx_pred (ndarray): 1-D ndarray of length M of predicted class labels where
              M is equal to total predicted boxes
        gt_boxes (ndarray): 2-D ndarray of boxes of size [num_targets, 4] with same
              column order as sources
        cls_idx_ground (ndarray): 1-D ndarray of length N of predicted class labels where
              N is equal to total ground truth boxes
        filename (str): contains path+img_name
        idx_to_cls (dict): Mapping between class idx (int) and class label (str)
        cat_pairs_img (dict): with keys as 1 to 7 category error types. Values as
                    list of pairs. Each pair contains (predicted box, gt box,
                    confidence, IoU, cls_pred_idx, cls_gt_idx)
        iou_threshold (float): float number that acts as a threshold for overlap checks

    Returns:
       all_results (dict): contains category-wise mapping of cropped boxes. This is used for
              tensorboard vis. Each key has the content for each tab on tensorboard (ex: _Main_,
              Type_1 etc..).
              9 keys are 'ground_img', 'pred_img', 1 to 7
              values as list of corresponding cropped images with text descriptions
              values of 'ground_img' and 'pred_img' would be single valued as its just orig img
              with some box labels.
              values of 1 to 7 keys would contain all merged (gt, pred) cropped img pairs.

    """
    all_results = defaultdict(list)
    try:
        gt_img = cv2.imread(filename)
    except IOError:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename)

    temp_pred_img = gt_img.copy()
    temp_gt_img = gt_img.copy()

    # draw GT annotations on image
    temp_gt_img = _put_all_boxes_gt(temp_gt_img, gt_boxes)
    text_gt = _get_text_to_write_gt(filename, cls_idx_ground, idx_to_cls)
    img_gt_ann = _draw_text_in_image(temp_gt_img, text_gt,
                                     'bottom',
                                     add_border=True,
                                     border_info=(0,100,0,0))
    all_results['ground_img'].append(img_gt_ann)

    # draw all predictions on image
    temp_pred_img, tp_count, fp_count = _put_all_boxes_pred(temp_pred_img,
                                                            boxes_pred,
                                                            cat_pairs_img)
    text_pred = _get_text_to_write_all_pred(cls_idx_pred,
                                            idx_to_cls,
                                            tp_count,
                                            fp_count,
                                            iou_threshold)
    img_pred_ann = _draw_text_in_image(temp_pred_img, text_pred,
                                       'bottom',
                                       add_border=True,
                                       border_info=(0,100,0,0))
    all_results['pred_img'].append(img_pred_ann)

    '''
    Example when 
    pair is = (array([799, 262, 895, 313], dtype=int32), array([], dtype=float32), 0.3452347, 0.0, 0, array([], dtype=int32))
    pair[0].size = 4
    pair[-1].size = 0
    pair[-2].size = 1
    pred_label= 0
    pred_prob = 0.3452347
    pred_iou_with_gt = 0.0   
    '''
    # draw cropped results for all 7 categories
    for cat_id, pairs in cat_pairs_img.items():
        # sort by confidence
        sorted(pairs, key=lambda p: p[2])
        # sorted(pairs, key=itemgetter(2))
        for pair in pairs:
            pred_box, gt_box, pred_prob, pred_iou, pred_idx, gt_idx = pair
            # 0 is assigned to normal class
            # BG classes are not included as they are assigned idx -1
            pred_label = idx_to_cls[pred_idx] if pred_idx.size else 'NA'
            gt_label = idx_to_cls[gt_idx] if gt_idx.size else 'NA'
            confidence = '{}%'.format(round(pred_prob*100,2)) if pred_prob.size else '0.00%'
            IoU = '{}'.format(round(pred_iou,2))

            if pred_box.size and gt_box.size:
                xmin_pred, ymin_pred, xmax_pred, ymax_pred = pred_box.astype(int)
                pred_roi = gt_img[ymin_pred:ymax_pred, xmin_pred:xmax_pred]
                xmin_gt, ymin_gt, xmax_gt, ymax_gt = gt_box.astype(int)
                gt_roi = gt_img[ymin_gt:ymax_gt, xmin_gt:xmax_gt]

            elif not pred_box.size:
                xmin_gt, ymin_gt, xmax_gt, ymax_gt = gt_box.astype(int)
                gt_roi = gt_img[ymin_gt:ymax_gt, xmin_gt:xmax_gt]
                pred_roi = np.zeros_like(gt_roi)

            else:
                xmin_pred, ymin_pred, xmax_pred, ymax_pred = pred_box.astype(int)
                pred_roi = gt_img[ymin_pred:ymax_pred, xmin_pred:xmax_pred]
                gt_roi = np.zeros_like(pred_roi)

            #if cat_id == 1:
            #    dir_name = data_root+cls_label
            #    save_tp_rois()

            merged_img = _draw_text_merge_draw_text(gt_roi, pred_roi, confidence,
                                                    IoU, pred_label, gt_label)

            all_results[cat_id].append(merged_img)

    return all_results

def _create_all_image_vis_results_only_rois(idx_to_cls,
                                            cat_pairs_all_img):
    """
    creates images with
        1. category-wise 1:1 mapping

    Args:
        idx_to_cls (dict): Mapping between class idx (int) and class label (str)
        cat_pairs_all_img (dict): with keys as 1 to 7 category error types. Values as
                    list of pairs. Each pair contains (filename, predicted box, gt box,
                    confidence, IoU, cls_pred_idx, cls_gt_idx). Each pair can be from any image.

    Returns:
       all_results (dict): contains category-wise mapping of cropped boxes. This is used for
              tensorboard vis. Each key has the content for each tab on tensorboard (ex:
              Type_1, Type_2 etc..).
              7 keys are 1 to 7
              values as list of corresponding filename and cropped images with text descriptions a
              values of 1 to 7 keys would contain (filename, merged(gt, pred) cropped img pairs)

    """
    all_results = defaultdict(list)
    read_imgs = dict()

    # draw cropped results for all 7 categories
    for cat_id, pairs in cat_pairs_all_img.items():
        for pair in pairs:
            filename, pred_box, gt_box, pred_prob, pred_iou, pred_idx, gt_idx = pair
            if filename not in read_imgs:
                try:
                    gt_img = cv2.imread(filename)
                    read_imgs[filename] = gt_img
                except IOError:
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), filename)
            else:
                # reuse
                gt_img = read_imgs[filename]
            # 0 is assigned to normal class
            # BG classes are not included as they are assigned idx -1
            pred_label = idx_to_cls[pred_idx] if pred_idx.size else 'NA'
            gt_label = idx_to_cls[gt_idx] if gt_idx.size else 'NA'
            confidence = '{}%'.format(round(pred_prob*100,2)) if pred_prob.size else '0.00%'
            IoU = '{}'.format(round(pred_iou,2))

            if pred_box.size and gt_box.size:
                xmin_pred, ymin_pred, xmax_pred, ymax_pred = pred_box.astype(int)
                pred_roi = gt_img[ymin_pred:ymax_pred, xmin_pred:xmax_pred]
                xmin_gt, ymin_gt, xmax_gt, ymax_gt = gt_box.astype(int)
                gt_roi = gt_img[ymin_gt:ymax_gt, xmin_gt:xmax_gt]

            elif not pred_box.size:
                xmin_gt, ymin_gt, xmax_gt, ymax_gt = gt_box.astype(int)
                gt_roi = gt_img[ymin_gt:ymax_gt, xmin_gt:xmax_gt]
                pred_roi = np.zeros_like(gt_roi)

            else:
                xmin_pred, ymin_pred, xmax_pred, ymax_pred = pred_box.astype(int)
                pred_roi = gt_img[ymin_pred:ymax_pred, xmin_pred:xmax_pred]
                gt_roi = np.zeros_like(pred_roi)

            merged_img = _draw_text_merge_draw_text(gt_roi, pred_roi, confidence,
                                                    IoU, pred_label, gt_label)

            fn_and_merged_image = (filename, merged_img)

            all_results[cat_id].append(fn_and_merged_image)

    return all_results

def _list_to_csv(annotations, output_file):
    df = pd.DataFrame(annotations)
    df.to_csv(output_file, index=None)

def _add_suffix_to_dir_files(data_root_orig, suffix, ftype):
    """modifies filenames in given directory
    add a suffix to their original name
    This will only change the file names that has the
    extension provided in ftype
    ex: when suffix = '_old', annotations.csv -> annotations_old.csv

    Args:
        data_root_orig (str): path to original/initial dataset
        suffix (str): new suffix to be added for original filename
        ftype (list): contains strings of file extensions ex: ['json', 'txt']
    """
    for file_path in glob(data_root_orig + '/*'):
        # ignore directories
        if os.path.isfile(file_path):
            orig_pre, orig_suf = file_path.split('.')
            if orig_suf in ftype:
                file_path_new = '{}{}.{}'.format(orig_pre,
                                                 suffix,
                                                 orig_suf)
                os.rename(file_path, file_path_new)

'''
def _create_req_files_from_ann(annotations, output_path):
    # Creates labels.json, train.json, test.json,
    # classes.txt from annotations
    # Args:
    # annotations (list): annotations
    # output_path (str): path to write new files

    # write classes.txt file
    labels = set(
        [element['label'] for a, list in annotations for element in list])
    with open(os.path.join(output_path, 'classes.txt'), 'w') as out:
        out.write('\n'.join(labels))

    # write labels.json
    labels_dict = [{'id': k, 'name': v} for k, v in enumerate(labels)]
    with open(os.path.join(output_path, 'labels.json'), 'w') as out:
        out.write(json.dumps(labels_dict))

    # populate data
    labels_id_lookup = {}
    for label in labels_dict:
        labels_id_lookup[label['name']] = label['id']
        label['examples'] = [(file, example) for file, boxes in annotations for
                             example in
                             boxes if example['label'] == label['name']]

    # build train.json and train.txt
    training_files = {}
    file_id = 1
    training_list = [ex for l in labels_dict for ex in l['training']]
'''

def filtered_objects_csv(filtered_boxes_given_type, output_dir):
    """ Creates filtered_annotations.csv
    Args:
        filtered_boxes_given_type (dict): contains keys as image name and values as dict
                  of boxes and labels in that image that are likely not annotated (type 6 errors with high conf).
                  category 6 errors with confidence > threshold
                  each value for a key would be a dict {'box': pred_box, 'label': pred_cls_label_name}
                  pred_box is a list with 4 elements (xmin, ymin, xmax, ymax)
                  pred_cls_label_name is a string
        output_dir (str): path to output dir where filtered_annotations.csv is created
    """
    rows = []

    for filename in filtered_boxes_given_type:
        row = [filename]
        for box_and_label in filtered_boxes_given_type[filename]:
            tmp_box_info = {}
            xmin, ymin, xmax, ymax = box_and_label['box']
            label = box_and_label['label']
            tmp_box_info['x'] = xmin
            tmp_box_info['y'] = ymin
            tmp_box_info['width'] = xmax - xmin
            tmp_box_info['height'] = ymax - ymin
            tmp_box_info['label'] = label
            row.append(json.dumps(tmp_box_info))

        rows.append(row)

        ann_file_new = os.path.join(output_dir, 'filtered_annotations.csv')
        _list_to_csv(rows, ann_file_new)