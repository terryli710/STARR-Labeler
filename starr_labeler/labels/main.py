from pathlib import Path
import sys
from glob import glob
import os
import hydra
from typing import List, Dict, Tuple, NamedTuple, Optional

from starr_labeler.labels.label_generator import label_generator

@hydra.main(version_base=None, config_path="disease_configs/")
def main(cfg):
    labels_class = label_generator(cfg)
    labels_class.compute_diagnosis_dates()
    labels_class.compute_diagnosis_labels()
main()