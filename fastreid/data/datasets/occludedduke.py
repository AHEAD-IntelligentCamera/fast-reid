# encoding: utf-8
"""
@author:  liaoxingyu
@contact: liaoxingyu2@jd.com
"""

import glob
import os.path as osp
import re

from .bases import ImageDataset
from ..datasets import DATASET_REGISTRY


@DATASET_REGISTRY.register()
class OccludedDuke(ImageDataset):
    """OccludedDuke.

    Reference:
        - Miao, Jiaxu, et al. Pose-guided feature alignment for occluded person re-identification. CVPR 2019.
        

    URL: `<https://github.com/layumi/DukeMTMC-reID_evaluation>` - Subset of DukeMTMC-reID dataset
    Splits: `<https://github.com/lightas/ICCV19_Pose_Guided_Occluded_Person_ReID/tree/master/dataset>`
    
    Dataset statistics:
        - identities: 1404 (train + query).
        - images:15618 (train) + 2210 (query) + 17661 (gallery).
        - cameras: 8.
    """
    dataset_dir = 'occluded_duke'
    dataset_url = None
    dataset_name = "OccludedDuke"

    def __init__(self, root='datasets', **kwargs):
        # self.root = osp.abspath(osp.expanduser(root))
        self.root = root
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')

        required_files = [
            self.dataset_dir,
            self.train_dir,
            self.query_dir,
            self.gallery_dir,
        ]
        self.check_before_run(required_files)

        train = self.process_dir(self.train_dir)
        query = self.process_dir(self.query_dir, is_train=False)
        gallery = self.process_dir(self.gallery_dir, is_train=False)

        super(OccludedDuke, self).__init__(train, query, gallery, **kwargs)

    def process_dir(self, dir_path, is_train=True):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_c(\d)')

        data = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())
            assert 1 <= camid <= 8
            camid -= 1  # index starts from 0
            if is_train:
                pid = self.dataset_name + "_" + str(pid)
                camid = self.dataset_name + "_" + str(camid)
            data.append((img_path, pid, camid))

        return data
