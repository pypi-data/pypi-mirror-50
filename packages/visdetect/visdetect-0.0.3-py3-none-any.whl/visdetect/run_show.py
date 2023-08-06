#!/usr/bin/env python
import argparse
from distutils.dir_util import copy_tree
import logging
import os
from random import randrange
import shutil
import socket
import subprocess
import sys


def get_tb_dir(args):
    """provides directory where tensorboard
    output to be stored.

    Args:
        args (argparse.ArgumentParser): Instance with input and output
                        directory path info
    """
    tb_dir = os.path.join(args.input)
    if not os.path.exists(tb_dir):
        os.makedirs(tb_dir)

    return tb_dir

def init_logging(verbose=False):
    handler = logging.StreamHandler(stream=sys.stdout)
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        handlers=[handler])

def validate_port(port):
    # check if port is already occupied
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', int(port))) # Try to open port
    except OSError as e:
        if e.errno is 48: # Errorno 48 means address already bound
            raise OSError ('{} already assigned. Try other '
                           'port using --port argument'.format(port))
        raise e
    s.close()

def main(args):
    init_logging(args.verbose)
    logger = logging.getLogger(__name__)
    port=args.port
    validate_port(port)

    require_global = not(args.local_only)
    require_local = not(args.global_only)

    if require_global and require_local:
        logger.info('Both Global and Local visualizations requested')

    tb_temp_dir = os.path.join(args.input,'temp')
    tb_temp_dir_global = os.path.join(tb_temp_dir, 'Global')
    tb_temp_dir_local = os.path.join(tb_temp_dir, 'Local')
    # remove if any and create new temp dir
    if os.path.exists(tb_temp_dir):
        shutil.rmtree(tb_temp_dir)
    # created required format temp directory
    os.makedirs(tb_temp_dir)

    if require_global:
        try:
            orig_global_dir = os.path.join(args.input, 'Global')
            os.makedirs(tb_temp_dir_global)
            # copy global dir to temp
            copy_tree(orig_global_dir, tb_temp_dir_global)
        except FileNotFoundError:
            print ('Global files not found at {} \n Try running: '
                                    'visdetect --analyze *args'.format(orig_global_dir))
            sys.exit(1)

    if require_local:
        orig_local_dir = os.path.join(args.input, 'Local')
        os.makedirs(tb_temp_dir_local)
        if not os.path.exists(orig_local_dir):
            raise FileNotFoundError('Local files not found at {} \n Try running: '
                                    'visdetect --analyze *args'.format(orig_local_dir))

        img_events = list()
        if args.files is not None:
            with open(args.files) as txt_file:
                logger.info('Reading from files.txt')
                img_events = [os.path.join(orig_local_dir, name.strip()) for name in txt_file.readlines()]

        if not img_events:
            # pick 10 random images
            logger.info('Empty files.txt, Copying 10 random image events')
            all_img_names = os.listdir(orig_local_dir)
            start = randrange(0, len(all_img_names)-1)
            end = start+10
            img_events = [os.path.join(orig_local_dir, name.strip()) for name in all_img_names[start:end]]

        for img_event in img_events:
            basename = img_event.split('/')[-1]
            dest_dir = os.path.join(tb_temp_dir_local, basename)
            # copy to temp local
            shutil.copytree(img_event, dest_dir)

    logger.info('Starting tensorboard on port {}'.format(port))
    subprocess.run(["tensorboard", "--logdir", "{}".format(tb_temp_dir), "--port", port])