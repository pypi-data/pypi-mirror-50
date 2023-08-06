#!/usr/bin/env python
"""Test a detection model."""

import argparse
import logging
import logging.handlers
import os
import os.path
import shutil
import sys

from visdetect import analysis
from visdetect import config
from visdetect.helpers import dataset_coco_format as dataset_cf
from tqdm import tqdm


def string_to_float_tuple(string):
    return tuple(float(x.strip()) for x in string.split(','))

def init_logging(verbose=False):
    handler = logging.StreamHandler(stream=sys.stdout)
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        handlers=[handler])

def get_tb_dir(args):
    """provides directory where tensorboard
    output to be stored.

    Args:
        args (argparse.ArgumentParser): Instance with input and output
                        directory path info
    """
    tb_dir = os.path.join(args.output_dir, 'tensorboard')
    if not os.path.exists(tb_dir):
        os.makedirs(tb_dir)
    else:
        overwrite = input('{} already exists. Delete and create new? Y = yes, N = no\n'.format(tb_dir))
        if overwrite.lower() == 'n':
            raise OSError('Output directory is expected to be empty')

        shutil.rmtree(tb_dir)
        os.makedirs(tb_dir)

    return tb_dir


def get_vis_config(args):
    vis_overrides = dict()
    vis_keys = (
        'analyse_only_global_metrics',
        'iou_threshold',
        'number_of_objects_per_error_global',
        'filter_pairs_of_error_type',
        'filter_object_type',
        'conf_for_type_filtering'
    )
    # override config values with commandline input
    for vis_key in vis_keys:
        if getattr(args, vis_key, None) is not None:
            vis_overrides[vis_key] = getattr(args, vis_key)

    vis_cfg = config.VisConfig(vis_overrides)

    return vis_cfg

def validate_args(pred_file, gt_file,
                  filter_pairs_of_error_type,
                  filter_object_type,
                  conf_for_type_filtering):
    assert pred_file.split('.')[-1]=='json', \
        "{} is expected to be a json file".format(pred_file)
    assert gt_file.split('.')[-1]=='json', \
        "{} is expected to be a json file".format(gt_file)

    if filter_pairs_of_error_type:
        assert 1<=filter_pairs_of_error_type<=7, \
            "Type has to be between 1 and 7 (both ends inclusive)"
        assert filter_object_type in ('gt', 'pred'), \
            "Unknown object type. only 'pred' or 'gt' are supported"
        assert 0<=conf_for_type_filtering<=1, \
            "confidence for filtering has to be positive and less than 1.0 "

        if filter_pairs_of_error_type==7:
            assert filter_object_type=='gt' and conf_for_type_filtering==0.0, \
            "Type 7 pairs do not have any predicted object and thus 0.0 confidence. " \
            "Try using filter_object_type='gt' and conf_for_type_filtering=0.0 "

        elif filter_pairs_of_error_type==6:
            assert filter_object_type=='pred', \
                "Type 6 pairs do not have any aasigned gt object. " \
                "Try using filter_object_type='pred' "

def main(args):
    init_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # required files
    gt_file = args.gt
    pred_file = args.predictions
    tb_dir = get_tb_dir(args)
    data_root = args.data_root
    filter_pairs_of_error_type = args.filter_pairs_of_error_type
    filter_object_type = args.filter_object_type
    conf_for_type_filtering = args.conf_for_type_filtering
    validate_args(pred_file, gt_file,
                  filter_pairs_of_error_type,
                  filter_object_type,
                  conf_for_type_filtering)

    vis_cfg = get_vis_config(args)

    # data for visual analysis
    dataset = dataset_cf.Dataset(gt_file, pred_file, data_root)
    # initialize
    vis_dectn = analysis.VisDetection(dataset.cls_to_idx,
                                      data_root,
                                      tb_dir,
                                      vis_cfg)
    filenames_pbar = tqdm(dataset.all_filenames)
    for filename in filenames_pbar:
        filenames_pbar.set_description("Running Imgwise Visual Analysis")
        logger.debug('Running vis analysis of {}'.format(filename))

        boxes_pred, boxes_pred_probs, cls_idx_pred, gt_boxes, cls_idx_ground = \
            dataset.generate_data(filename)
        # cls_idx start with 0
        vis_dectn.perform_perimg_analysis(boxes_pred,
                                          boxes_pred_probs,
                                          cls_idx_pred,
                                          gt_boxes,
                                          cls_idx_ground,
                                          filename)

    # computes global plots and write to tb
    vis_dectn.perform_global_analysis()

    # show tensorboard metrics
    logger.info('Saved tensorboard '
                'files at {}'.format(tb_dir))


