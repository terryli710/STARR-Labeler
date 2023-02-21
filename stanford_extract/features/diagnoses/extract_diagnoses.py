import pandas as pd
from pathlib import Path
import sys

from stanford_extract.features.extract_features import extract_base

class extract_diagnoses(extract_base):
    def __init__(self, config, file_name, feature_type, save_truncated):
        super().__init__(config, file_name, feature_type, save_truncated)

    def process_data(self, pat_data):
        diagnoses_type = self.cfg['FEATURES']['TYPES']['DIAGNOSES']['TYPE']
        pat_data.loc[:, diagnoses_type] = pat_data.loc[:, diagnoses_type].str.split(',')
        pat_data = pat_data.explode(diagnoses_type).reset_index(drop=True)

        if 'INCLUDE' in self.cfg['FEATURES']['TYPES']['DIAGNOSES']:
            diagnoses_regex = "|".join(list(self.cfg['FEATURES']['TYPES']['DIAGNOSES']['INCLUDE'].keys()))
            pat_data = pat_data.loc[pat_data[diagnoses_type].str.contains(diagnoses_regex, regex = True, case = False, na = False)]
        
        pat_data = pat_data.loc[~pd.isna(pat_data.loc[:, diagnoses_type])]
        pat_data.loc[:, diagnoses_type] = pat_data.loc[:, diagnoses_type].map(lambda x: "".join(x.split('.', 1)).strip()[0:self.cfg['FEATURES']['TYPES']['DIAGNOSES']['NUM_ICD_CHARS']])
        pat_data = pat_data[['Patient Id', diagnoses_type, 'Date']]
        pat_data.loc[:, 'Value'] = 1
        pat_data = pat_data[['Patient Id', diagnoses_type, 'Value', 'Date']]
        pat_data.columns = ['Patient Id', 'Type', 'Value', 'Event_dt']
        return pat_data

    def truncate_data(self, pat_data):
        truncated = pat_data[['Patient Id', 'Date', 'ICD10 Code']]
        truncated = truncated.sort_values(by=['Patient Id'])
        return truncated


