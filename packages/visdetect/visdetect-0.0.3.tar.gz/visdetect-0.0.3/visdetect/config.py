import abc

class ConfigParam:
    def __init__(self, name, default=None, doc=None):
        self.name = name
        self.default = default
        self.__doc__ = doc

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        if self.name not in obj.params:
            return self.default

        return obj.params[self.name]

    def __set__(self, obj, value):
        raise AttributeError('Config parameter %s is readonly' % self.name)

    def __delete__(self, obj):
        raise AttributeError('Config parameter %s is readonly' % self.name)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

class Config:
    def __init__(self, overrides=None):
        self.params = {}

        if overrides is not None:
            for k, v in overrides.items():
                # Ignore the override if it's not overriding anything
                if not hasattr(self, k):
                    continue

                self.params[k] = self._try_cast(v, type(getattr(self, k)))

    def __iter__(self):
        genealogy = [self.__class__]

        # Iterate through all ConfigParam in current and parent classes
        while len(genealogy) > 0:
            cls = genealogy.pop()
            for v in cls.__dict__.values():
                if isinstance(v, ConfigParam):
                    yield v.name, getattr(self, v.name)
            genealogy += list(cls.__bases__)

    @staticmethod
    def _try_cast(obj, totype):
        """Try to cast obj to target type, but don't try too hard"""
        if totype is str:
            return str(obj)
        if totype is int:
            return int(obj)
        if totype is float:
            return float(obj)
        if totype is bool:
            if isinstance(obj, str):
                return obj.lower() in ('yes', 'true', 't', '1')
            return bool(obj)

        return obj

class VisConfig(Config, metaclass=abc.ABCMeta):
    """Configuration for visual analysis of detection task

    This class contains configuration that is used to list different type of
    fine grained FP's analysis.
    """
    iou_threshold = ConfigParam(
        'iou_threshold', 0.5,
        'IoU threshold used to create true positives, false positives,'
        'This reflects the way you want to compute mAP'
        'Generally 0.5 or 0.75 are used')

    analyse_only_global_metrics = ConfigParam(
        'analyse_only_global_metrics', False,
        'Local (per image) analysis is not performed when set to True'
        'Only global metrics like confusion matrix, error'
        'distributions over entire evaluation set and per class '
        'error distributions are analysed on Tensorboard'
        'If true then will not create image-wise mappings (local metrics)'
        'which saves time of creating cropped ROIs, gt and pred mappings '
        '(so no opencv overhead)')

    number_of_objects_per_error_global = ConfigParam(
        'number_of_objects_per_error_global', 100,
        'Over entire evaluation set (global) picks these number of objects'
        'per error category. Displays ROI pairs of predicted and '
        'ground truth.')

    # comment Duplicated.
    filter_pairs_of_error_type = ConfigParam(
        'filter_pairs_of_error_type', None,
        'Creates a new annotations.csv file in the kensho required format '
        'Either gt or pred object is chosen from these pairs based on filter_object_type '
        'argument. It has to be between 1 and 7 (both inclusive). If None then no filtering is'
        'done so no csv file would be generated')

    filter_object_type = ConfigParam(
       'filter_object_type', 'pred'
       'takes binary label either pred or gt'
        'For type 7, choosing pred would throw an error'
        'as no predictions are present in type 7 pairs')

    conf_for_type_filtering = ConfigParam(
        'conf_for_type_filtering', 0.0,
        'Threshold used to select boxes during type filtering. Should be a '
        'float between 0.0 and 1.0')