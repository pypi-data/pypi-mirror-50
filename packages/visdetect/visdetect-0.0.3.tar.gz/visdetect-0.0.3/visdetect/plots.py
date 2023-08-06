import itertools
import math
import matplotlib.pyplot as plt
import numpy as np

from collections import OrderedDict

def get_confusion_matrix_plt(cm, cls_to_idx, normalize=False):
    """ Generates matplotlib figure of confusion matrix

    Args:
        cm (ndarray): Confusion matrix with 2-D ndarray of [n, n] dimensions where
                n = number of ormal classes (no BG class)
                cm[i][j] = number of observations known to be in class i but predicted to
                be as class j. index 0 class indicates normal cls (not reserved for BG)
        cls_to_idx (dict): mapping from class labels(str) to index (int)
        normalize (bool): tells whether to normalize values in confusion matrix

    Returns:
        figure (Figure) : The Figure instance from matplotlib pyplot (plt.figure)

    """
    # (array, shape = [n]): String names/class labels
    target_names = np.array(list(cls_to_idx.keys()))

    # the gradient of the values displayed from matplotlib.pyplot.cm
    # see http://matplotlib.org/examples/color/colormaps_reference.html
    cmap = plt.get_cmap('Blues')

    figure = plt.figure(figsize=(cm.shape[0], cm.shape[1]))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title('Confusion Matrix')
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=90)
        plt.yticks(tick_marks, target_names)

    if normalize:
        # Normalize the confusion matrix.
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm[np.isnan(cm)] = 0

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.2f}".format(cm[i, j]),
                     horizontalalignment="center",
                     verticalalignment='center',
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     verticalalignment='center',
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.close('all')

    return figure

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height"""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    color='blue')

def mask_pie_sizes_with_min_percent(sizes, labels,
                                    min_percent=5.0):
    """matplotlib pie chargs have the issue
    of overlapping labels when they have small percents/sizes. so
    avoid them with masking original sizes to match min_percent"""

    total = sum(sizes)
    percents = [round(s/total*100, 1) if total else 0 for s in sizes]
    orig_err_labels_map = {label:(perct, size) for label, perct, size in zip(labels, percents, sizes)}
    new_sizes = []
    for size, perct in zip(sizes, percents):
        if perct<min_percent:
            # mask
            req_size = round(min_percent*total/100)
            diff = req_size - size
            total+=diff
            new_sizes.append(req_size)
        else:
            new_sizes.append(size)

    return new_sizes, orig_err_labels_map

def draw_pie_chart_plt(ax,
                       err_labels,
                       sizes,
                       colors,
                       title,
                       angle=0):
    """Inserts Pie chart in the given axes(ax)

     Args:
         ax (plt.axes.Axes): Matplotlib Axes instance
         err_labels (list): labels to attach to the pie chart
         sizes (list): based on which area of subsection is computed
         colors (list): list of colors for pie subsections
         title (str): Title for the current axes plot
         angle (int): start angle

    """
    # add borders
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_zorder(1000)
    ax.patch.set_alpha(0.05)
    ax.patch.set_color('black')

    # to avoid overlapping labels issue with pie plots
    # mask min percentage and unmask at the end
    new_sizes, orig_err_labels_map = mask_pie_sizes_with_min_percent(sizes, err_labels,
                                                                     min_percent=6.0)

    # Equal aspect ratio ensures that pie is drawn as a circle
    patches, labels, autopercents = ax.pie(new_sizes,
                                           labels=err_labels,
                                           colors=colors,
                                           autopct='%1.1f%%',
                                           pctdistance=0.75,
                                           textprops= {'color':'black', 'weight':'bold'},
                                           explode = [0.05]*len(err_labels),
                                           radius = 1.2,
                                           shadow=False,
                                           startangle=angle)
    ax.axis('equal')
    # draw circle in the middle
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    ax.add_artist(centre_circle)

    for pct, label in zip(autopercents, labels):
        # unmask pie labels and percents
        orig_perct, orig_size = orig_err_labels_map[label.get_text()]
        pct.set_text("{:.1f}%\n({:d})".format(orig_perct, orig_size))

    ax.set_title(title)

def draw_conf_dist_type6_plt(ax, conf_dist_for_type6, global_catwise_total):
    """Inserts histogram into the given axes (ax). Histogram contains the
       confidence score distribution of type6 errors

    Args:
        ax (plt.axes.Axes): Matplotlib Axes instance
        conf_dist_for_type6 (dict): keys as confidence ref points ex: 0.1, 0.4 etc.., values
                            as its corresponding count (int)
        global_catwise_total (dict): keys as cat/error type ex: 1, 2..7 and values as its
                            corresponding error count (int)

    """
    width = 0.05

    # plot rectangle bars for each of conf ref point
    rects = dict()
    for ref_pt in conf_dist_for_type6:
        rects[ref_pt] = ax.bar(ref_pt, conf_dist_for_type6[ref_pt],
                               width, color='red', label='FP')

    ax.set_xticks(list(conf_dist_for_type6.keys()))

    # Add some text for labels, title
    ax.set_ylabel('Number of predictions nearby ref')
    ax.set_xlabel('Confidence ref points')
    ax.set_title('Confidence distribution of '
                 'type-6 errors ({:d})'.format(global_catwise_total[6]))

    # remove duplicate legend names
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right')
    ax.set_ylim(ymin=0)

    for rect_id in rects:
        autolabel(rects[rect_id], ax)

def draw_all_fine_grained_errors_plt(ax,
                                     err_counts,
                                     gt_boxes_total,
                                     pred_boxes_total):
    """ Inserts overall(7 types) errors distribution histogram into given axes (ax)

    Args:
        ax (plt.axes.Axes): Matplotlib Axes instance
        err_counts (dict): keys include error type, values as the count of
                        the corresponding error type.
        gt_boxes_total (int): total ground truth boxes
        pred_boxes_total (int): total predicted boxes

    """

    width = 0.8
    colors_labels_special = {1:('green','TP'), 7:('pink', 'FN')}

    # plot rectangle bars for each error type
    rects = dict()
    for i in range(1, len(err_counts)+1):
        c,l = colors_labels_special.get(i, ('red', 'FP'))
        rects[i] = ax.bar(i, err_counts[i], width, color=c, label=l)

    ax.set_ylim(ymin=0)
    # Add some text for labels, title
    ax.set_ylabel('Number of errors')
    ax.set_xlabel('Error type')
    ax.set_title('Overall Error Distribution '
                 '(Total {:d} GT and {:d} Pred boxes)'.format(gt_boxes_total,
                                                              pred_boxes_total))
    # remove duplicate legend names
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(),loc='upper right')

    for rect_id in rects:
        autolabel(rects[rect_id], ax)

    ax.set_xticks(np.arange(1, len(err_counts)+1))

def draw_cheat_sheet_plt(ax, err_to_color):
    """Details about error types"""
    err_to_text = OrderedDict([('Type-1', 'TP (IoU good, confidence good)'),
                               ('Type-2','FP (IoU bad but prediction same cls as GT)'),
                               ('Type-3','FP (IoU good but not best confidence)'),
                               ('Type-4','FP (IoU good but misclassified)'),
                               ('Type-5','FP (IoU bad and also misclassified)'),
                               ('Type-6','FP (IoU zero with same GT class)'),
                               ('Type-6*','FP (IoU zero with any GT class. Yes, subset of Type6)'),
                               ('Type-7','FN (GT had no TP prediction)')
                               ])

    xs = 0.04
    ys = 0.92
    # textbox properties
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    for typ, info in err_to_text.items():
        props['facecolor'] = err_to_color[typ.lower()]
        ax.text(xs, ys, '{} : {}'.format(typ, info),
                transform=ax.transAxes,
                fontsize=10,
                fontweight='bold',
                color = 'black',
                bbox=props)
        ys-=0.1

    extra_notes = 'Notes:\nTotal GT boxes = Type1 + Type7 \n' \
            'Total Pred boxes = Type1 + Type2 + Type3 + Type4 + Type5 + Type6* \n' \
            'Total 6* = Type6 - [ Type4 + Type5 ]'

    props['facecolor'] = 'grey'
    props['alpha'] = 0.1
    ax.text(xs, 0.03, extra_notes,
            transform=ax.transAxes,
            fontsize=10,
            fontweight='bold',
            color = 'black',
            bbox=props)
    ax.set_title('Cheat sheet for error types')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

def get_error_dist_plt(err_counts,
                       gt_boxes_total,
                       pred_boxes_total,
                       conf_dist_for_type6):
    """Creates error distribution figure with 6 subplots
    ax[0,0] for ground truth boxes (Type 7, Type 1)
    ax[1,0], ax[1,1] for predicted boxes (Type 1, 2 ,3 ,4, 5, 6, 6*)
    ax[2,0], ax[2,1] for all error distribution, type6 error confidence distribution (Type 1 to 7)

    Note: type1 + type2 + type3 + type4 + type5 + type6* = total predicted boxes
        where, type6* = type6 - (type4 + type5)
        type 6 is the predictions with IoU=0 with same class gt, while
        type 6* is the prediction with IoU=0 with any of gt boxes (same cls/different cls)

    Args:
        cls_name (str): current class name. Note: 'allclass" is a special class name
                    to get error distribution over all classes
        err_counts (dict): keys include error type, values as the count of
                        the corresponding error type.
        gt_boxes_total (int): total ground truth boxes
        pred_boxes_total (int): total predicted boxes
        conf_dist_for_type6 (dict): keys as confidence ref points ex: 0.1, 0.4 etc.., values
                            as its corresponding count (int)

    Returns:
        fig (plt.Figure) : The Figure instance from matplotlib pyplot (plt.figure)

    """
    w = 16
    h = 16
    err_to_color = {'type-1': 'green',
                    'type-2':'red', 'type-3':'red',
                    'type-4': 'red', 'type-5':'red',
                    'type-6':'red', 'type-6*': 'red',
                    'type-7': 'pink'}

    fig, ax = plt.subplots(figsize=(w, h), nrows=3, ncols=2)
    # plot 1
    err_labels=['type-1', 'type-7']
    draw_pie_chart_plt(ax[0,0],
                       err_labels=err_labels,
                       sizes=[err_counts[1], err_counts[7]],
                       colors=[err_to_color[e] for e in err_labels],
                       title='Ground truth boxes ({:d})'.format(gt_boxes_total),
                       angle=20)
    # plot 2
    draw_cheat_sheet_plt(ax[0,1], err_to_color)

    type_6p_count = pred_boxes_total - sum([err_counts[i] for i in range(1, 6)])
    # plot 3
    err_labels = ['type-{:d}'.format(i) if i!=6 else 'type-6*' for i in range(1, 7)]
    draw_pie_chart_plt(ax[1,0],
                       err_labels=err_labels,
                       sizes=[err_counts[i] if i!=6 else type_6p_count for i in range(1, 7)],
                       colors=[err_to_color[e] for e in err_labels],
                       title='Predicted boxes ({:d})'.format(pred_boxes_total),
                       angle=90)
    # plot 4
    err_labels = ['type-4', 'type-5', 'type-6*']
    draw_pie_chart_plt(ax[1,1],
                       err_labels= err_labels,
                       sizes=[err_counts[4], err_counts[5], type_6p_count],
                       colors=[err_to_color[e] for e in err_labels],
                       title='Type-6 errors ({:d})'.format(err_counts[6]),
                       angle=0)
    # plot 5
    draw_all_fine_grained_errors_plt(ax[2,0], err_counts,
                                     gt_boxes_total, pred_boxes_total)

    # plot 6
    draw_conf_dist_type6_plt(ax[2,1], conf_dist_for_type6, err_counts)

    # remove duplicate legend names
    handles, labels = ax[2,0].get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys(), loc='upper center')
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.3, wspace=0.15)
    plt.close('all')

    return fig

def get_map_plt(cls_metrics, mean_ap, iou):
    """Creates a plot showing clswise AP and mAP

    Args:
        cls_metrics (dict): with keys as cls label (str) and values as float
                    representing avg precision values
        mean_ap (float): mean average precision
        iou (float): iou threshold used for map computation

    Returns:
        fig (plt.Figure) : The Figure instance from matplotlib pyplot (plt.figure)
    """

    y_pos = np.arange(len(cls_metrics))
    labels = list(cls_metrics.keys())
    values = list(cls_metrics.values())
    title = 'mAP={:.3f} @ IoU={:.1f}'.format(mean_ap, iou)
    fig, ax = plt.subplots(figsize=(12,12), nrows=1, ncols=1)
    ax.barh(y_pos, values, height=0.5, align='center', alpha=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_ylabel('Class Labels')
    ax.set_xlim(xmin=0)
    ax.set_xticks(np.linspace(0, 1, 11, dtype=np.float32))
    ax.set_xlabel('Avg Precision')
    ax.set_title(title)

    fig.tight_layout()
    plt.close('all')

    return fig

def get_conf_dist_type6_clswise_plt(cls_to_idx, conf_dist_for_type6):
    """Generates matplotlib figure for confidence distribution of class-wise type6 errors

    Args:
        cls_to_idx (dict): mapping from class labels(str) to index (int)
        conf_dist_for_type6 (dict): keys as confidence ref points ex: 0.1, 0.4 etc.., values
                            as its corresponding count (int)

    Returns:
        fig (Figure) : The Figure instance from matplotlib pyplot (plt.figure)

    """
    num_classes = len(cls_to_idx)
    fig, axs = plt.subplots(nrows=math.ceil(num_classes/2),
                            ncols=2,
                            figsize=(1.5*num_classes, 3*num_classes))

    width = 0.05
    for i, ax in enumerate(axs.flat):
        if i >= num_classes:
            # axes has dual column. delete empty axes
            fig.delaxes(ax)
            break
        # plot rectangle bars for each error type
        rects = dict()
        conf_dist = conf_dist_for_type6[i]
        for ref_pt in conf_dist:
            rects[ref_pt] = ax.bar(ref_pt, conf_dist[ref_pt], width, color='red')
        for rect_id in rects:
            autolabel(rects[rect_id], ax)
        curr_cls_label = cls_to_idx[i]
        ax.set_title('{:s}'.format(curr_cls_label))
        ax.set_ylim(ymin=0)
        ax.set_xticks(list(conf_dist.keys()))

    for ax in axs.flat:
        ax.set(xlabel='Confidence ref points', ylabel='Number of predicted boxes nearby ref')

    fig.suptitle('Class-wise type6 error confidence distribution', y=1.02)
    fig.tight_layout()
    plt.close('all')

    return fig

def get_fine_grained_errors_clswise_plt(cls_to_idx,
                                        global_clswise_cat_errors,
                                        gt_boxes_per_class):
    """For each cls plots error types

    Args:
        cls_to_idx (dict): mapping from class labels(str) to index (int)
        global_clswise_cat_errors (dict): predicted objects distribution over 7 category error types
                                    ex: {class_id: {error_type:count,..}, ..}
        gt_boxes_per_class (dict): class label (str) to corresponding count of gt boxes (int)

    Returns:
        fig (Figure) : The Figure instance from matplotlib pyplot (plt.figure) with
        subplots of per classwise error analysis

    """
    num_classes = len(cls_to_idx)
    fig, axs = plt.subplots(nrows=math.ceil(num_classes/2),
                            ncols=2,
                            figsize=(1.5*num_classes, 3*num_classes))

    width = 0.5
    colors_labels_special = {1:('green','TP'), 7:('pink', 'FN')}
    fg_errors_cls = global_clswise_cat_errors
    for i, ax in enumerate(axs.flat):
        if i >= num_classes:
            # axes has dual column. delete empty axes
            fig.delaxes(ax)
            break
        # plot rectangle bars for each error type
        rects = dict()
        fg_errors = fg_errors_cls[i]
        for cat_id in range(1, len(fg_errors)+1):
            c,l = colors_labels_special.get(cat_id, ('red', 'FP'))
            rects[cat_id] = ax.bar(cat_id,fg_errors[cat_id], width, color=c, label=l)
        for rect_id in rects:
            autolabel(rects[rect_id], ax)
        curr_cls_label = cls_to_idx[i]
        ax.set_title('{:s} (Total {:d} GT boxes)'.format(curr_cls_label,
                                                         gt_boxes_per_class[curr_cls_label]))
        ax.set_ylim(ymin=0)
        ax.set_xticks(np.arange(1, len(fg_errors)+1))

    for ax in axs.flat:
        ax.set(xlabel='Error type', ylabel='Number of predicted boxes')

    # remove duplicate legend names
    handles, labels = axs[0][0].get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    fig.legend(by_label.values(), by_label.keys())
    fig.suptitle('Class-wise error analysis', y=1.02)
    fig.tight_layout()
    plt.close('all')

    return fig