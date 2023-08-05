# -*- coding: utf-8 -*-
"""

:copyright: (c) 2019 by Ryerson Multimedia Lab
:license: BSD 3-clause, see LICENSE for more details.

"""

import numpy as np
import pandas as pd
from rmlhrv import tools, ecg
from rmlhrv.factory import FrequencyDomain as fd
from rmlhrv.factory import TimeDomain as td

def get_features(rpeaks, segment_duration, nni, plot=True):
    '''
        gets time domain and frequency domain features given rpeaks as an array
        plot default set to False; used to plot lomb spectrum psd
    '''
    mode='dev'
    if plot: mode='normal' #for plotting lomb_psd spectrum
    
    HR = td.hr_parameters(rpeaks=rpeaks)[0]
    AVNN  = td.nni_parameters(rpeaks=rpeaks)[1] / 1000         #put in seconds
    SDNN = td.sdnn(rpeaks=rpeaks)[0] / 1000
    SDANN = td.sdann(rpeaks=rpeaks, duration=segment_duration)[0] / 1000
    SDNNIDX = td.sdnn_index(rpeaks=rpeaks, duration=segment_duration)[0] / 1000
    RMSSD = td.rmssd(rpeaks=rpeaks)[0] / 1000
    pNN50 = td.nn50(rpeaks=rpeaks)[1] / 1000
    
    fbands = {'ulf': (0.0, 0.003), 
              'vlf': (0.003, 0.04), 
              'lf': (0.04, 0.15), 
              'hf': (0.15, 0.4)}

    if mode == 'normal':
        freq_features = fd.lomb_psd(nni, fbands=fbands, mode=mode)

    elif mode == 'dev':
        freq_features_tuple = fd.lomb_psd(nni, fbands=fbands, mode=mode)
        freq_features = freq_features_tuple[0]

    ULF, VLF, LF, HF = freq_features['lomb_peak']

    LF_HF = freq_features['lomb_ratio']
    ulf_pow, vlf_pow, _, _ = freq_features['lomb_log']
    total_pow = freq_features['lomb_total']
    TP = (ulf_pow + vlf_pow)
    features = {'HR'    : HR,
                'NNRR'  : AVNN,            
                'AVNN'  : AVNN,
                'RMSSD' : RMSSD,
                'pNN50' : pNN50, 
                'TP'    : TP,
                'ULF'   : ULF,
                'VLF'   : VLF,
                'LF'    : LF,
                'HF'    : HF, 
                'LF_HF' : LF_HF,
                'interval in seconds':AVNN # Duplicate column to match the feature set with trained classifier
                }
    return features

def run(path, pat_name, save = False, plot=True, segment_duration=30, window = 30, fs=256.): # window and segment_duration is in seconds
    raw_data = pd.read_csv(path, index_col=0, header=None)
    data = raw_data.iloc[:,1]   #ecg data is in last column
    data = data/np.max(data)
    ecg_data = np.array(data)
    ecg_data = ecg_data*-1

    time_in_s = len(ecg_data)//fs

    _, filtered, rpeaks, _, _, _, _ = ecg.ecg(ecg_data, sampling_rate=fs, show=False)
    nni = tools.nn_intervals(rpeaks.astype(float))
    rpeaks = rpeaks.astype(float).transpose()/fs

    df = pd.DataFrame()
    for i in range(int(time_in_s/window)):
        features = get_features(rpeaks[i * window: (i + 1) * window], int(fs * segment_duration), nni, plot=plot)
        if i == 0:
            df = pd.DataFrame.from_dict(features, orient='index').transpose()
        else:
            df.loc[i] = pd.Series(features).transpose()
                
    if save:
        df.to_csv(pat_name + '_30sec_features.csv')

    return df