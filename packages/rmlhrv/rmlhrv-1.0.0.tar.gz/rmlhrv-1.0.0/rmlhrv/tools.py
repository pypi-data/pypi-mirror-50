#!/usr/bin/env python -W ignore::FutureWarning
# -*- coding: utf-8 -*-
"""

:copyright: (c) 2018 by Pedro Gomes (HAW Hamburg)
:license: BSD 3-clause, see LICENSE for more details.
"""
from __future__ import absolute_import, division
from rmlhrv.__version__ import __version__

import os
import warnings
import json
import collections
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as dt
from rmlhrv import utils
from rmlhrv import ecg
from six.moves import range
import six

# 3rd party
import scipy.signal as ss
from scipy import interpolate, optimize
from scipy.stats import stats

# Turn off toolbox triggered warnings
WARN = False
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)


def nn_intervals(rpeaks=None):
	"""Computes the NN intervals [ms] between successive R-peaks.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-intervals-nn-intervals

	Parameter
	---------
	rpeaks : array
		R-peak times in [ms] or [s]

	Returns
	-------
	nni : array
		NN intervals in [ms]

	Raises
	------
	TypeError
		If no data provided for 'rpeaks'
	TypeError
		If data format is not list or numpy array
	TypeError
		If 'rpeaks' array contains non-integer or non-float value

	Notes
	-----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-intervals-nn-intervals

	"""
	# Check input signal
	if rpeaks is None:
		raise TypeError("No data for R-peak locations provided. Please specify input data.")
	elif type(rpeaks) is not list and not np.ndarray:
		raise TypeError("List, tuple or numpy array expected, received  %s" % type(rpeaks))

	if all(isinstance(n, int) for n in rpeaks) is False and all(isinstance(n, float) for n in rpeaks) is False:
		raise TypeError("Incompatible data type in list or numpy array detected (only int or float allowed).")

	# Confirm numpy arrays & compute NN intervals
	rpeaks = np.asarray(rpeaks)
	nn_int = np.zeros(rpeaks.size - 1)

	for i in range(nn_int.size):
		nn_int[i] = rpeaks[i + 1] - rpeaks[i]

	return nn_format(nn_int)


def nn_format(nni=None):
	"""Checks format of the NN intervals (seconds or milliseconds) and converts s data to ms data, if necessary.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-format-nn-format

	Parameters
	----------
	nni : array
		Series of NN intervals in [ms] or [s]

	Returns
	-------
	nni : array
		Series of NN intervals in [ms]

	Raises
	------
	TypeError
		If no data provided for 'nni'

	Notes
	-----
	..	You can find the documentation for this module here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-format-nn-format

	"""
	# Check input
	if nni is None:
		raise TypeError("No input data provided for 'nn'. Please specify input data")
	nn_ = np.asarray(nni, dtype='float64')

	# Convert if data has been identified in [s], else proceed with ensuring the NumPy array format
	if np.max(nn_) < 10:
		nn_ = [int(x * 1000) for x in nn_]

	return np.asarray(nn_)


def nni_diff(nni=None):
	"""Computes the series of differences between successive NN intervals [ms].

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-interval-differences-nn-diff

	Parameters
	----------
	nni : array
		NN intervals in [ms] or [s].

	Returns
	-------
	nni_diff_ : numpy array
		Difference between successive NN intervals in [ms].

	Raises
	------
	TypeError
		If no data provided for 'rpeaks'.
	TypeError
		If no list or numpy array is provided.
	TypeError
		If NN interval array contains non-integer or non-float value.

	Notes
	..	You can find the documentation for this module here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#nn-interval-differences-nn-diff

	"""
	# Check input signal
	if nni is None:
		raise TypeError("No data for R-peak locations provided. Please specify input data.")
	elif type(nni) is not list and type(nni) is not np.ndarray:
		raise TypeError("List or numpy array expected, received  %s" % type(nni))
	elif all(isinstance(x, int) for x in nni) and all(isinstance(x, float) for x in nni):
		raise TypeError("'nni' data contains non-int or non-float data.")
	else:
		nn = nn_format(nni)

	# Confirm numpy arrays & compute NN interval differences
	nn_diff_ = np.zeros(nn.size - 1)

	for i in range(nn.size - 1):
		nn_diff_[i] = abs(nn[i + 1] - nn[i])

	return np.asarray(nn_diff_)


def heart_rate(nni=None, rpeaks=None):
	"""Computes a series of Heart Rate values in [bpm] from a series of NN intervals or R-peaks in [ms] or [s] or the HR from a single NNI.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#heart-rate-heart-rate

	Parameters
	----------
	nni : int, float, array
		NN intervals in [ms] or [s].
	rpeaks : int, float, array
		R-peak times in [ms] or [s].

	Returns
	-------
	bpm : list, numpy array, float
		Heart rate computation [bpm].
		Float value if 1 NN interval has been provided
		Float array if series of NN intervals or R-peaks are provided.

	Raises
	------
	TypeError
		If no input data for 'rpeaks' or 'nn_intervals provided.
	TypeError
		If provided NN data is not provided in float, int, list or numpy array format.

	Notes
	-----
	..	You can find the documentation for this module here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#heart-rate-heart-rate

	"""
	# Check input
	if nni is None and rpeaks is not None:
		# Compute NN intervals if rpeaks array is given; only 1 interval if 2 r-peaks provided
		nni = nn_intervals(rpeaks) if len(rpeaks) > 2 else int(np.abs(rpeaks[1] - rpeaks[0]))
	elif nni is not None:
		# Use given NN intervals & confirm numpy if series of NN intervals is provided
		if type(nni) is list or type(nni) is np.ndarray:
			nni = nn_format(nni) if len(nni) > 1 else nni[0]
		elif type(nni) is int or float:
			nni = int(nni) if nni > 10 else int(nni) / 1000
	else:
		raise TypeError("No data for R-peak locations or NN intervals provided. Please specify input data.")

	# Compute heart rate data
	if type(nni) is int:
		return 60000. / float(nni)
	elif type(nni) is np.ndarray:
		return np.asarray([60000. / float(x) for x in nni])
	else:
		raise TypeError("Invalid data type. Please provide data in int, float, list or numpy array format.")


def plot_ecg(signal=None,
			 t=None,
			 sampling_rate=1000.,
			 interval=None,
			 rpeaks=True,
			 figsize=None,
			 title=None,
			 show=True):
	"""Plots ECG signal on a medical grade ECG paper-like figure layout.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#plot-ecg-plot-ecg

	Parameters
	----------
	signal : array
		ECG signal (filtered or unfiltered)
	t : array, optional
		Time vector for the ECG signal (default: None)
	sampling_rate : int, float, optional
		Sampling rate of the acquired signal in [Hz] (default: 1000Hz)
	interval : array, 2-element, optional
		Visualization interval of the ECG signal plot (default: None: [0s, 10s]
	rpeaks : bool, optional
		If True, marks R-peaks in ECG signal (default: True)
	figsize : array, optional
		Matplotlib figure size (width, height) (default: None: (12, 4))
	title : str, optional
		Plot figure title (default: None).
	show : bool, optional
		If True, shows the ECG plot figure(default: True)

	Returns
	-------
	fig_ecg : matplotlib figure object
		Matplotlib figure of ECG plot

	Raises
	------
	TypeError
		If no ECG data provided.

	Notes
	----
	..	The 'rpeaks' parameter will have no effect if there are more then 50 r-epaks within the visualization interval.
		In this case, no markers will be set to avoid overloading the plot
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#plot-ecg-plot-ecg

	"""
	# Check input data
	if signal is None:
		raise TypeError("No ECG data provided. Please specify input data.")
	else:
		# Confirm numpy
		signal = np.asarray(signal)

	# Compute time vector
	if t is None:
		t = time_vector(signal, sampling_rate=sampling_rate)

	# Configure interval of visualized signal
	interval = check_interval(interval, limits=[0, t[-1]], default=[0, 10])

	# Prepare figure
	if figsize is None:
		figsize = (12, 4)

	fig_ecg = plt.figure(figsize=figsize)
	ax = fig_ecg.add_subplot(111)

	# Configure axis according to according to BITalino ECG sensor ranges
	if signal.max() > 1.5:
		y_min = int(signal.min() - (signal.max() - signal.min()) * 0.2)
		y_max = int(signal.max() + (signal.max() - signal.min()) * 0.2)
		unit = '-'
		y_minor = np.linspace(y_min, y_max, 12)
		y_major = np.linspace(y_min, y_max, 4)
	elif signal.max() < 1.0:
		y_min, y_max = -1., 1.,
		unit = 'mV'
		y_minor = np.arange(-0.9, y_min, 0.1)
		y_major = np.arange(-1.0, y_max + 0.5, 0.5)
	else:
		y_min, y_max = -1.5, 1.5,
		unit = 'mV'
		y_minor = np.arange(-1.4, y_min, 0.1)
		y_major = np.arange(y_min, y_max + 0.5, 0.5)

	ax.axis([interval[0], interval[1], y_min, y_max])
	ax.set_xlabel('Time [$s$]')
	ax.set_ylabel('ECG [$%s$]' % unit)

	# Set ticks as ECG paper (box height ~= 0.1mV; width ~= 0.1s when using default values)
	n = int(interval[1] / 10)
	ax.set_xticks(np.arange(0.0, interval[1] + 0.1, float(n)/5), minor=True)
	ax.xaxis.grid(which='minor', color='salmon', lw=0.3)
	ax.set_xticks(np.arange(0, interval[1] + 0.1, n))
	ax.xaxis.grid(which='major', color='r', lw=0.7)
	ax.set_yticks(y_minor, minor=True)
	ax.yaxis.grid(which='minor', color='salmon', lw=0.3)
	ax.set_yticks(y_major)
	ax.yaxis.grid(which='major', color='r', lw=0.7)

	# Add legend
	unit = '' if unit == '-' else unit
	text_ = 'Division (x): %is\nDivision (y): %.1f%s' % (n, (np.abs(y_major[1] - y_major[0])), unit)
	ax.text(0.88, 0.85, text_, transform=ax.transAxes, fontsize=9,
		bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

	# Plot ECG signal
	ax.plot(t, signal, 'r')
	fig_ecg.tight_layout()

	# Plot r-peaks
	rps = ecg(signal=signal, sampling_rate=sampling_rate, show=False)[2]
	p = [float(signal[x]) for x in rps]
	r = t[rps]
	if rpeaks:
		ax.plot(r, p, 'g*', alpha=0.7)

	# Add title
	if title is not None:
		ax.set_title('ECG Signal - %s' % str(title))
	else:
		ax.set_title('ECG Signal')

	# Show plot
	if show:
		plt.show()

	# Output
	args = (fig_ecg, )
	names = ('ecg_plot', )
	return utils.ReturnTuple(args, names)


def tachogram(nni=None,
			  signal=None,
			  rpeaks=None,
			  sampling_rate=1000.,
			  hr=True,
			  interval=None,
			  title=None,
			  figsize=None,
			  show=True):
	"""Plots Tachogram (NNI & HR) of an ECG signal, NNI or R-peak series.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#tachogram-tachogram

	Parameters
	----------
	nni : array
		NN intervals in [ms] or [s].
	rpeaks : array
		R-peak times in [ms] or [s].
	signal : array, optional
		ECG signal.
	sampling_rate : int, float
		Sampling rate of the acquired signal in [Hz].
	hr : bool, optional
		If True, plots series of heart rate data in [bpm] (default: True).
	interval : list, optional
		Sets visualization interval of the signal (default: [0, 10]).
	title : str, optional
		Plot figure title (default: None).
	figsize : array, optional
		Matplotlib figure size (width, height) (default: (12, 4)).
	show : bool, optional
		If True, shows plot figure (default: True).

	Returns
	-------
	fig : matplotlib.pyplot figure
		Tachogram figure & graph

	Raises
	------
	TypeError
		If no input data for 'nni', 'rpeaks' or 'signal' is provided

	Notes
	-----
	..	NN intervals are derived from the ECG signal if 'signal' is provided.
	.. 	If both 'nni' and 'rpeaks' are provided, 'rpeaks' will be chosen over the 'nn' and the 'nni' data will be computed
		from the 'rpeaks'.
	..	If both 'nni' and 'signal' are provided, 'nni' will be chosen over 'signal'.
	..	If both 'rpeaks' and 'signal' are provided, 'rpeaks' will be chosen over 'signal'.

	"""
	# Check input
	if signal is not None:
		rpeaks = ecg(signal=signal, sampling_rate=sampling_rate, show=False)[2]
	elif nni is None and rpeaks is None:
		raise TypeError('No input data provided. Please specify input data.')

	# Get NNI series
	nni = check_input(nni, rpeaks)

	# Time vector back to ms
	t = np.cumsum(nni) / 1000.

	# Configure interval of visualized signal
	interval = check_interval(interval, limits=[0, t[-1]], default=[0, 10])

	# Prepare figure
	if figsize is None:
		figsize = (12, 4)
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(111)

	# X-Axis configuration
	# Set x-axis format to seconds if the duration of the signal <= 60s
	if interval[1] <= 60:
		ax.set_xlabel('Time [s]')
	# Set x-axis format to MM:SS if the duration of the signal > 60s and <= 1h
	elif 60 < interval[1] <= 3600:
		ax.set_xlabel('Time [MM:SS]')
		formatter = mpl.ticker.FuncFormatter(lambda ms, x: str(dt.timedelta(seconds=ms))[2:])
		ax.xaxis.set_major_formatter(formatter)
	# Set x-axis format to HH:MM:SS if the duration of the signal > 1h
	else:
		ax.set_xlabel('Time [HH:MM:SS]')
		formatter = mpl.ticker.FuncFormatter(lambda ms, x: str(dt.timedelta(seconds=ms)))
		ax.xaxis.set_major_formatter(formatter)

	n = int(interval[1] / 10)
	ax.set_xticks(np.arange(0, interval[1] + n, n))

	# Y-Axis configuration (min, max set to maximum of the visualization interval)
	ax.set_ylabel('NN Interval [$ms$]')
	nn_min = np.min(nni[np.argwhere(np.logical_and(interval[0] <= t, t <= interval[1]))])
	nn_max = np.max(nni[np.argwhere(np.logical_and(interval[0] <= t, t <= interval[1]))])
	ax.axis([interval[0], interval[1], nn_min * 0.9, nn_max * 1.1])

	# Plot 'x' markers only if less than 50 rpeaks are within the given data, otherwise don't add them
	if np.argwhere(t < interval[1]).size < 50:
		l1 = ax.plot(t, nni, color='g', label='NN Intervals', marker='x', linestyle='--', linewidth=0.8)
		ax.vlines(t, 200, 3000, linestyles='--', linewidth=0.5, alpha=0.7, colors='lightskyblue')
	else:
		l1 = ax.plot(t, nni, color='g', label='NN Intervals', linestyle='--', linewidth=0.8)
	lns = []

	# Plot heart rate signal
	if hr:
		ax2 = ax.twinx()
		bpm_values = heart_rate(nni)
		hr_min = heart_rate(nn_max)
		hr_max = heart_rate(nn_min)

		ax2.set_ylabel('Heart Rate [$1/min$]', rotation=270, labelpad=15)
		ax2.axis([interval[0], interval[1], hr_min * 0.9, hr_max * 1.1])

		# Plot 'x' markers only if less than 50 rpeaks are within the given data, otherwise don't add them
		if np.argwhere(t < interval[1]).size < 50:
			l2 = ax2.plot(t, bpm_values, color='red', label='Heart Rate', marker='x', linestyle='--', linewidth=0.8)
		else:
			l2 = ax2.plot(t, bpm_values, color='red', label='Heart Rate', linestyle='--', linewidth=0.8)
		lns = l1 + l2
		labs = [l.get_label() for l in lns]
		ax.legend(lns, labs, loc=1)
	else:
		ax.legend(loc=1)

	# Add title
	if title is not None:
		ax.set_title('Tachogram - %s' % str(title))
	else:
		ax.set_title('Tachogram')

	# Show plot
	if show:
		plt.show()

	# Output
	args = (fig,)
	names = ('tachogram_plot',)
	return utils.ReturnTuple(args, names)


def check_interval(interval=None, limits=None, default=None):
	"""General purpose function that checks and verifies correctness of interval limits within optionally defined
	valid interval specifications and and/or default values if no interval is specified.

	This function can be used to set visualization intervals, check overlapping frequency bands, or for other similar
	purposes and is intended to automatically catch possible error sources due to invalid intervals.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#check-interval-check-interval

	Parameters
	----------
	interval : array, 2-elements
		Input interval [min, max] (default: None)
	limits : array, 2-elements
		Minimum and maximum allowed interval limits (default: None)
	default : array, 2-elements
		Specified default interval (e.g. if 'interval' is None)

	Returns
	-------
	interval : array
		Valid interval limits.

	Raises
	------
	TypeError
		If no input data is specified
	ValueError
		If any of the input data has equal lower and upper limits

	Warnings
	--------
	..	If overlapping limits had to be fixed.
	..	If limits are overlapping (e.g. lower limit > upper limit)

	Notes
	-----
	(Warnings are only triggered if the module variable 'WARN' is set to 'True')
	..	If 'interval[0]' is out of boundaries ('interval[0]' < 'limit[0]' or 'interval[0]' >= 'limit[1]')
		-> sets 'interval[0] = limit[0]'
	..	If 'interval[1]' is out of boundaries ('interval[1]' <= 'limit[0]' or 'interval[1]' > 'limit[1]')
		-> sets 'interval[1] = limit[1]'
	..	If limits are overlapping (e.g. lower limit > upper limit) and had to be fixed.
	..	This thing is got unnecessarily complicated, but in the end I just went with it...
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#check-interval-check-interval

	"""
	if interval is None and limits is None and default is None:
		raise TypeError("No input data specified. Please verify your input data.")

	# Create local copy to prevent changing input variable
	interval = list(interval) if interval is not None else None

	# Check default limits
	if default is not None:
		default = _check_limits(default, 'default')

	# Check maximum range limits
	if limits is None and default is not None:
		limits = default
	elif limits is not None:
		limits = _check_limits(limits, 'limits')

	# Check interval limits
	if interval is None:
		if default is not None:
			return default
		elif default is None and limits is not None:
			return limits

	# If only interval is specified, but not 'min', 'max' or 'default' check if lower limit >= upper limit
	elif interval is not None and limits is None:
		return _check_limits(interval, 'interval')

	# If none of the input is 'None'
	else:
		# Check interval
		interval = _check_limits(interval, 'interval')
		if not limits[0] <= interval[0]:
			interval[0] = limits[0]
			if WARN:
				warnings.warn("Interval limits out of boundaries. Interval set to: %s" % interval, stacklevel=2)
		if not limits[1] >= interval[1]:
			interval[1] = limits[1]
			if WARN:
				warnings.warn("Interval limits out of boundaries. Interval set to: %s" % interval, stacklevel=2)
		return interval


def _check_limits(interval, name):
	"""Checks if interval limits are not overlapping or equal.

	Parameters
	----------
	interval : array, 2-element
		Interval boundaries [min, max].
	name : str
		Variable name to be used on exceptions and warnings.

	Returns
	-------
	interval : array, 2-element
		Valid and corrected interval limits (if correction is necessary).

	Raises
	------
	ValueError
		If interval limits are equal.

	Warnings
	--------
	..	If limits are overlapping (e.g. lower limit > upper limit) and had to be fixed.

	"""
	# upper limit < 0 or upper limit > max interval -> set upper limit to max
	if interval[0] > interval[1]:
		interval[0], interval[1] = interval[1], interval[0]
		vals = (name, name, interval[0], interval[1])
		if WARN:
			warnings.warn("Corrected invalid '%s' limits (lower limit > upper limit).'%s' set to: %s" % vals)
	if interval[0] == interval[1]:
		raise ValueError("'%f': Invalid interval limits as they are equal." % name)
	return interval


def segmentation(nni=None, full=True, overlap=False, duration=300):
	"""Segmentation of signal peaks into individual segments of set duration.
	(e.g. splitting R-peak locations into 5min segments for computation of SDNN index)

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#segmentation-segmentation

	Parameters
	----------
	nni: array
		Series of NN intervals [ms] or [s].
	full : bool, optional
		If True, returns last segment, even if the sum of NNI does not reach the segment duration (default: False).
	overlap : bool, optional
		If True, allow to return NNI that go from the interval of one segment to the successive segment (default: False).
	duration : int, optional
		Maximum duration duration per segment in [s] (default: 300s).

	Returns
	-------
	segments : array, array of arrays
		NN intervals in each segment/time interval. If cumulative sum of NN input data < duration, the NN input data
		will be returned.

	Raises
	------
	TypeError
		If no 'nni' data is not provided.

	Warnings
	--------
	If signal is shorter than the specified duration.

	Notes
	----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#segmentation-segmentation

	"""
	# Check input
	if nni is None:
		raise TypeError("Please specify input data.")

	# Preparations
	nni= nn_format(nni)
	tn = np.cumsum(nni)
	max_time = tn[-1]
	duration *= 1000			# convert from s to ms

	# Check if signal is longer than maximum segment duration
	if np.sum(nni) > duration:

		# Compute limits for each segment
		segments = []
		limits = np.arange(0, max_time + duration, duration)

		# Current index
		cindex = 0

		# Segment signals
		for i, _ in enumerate(range(0, limits.size - 1)):
			csegment = []
			while np.sum(csegment) < duration:
				csegment.append(nni[cindex])
				if cindex < nni.size - 1:
					cindex += 1
				else:
					break

			# Check if overlap exists (just to be sure)
			if np.sum(csegment) > duration:
				csegment = csegment[:-1]
				cindex -= 1

			segments.append(list(csegment))

		# Remove the last incomplete segment if required
		if not full:
			segments = segments[:-1]

		return segments, True
	else:
		if WARN:
			warnings.warn("Signal duration is to short for segmentation into %is. "
						  "Input data will be returned." % duration)
		return nni, False


def hrv_report(results=None, path=None, rfile=None, nni=None, info={}, file_format='txt', delimiter=';', hide=False, plots=False):
	"""Generates HRV report (in .txt or .csv format) of the provided HRV results.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-reports-hrv-report

	Parameters
	----------
	results : dict, biosppy.utils.ReturnTuple object
		Results of the HRV parameter computations
	rfile : str, file handler
		Absolute path of the output directory or report file handler
	nni : array, optional
		NN interval series in [ms] or [s]
	info : dict, optional
		Dictionary with HRV metadata:
		---------------------------------------------------------------
		Keys		:	Description
		---------------------------------------------------------------
		file		:	Name of the signal acquisition file.
		device		:	Acquisition device.
		identifier	:	ID of the acquisition device (e.g. MAC-address)
		fs			:	Sampling rate used during acquisition.
		resolution	:	Resolution used during acquisition.
		---------------------------------------------------------------
	file_format : str, optional
		Output file format, select 'txt' or 'csv' (default: 'txt')
	delimiter : str, optional
		Delimiter to separate the columns in the exported report (default: ';')
	hide : bool
		Hide parameters in report that have not been computed
	plots : bool, optional
		If True, save figures in results as .png file

	Returns
	-------
	rfile : str
		Absolute path of the output report file (may vary from the input file name)

	Raises
	------
	TypeError
		If no HRV results provided
	TypeError
		If no file or directory path provided
	TypeError
		If selected output file format is not supported
	IOError
		If selected file or directory does not exist

	Warnings
	--------
	..	New generated file name, if provided file does already exist

	Notes
	-----
	..	Existing files will not be overwritten, instead the new file will consist of the given file name with an
		(incremented) identifier (e.g. '_1') that will be added at the end of the provided file name.
	..	Plot figures will be saved in .png format.
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-reports-hrv-report

	"""
	SUPPORTED_FILE_FORMATS = ['txt', 'csv']
	plot_files = []

	# Check input
	if results is None:
		raise TypeError("No HRV results provided. Please specify input data.")
	if file_format not in SUPPORTED_FILE_FORMATS:
		raise TypeError("Unsupported file format. Only txt and csv formats are supported.")

	# Check path input
	if path is None:
		raise TypeError("No file name or directory provided. Please specify at least an output directory.")
	elif type(path) is str:
		if rfile is None:
			# Generate automatic file name
			rfile = 'hrv_report' + dt.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S') + '.' + file_format
			path += rfile
		else:
			# Check if file name has an compatible extension
			_, fformat = os.path.splitext(rfile)
			if fformat != file_format or fformat == '':
				path = path + rfile + '.' + file_format
			else:
				path = path + rfile
	elif os.path.isfile(path): #type(path) is file
		path_ = path.name
		path.close()
		path = path_

	if 'hrv_export' in str(path):
		path = path.replace('hrv_export', 'hrv_report')

	rfile, _ = _check_fname(path, file_format, rfile)

	# Load HRV parameters metadata
	params = json.load(open(os.path.join(os.path.split(__file__)[0], './files/hrv_keys.json'), 'r'), encoding='utf-8')

	# Prepare output dictionary
	output = {'Name': rfile}
	if 'comment' in results.keys():
		output['comment'] = results['comment']
	else:
		output['comment'] = 'n/a'

	for key in results.keys():
		if not isinstance(results[key], plt.Figure):
			# Hide 'nan' and 'n/a' values in report if preferred
			if hide and str(results[key]) in ['nan', 'n/a']:
				continue
			else:
				output[key] = results[key]
		else:
			# If matplotlib figure found, plots=True, and the figure is known in 'hrv_keys.json' -> save the figure
			if plots:
				if key in params:
					pfname = os.path.splitext(rfile)[0] + '_' + str(key)
					results[key].savefig(pfname, dpi=300)
					plot_files.append(os.path.split(pfname)[1] + '.png')

	# Metadata
	tstamp = dt.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')
	mdesc = {'file': 'File', 'device': 'Device',
			'identifier': 'Identifier/MAC', 'fs': 'Sampling Rate', 'resolution': 'Resolution', 'tstamp': 'Date Time'}
	mdata = {}

	for key in mdesc.keys():
		mdata[key] = info[key] if key in info.keys() else 'n/a'
	mdata['tstamp'] = tstamp[1:]

	# Prepare text file format
	hformat = '# %s %*s %s\n'
	cformat = '%s %*s %*s\n'
	sformat = '\n	-	%s'
	titles = {
		'time': 'Time Domain',
		'frequency_fft': 'Frequency Domain - FFT Welch\'s Method',
		'frequency_ar': 'Frequency Domain - Autoregression Method',
		'frequency_lomb': 'Frequency Domain - Lomb-Scargle Method',
		'nonlinear': 'Nonlinear Methods',
		'metadata': 'METADATA',
		'plots': 'Plots'
	}

	with open(rfile, 'w+') as f:
		# Write header
		f.write('# BIOSPPY HRV REPORT - v.%s\n' % __version__)
		for key in mdata.keys():
			f.write(hformat % (mdesc[key], 20 - len(mdesc[key]), delimiter, mdata[key]))

		# Add comment
		line = 70
		f.write('\n\n%s\n%s\n%s\n%s\n' % (line * '-', 'COMMENTS', output['comment'], line * '-'))

		# Prepare content
		content = dict()
		for key in params.keys():
			if 'plot' not in str(key):
				key = str(key)

				# Prepare parameter label & units
				if key not in ['comment', 'Name']:
					label = str(params[key][1]) + (' (%s)' % params[key][2])

					# Select output parameters (to report file)
					if key in output.keys() and 'plot' not in str(key) and 'histogram' not in str(key):
						if str(output[key]) in ['nan', 'n/a'] and hide:
							continue
						else:
							para = output[key]
							out = ''
							if isinstance(para, collections.Iterable) and type(para) is not str:
								for i, val in enumerate(list(para)):
									if val is str or np.nan:
										val_ = str(val) if val not in ['n/a', 'nan'] else 'n/a'
									elif val == float:
										val_ = '%.3f' % val if val not in ['n/a', 'nan'] else 'n/a'
									out += sformat % val_
							elif type(para) is str:
								out = '%s' % output[key] if output[key] not in ['n/a', 'nan', None] else 'n/a'
							else:
								out = '%.3f' % output[key] if output[key] not in ['n/a', 'nan', None] else 'n/a'
						content[key] = cformat % (label, 50 - len(label), delimiter, 1, out)
					elif not hide:
						content[key] = cformat % (label, 50-len(label), delimiter, 1, 'n/a')
				else:
					content['comment'] = output[key]

		# Write output to report file
		current_domain = []

		# Go through all parameters in 'hrv_keys.json'
		for n in range(1, len(params.keys()) - 1):
			# Go through content
			for key in content.keys():
				# Check keys by specified order set in the last element of each entry in 'hrv_keys.json'
				if params[key][-1] == n:
					# Set parameter title in output file (Time Domain, Frequency Domain, etc.)
					if current_domain != params[key][0] and str(key) not in ['nn_intervals']:
						current_domain = params[key][0]
						if current_domain != 'plot':
							f.write('\n\n%s\n%s\n%s\n' % (line * '-', titles[current_domain], line * '-'))

					# Finally, write parameter content to output file
					f.write(content[key])

		# Add generated plot figures (file names to facilitate the link between report files and plot figures)
		if plots:
			f.write('\n\n%s\n%s\n%s\n' % (line * '-', 'Plot Figure Files', line * '-'))
			for plot in plot_files:
				f.write('%s\n' % plot)

		# Add NNI if desired
		if nni is not None:
			f.write('\n\n%s\n' % params['nn_intervals'][1])
			for i in nni:
				f.write('%.3f\n ' % i)

	return rfile


def hrv_export(results=None, path=None, efile=None, comment=None, plots=False):
	"""
	Exports HRV results into a JSON file.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-export-hrv-export

	Parameters
	----------
	results : dict, biosppy.utils.ReturnTuple object
		Results of the HRV analysis
	path : str
		Absolute path of the output directory
	efile : str, optional
		Output file name
	comment : str, optional
		Optional comment
	plots : bool, optional
		If True, save figures of the results in .png format

	Returns
	-------
	efile : str
		Absolute path of the output export file (may vary from the input data)

	Raises
	------
	TypeError
		No input data provided
	TypeError
		Unsupported data format provided (other than dict, or utils.ReturnTuple object.)
	TypeError
		If no file or directory path provided

	Notes
	-----
	..	If 'path' is a file handler, 'efile' will be ignored.
	..	Creates file with automatic name generation if only an output path is provided.
	..	Output file name may vary from input file name due changes made to avoid overwrting existing files (your
		results are important after all!).
	..	Existing files will not be overwritten, instead the new file will consist of the given file name with an
		(incremented) identifier (e.g. '_1') that will be added at the end of the provided file name.
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-export-hrv-export

	"""
	# Check input (if available & utils.ReturnTuple object)
	if results is None:
		raise TypeError("No results data provided. Please specify input data.")
	elif results is not type(dict()) and isinstance(results, utils.ReturnTuple) is False:
		raise TypeError("Unsupported data format: %s. "
						"Please provide input data as Python dictionary or biosppy.utils.ReturnTuple object." % type(results))

	if path is None:
		raise TypeError("No file name or directory provided. Please specify at least an output directory.")
	elif type(path) is str:
		if efile is None:
			# Generate automatic file name
			efile = 'hrv_export' + dt.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S') + '.json'
			path += efile
		else:
			# Check if file name has an '.json' extension
			_, fformat = os.path.splitext(efile)
			if fformat != 'json':
				path = path + efile + '.json'
			else:
				path = path + efile
	elif os.path.isfile(path): #type(path) is file
		path_ = path.name
		path.close()
		path = path_

	efile, _ = _check_fname(path, 'json', efile)

	# Get HRV parameters
	params = json.load(open(os.path.join(os.path.split(__file__)[0], './files/hrv_keys.json'), 'r'))

	# Save plot figures
	if plots:
		for key in results.keys():
			if isinstance(results[key], plt.Figure) and key in params.keys():
				results[key].savefig(os.path.splitext(efile)[0] + '_' + str(key), dpi=300)

	# Prepare output dictionary
	output = {'Name': efile, 'Comment': str(comment)}
	for key in results.keys():
		if 'plot' not in str(key) and 'histogram' not in str(key):
			output[key] = results[key] if str(results[key]) != 'nan' else 'n/a'

	# Write output dictionary to JSON file
	json.encoder.FLOAT_REPR = lambda o: format(o, 'f')
	with open(efile, 'w+') as f:
		json.dump(output, f, sort_keys=True, indent=4, separators=(',', ': '))

	return str(efile)


def hrv_import(hrv_file=None):
	"""Imports HRV results stored in JSON files generated with the 'hrv_export()' function.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-import-hrv-import

	Parameters
	----------
	hrv_file : file object, str
		File handler or absolute string path of the HRV JSON file

	Returns
	-------
	output : biosppy.utils.ReturnTuple object
		All imported results.

	Raises
	------
	TypeError
		No input data provided.

	Notes
	-----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#hrv-import-hrv-import

	"""
	# Check input data and load JSON file content
	if hrv_file is None:
		raise TypeError("No input data provided. Please specify input data.")
	elif type(hrv_file) is str:
		data = json.load(open(hrv_file, 'r'))
	elif os.path.isfile(hrv_file): #isinstance(hrv_file, file)
		data = json.load(hrv_file)

	results = dict()
	for key in data.keys():
		results[str(key)] = data[key] if type(data[key]) is not np.unicode else str(data[key])

	# Create utils.ReturnTuple object from imported data
	return utils.ReturnTuple(results.values(), results.keys())


def join_tuples(*args):
	"""Joins multiple biosppy.utils.ReturnTuple objects into one biosppy.utils.ReturnTuple object.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#join-tuples-join-tuples

	Parameters
	----------
	tuples : list, array, utils.ReturnTuple objects
		List or array containing utils.ReturnTuple objects.

	Returns
	-------
	return_tuple : biosppy.utils.ReturnTuple object
		biosppy.utils.ReturnTuple object with the content of all input tuples joined together.

	Raises
	------
	TypeError:
		If no input data is provided
	TypeError:
		If input data contains non-biosppy.utils.ReturnTuple objects

	Notes
	----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#join-tuples-join-tuples

	"""
	# Check input
	if args is None:
		raise TypeError("Please specify input data.")

	for i in args:
		if not isinstance(i, utils.ReturnTuple):
			raise TypeError("The list of tuples contains non-utils.ReturnTuple objects.")

	# Join tuples
	names = ()
	vals = ()

	for i in args:
		for key in i.keys():
			names = names + (key, )
			vals = vals + (i[key], )

	return utils.ReturnTuple(vals, names)


def _check_fname(rfile, fformat='txt', name='new_file'):
	"""Checks if file or path exists and creates new file with a given suffix or incrementing identifier at the end of
	the file name to avoid overwriting existing files.

	Parameters
	----------
	rfile : str
		Absolute file path or directory.
	fformat : str
		File format (e.g. 'txt').
	name : str
		File name for newly created file if only directory is provided.

	Returns
	-------
	rfile : str
		Absolute file path of a new file.

	Raises
	------
	IOError
		If file or directory does not exist.

	Warnings
	--------
	..	New generated file name, if provided file does already exist.

	Notes
	-----
	..	Existing files will not be overwritten, instead the new file will consist of the given file name with an
		(incremented) identifier (e.g. '_1') that will be added at the end of the provided file name.
	..	If only directory provided, the new file name will consist of the provided 'name' string.

	"""
	# Prepare path data
	fformat = '.' + fformat

	# Check if 'rfile' is a path name or path + file name
	if os.path.isdir(rfile) and not os.path.isfile(rfile + name + fformat):
		rfile = rfile + name + fformat
	elif os.path.isfile(rfile):
		old_rfile = rfile

		# Increment file identifier until an available file name has been found
		while(os.path.isfile(rfile)):
			rfile, format = os.path.splitext(rfile)

			# check for duplicate file name and create new file with (incremented) number at the end
			if rfile[-3:-1].isdigit():
				rfile = rfile[:-3] + str(int(rfile[-3:]) + 1)
			elif rfile[-2:-1].isdigit():
				rfile = rfile[:-2] + str(int(rfile[-2:]) + 1)
			elif rfile[-1].isdigit():
				rfile = rfile[:-1] + str(int(rfile[-1:]) + 1)
			elif rfile[-1].isdigit and rfile[-1] != '_':
				rfile += '_1'
			rfile += ('%s' % fformat)

		# Show warning if file does already exist
		msg = "\nFile '%s' does already exist." \
			  "New file name '%s' selected to avoid overwriting existing files." % (old_rfile, rfile)
		warnings.warn(msg, stacklevel=2)
	elif not os.path.isfile(rfile):
		rfile = os.path.splitext(rfile)[0] + fformat
		with open(rfile, 'w+'):
			pass
	else:
		raise IOError("File or directory does not exist. Please verify input data.")

	return rfile, os.path.split(rfile)


def std(array, dof=1):
	"""Computes the standard deviation of a data series.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#standard-deviation-std

	Parameters
	----------
	array : list, numpy array
		Data series.
	dof : int
		Degree of freedom (default to 1).

	Returns
	-------
	result : float
		Standard deviation of the input data series

	Raises
	------
	TypeError
		If input array is not specified

	Notes
	-----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#standard-deviation-std

	"""
	if array is None:
		raise TypeError("Please specify input data.")

	array = np.asarray(array)
	result = np.sum([(x - np.mean(array))**2 for x in array])
	result = np.sqrt(1. / (array.size - dof) * result)
	return result


def time_vector(signal=None, sampling_rate=1000.):
	"""Computes time vector for the provided input signal.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#time-vector-time-vector

	Parameters
	----------
	signal : array
		ECG signal (or any other sensor signal)
	sampling_rate : int, float, optional
		Sampling rate of the input signal in [Hz]

	Returns
	-------
	time_vector : array
		Time vector for the input signal sampled at the input 'sampling_rate'

	Raises
	------
	TypeError
		If input signal is not specified.

	Notes
	-----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#time-vector-time-vector

	"""
	if signal is None:
		raise TypeError("Please specify input signal.")

	signal = np.asarray(signal)
	t = np.arange(0, signal.size / sampling_rate, 1./sampling_rate)
	return t


def check_input(nni=None, rpeaks=None):
	"""Checks if input series of NN intervals or R-peaks are provided and, if yes, returns a NN interval series in [ms]
	format.

	Docs:	https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#check-input-check-input

	Parameters
	----------
	nni : array, int
		NN intervals in [ms] or [s].
	rpeaks : array, int
		R-peak times in [ms] or [s].

	Returns
	-------
	nni : array
		NN interval series [ms].

	Raises
	------
	TypeError
		If no input data for 'nni' and 'rpeaks' provided.

	Notes
	-----
	..	You can find the documentation for this function here:
		https://rmlhrv.readthedocs.io/en/latest/_pages/api/tools.html#check-input-check-input

	"""
	# Check input
	if nni is None and rpeaks is not None:
		# Compute NN intervals if r_peaks array is given
		nni = nn_intervals(rpeaks)
	elif nni is not None:
		# Use given NN intervals & confirm numpy
		nni = nn_format(nni)
	else:
		raise TypeError("No R-peak data or NN intervals provided. Please specify input data.")
	return nni


def _norm_freq(frequency=None, sampling_rate=1000.):
	"""Normalize frequency to Nyquist Frequency (Fs/2).

    Parameters
    ----------
    frequency : int, float, list, array
        Frequencies to normalize.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).

    Returns
    -------
    wn : float, array
        Normalized frequencies.

    """

	# check inputs
	if frequency is None:
		raise TypeError("Please specify a frequency to normalize.")

	# convert inputs to correct representation
	try:
		frequency = float(frequency)
	except TypeError:
		# maybe frequency is a list or array
		frequency = np.array(frequency, dtype='float')

	Fs = float(sampling_rate)

	wn = 2. * frequency / Fs

	return wn


def _filter_init(b, a, alpha=1.):
	"""Get an initial filter state that corresponds to the steady-state
    of the step response.

    Parameters
    ----------
    b : array
        Numerator coefficients.
    a : array
        Denominator coefficients.
    alpha : float, optional
        Scaling factor.

    Returns
    -------
    zi : array
        Initial filter state.

    """

	zi = alpha * ss.lfilter_zi(b, a)

	return zi


def _filter_signal(b, a, signal, zi=None, check_phase=True, **kwargs):
	"""Filter a signal with given coefficients.

    Parameters
    ----------
    b : array
        Numerator coefficients.
    a : array
        Denominator coefficients.
    signal : array
        Signal to filter.
    zi : array, optional
        Initial filter state.
    check_phase : bool, optional
        If True, use the forward-backward technique.
    ``**kwargs`` : dict, optional
        Additional keyword arguments are passed to the underlying filtering
        function.

    Returns
    -------
    filtered : array
        Filtered signal.
    zf : array
        Final filter state.

    Notes
    -----
    * If check_phase is True, zi cannot be set.

    """

	# check inputs
	if check_phase and zi is not None:
		raise ValueError(
			"Incompatible arguments: initial filter state cannot be set when \
            check_phase is True.")

	if zi is None:
		zf = None
		if check_phase:
			filtered = ss.filtfilt(b, a, signal, **kwargs)
		else:
			filtered = ss.lfilter(b, a, signal, **kwargs)
	else:
		filtered, zf = ss.lfilter(b, a, signal, zi=zi, **kwargs)

	return filtered, zf


def _filter_resp(b, a, sampling_rate=1000., nfreqs=4096):
	"""Compute the filter frequency response.

    Parameters
    ----------
    b : array
        Numerator coefficients.
    a : array
        Denominator coefficients.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    nfreqs : int, optional
        Number of frequency points to compute.

    Returns
    -------
    freqs : array
        Array of frequencies (Hz) at which the response was computed.
    resp : array
        Frequency response.

    """

	w, resp = ss.freqz(b, a, nfreqs)

	# convert frequencies
	freqs = w * sampling_rate / (2. * np.pi)

	return freqs, resp


def _get_window(kernel, size, **kwargs):
	"""Return a window with the specified parameters.

    Parameters
    ----------
    kernel : str
        Type of window to create.
    size : int
        Size of the window.
    ``**kwargs`` : dict, optional
        Additional keyword arguments are passed to the underlying
        scipy.signal.windows function.

    Returns
    -------
    window : array
        Created window.

    """

	# mimics scipy.signal.get_window
	if kernel in ['blackman', 'black', 'blk']:
		winfunc = ss.blackman
	elif kernel in ['triangle', 'triang', 'tri']:
		winfunc = ss.triang
	elif kernel in ['hamming', 'hamm', 'ham']:
		winfunc = ss.hamming
	elif kernel in ['bartlett', 'bart', 'brt']:
		winfunc = ss.bartlett
	elif kernel in ['hanning', 'hann', 'han']:
		winfunc = ss.hann
	elif kernel in ['blackmanharris', 'blackharr', 'bkh']:
		winfunc = ss.blackmanharris
	elif kernel in ['parzen', 'parz', 'par']:
		winfunc = ss.parzen
	elif kernel in ['bohman', 'bman', 'bmn']:
		winfunc = ss.bohman
	elif kernel in ['nuttall', 'nutl', 'nut']:
		winfunc = ss.nuttall
	elif kernel in ['barthann', 'brthan', 'bth']:
		winfunc = ss.barthann
	elif kernel in ['flattop', 'flat', 'flt']:
		winfunc = ss.flattop
	elif kernel in ['kaiser', 'ksr']:
		winfunc = ss.kaiser
	elif kernel in ['gaussian', 'gauss', 'gss']:
		winfunc = ss.gaussian
	elif kernel in ['general gaussian', 'general_gaussian', 'general gauss',
					'general_gauss', 'ggs']:
		winfunc = ss.general_gaussian
	elif kernel in ['boxcar', 'box', 'ones', 'rect', 'rectangular']:
		winfunc = ss.boxcar
	elif kernel in ['slepian', 'slep', 'optimal', 'dpss', 'dss']:
		winfunc = ss.slepian
	elif kernel in ['cosine', 'halfcosine']:
		winfunc = ss.cosine
	elif kernel in ['chebwin', 'cheb']:
		winfunc = ss.chebwin
	else:
		raise ValueError("Unknown window type.")

	try:
		window = winfunc(size, **kwargs)
	except TypeError as e:
		raise TypeError("Invalid window arguments: %s." % e)

	return window


def get_filter(ftype='FIR',
			   band='lowpass',
			   order=None,
			   frequency=None,
			   sampling_rate=1000., **kwargs):
	"""Compute digital (FIR or IIR) filter coefficients with the given
    parameters.

    Parameters
    ----------
    ftype : str
        Filter type:
            * Finite Impulse Response filter ('FIR');
            * Butterworth filter ('butter');
            * Chebyshev filters ('cheby1', 'cheby2');
            * Elliptic filter ('ellip');
            * Bessel filter ('bessel').
    band : str
        Band type:
            * Low-pass filter ('lowpass');
            * High-pass filter ('highpass');
            * Band-pass filter ('bandpass');
            * Band-stop filter ('bandstop').
    order : int
        Order of the filter.
    frequency : int, float, list, array
        Cutoff frequencies; format depends on type of band:
            * 'lowpass' or 'highpass': single frequency;
            * 'bandpass' or 'bandstop': pair of frequencies.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    ``**kwargs`` : dict, optional
        Additional keyword arguments are passed to the underlying
        scipy.signal function.

    Returns
    -------
    b : array
        Numerator coefficients.
    a : array
        Denominator coefficients.

    See Also:
        scipy.signal

    """

	# check inputs
	if order is None:
		raise TypeError("Please specify the filter order.")
	if frequency is None:
		raise TypeError("Please specify the cutoff frequency.")
	if band not in ['lowpass', 'highpass', 'bandpass', 'bandstop']:
		raise ValueError(
			"Unknown filter type '%r'; choose 'lowpass', 'highpass', \
            'bandpass', or 'bandstop'."
			% band)

	# convert frequencies
	frequency = _norm_freq(frequency, sampling_rate)

	# get coeffs
	b, a = [], []
	if ftype == 'FIR':
		# FIR filter
		if order % 2 == 0:
			order += 1
		a = np.array([1])
		if band in ['lowpass', 'bandstop']:
			b = ss.firwin(numtaps=order,
						  cutoff=frequency,
						  pass_zero=True, **kwargs)
		elif band in ['highpass', 'bandpass']:
			b = ss.firwin(numtaps=order,
						  cutoff=frequency,
						  pass_zero=False, **kwargs)
	elif ftype == 'butter':
		# Butterworth filter
		b, a = ss.butter(N=order,
						 Wn=frequency,
						 btype=band,
						 analog=False,
						 output='ba', **kwargs)
	elif ftype == 'cheby1':
		# Chebyshev type I filter
		b, a = ss.cheby1(N=order,
						 Wn=frequency,
						 btype=band,
						 analog=False,
						 output='ba', **kwargs)
	elif ftype == 'cheby2':
		# chebyshev type II filter
		b, a = ss.cheby2(N=order,
						 Wn=frequency,
						 btype=band,
						 analog=False,
						 output='ba', **kwargs)
	elif ftype == 'ellip':
		# Elliptic filter
		b, a = ss.ellip(N=order,
						Wn=frequency,
						btype=band,
						analog=False,
						output='ba', **kwargs)
	elif ftype == 'bessel':
		# Bessel filter
		b, a = ss.bessel(N=order,
						 Wn=frequency,
						 btype=band,
						 analog=False,
						 output='ba', **kwargs)

	return utils.ReturnTuple((b, a), ('b', 'a'))


def filter_signal(signal=None,
				  ftype='FIR',
				  band='lowpass',
				  order=None,
				  frequency=None,
				  sampling_rate=1000., **kwargs):
	"""Filter a signal according to the given parameters.

    Parameters
    ----------
    signal : array
        Signal to filter.
    ftype : str
        Filter type:
            * Finite Impulse Response filter ('FIR');
            * Butterworth filter ('butter');
            * Chebyshev filters ('cheby1', 'cheby2');
            * Elliptic filter ('ellip');
            * Bessel filter ('bessel').
    band : str
        Band type:
            * Low-pass filter ('lowpass');
            * High-pass filter ('highpass');
            * Band-pass filter ('bandpass');
            * Band-stop filter ('bandstop').
    order : int
        Order of the filter.
    frequency : int, float, list, array
        Cutoff frequencies; format depends on type of band:
            * 'lowpass' or 'bandpass': single frequency;
            * 'bandpass' or 'bandstop': pair of frequencies.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    ``**kwargs`` : dict, optional
        Additional keyword arguments are passed to the underlying
        scipy.signal function.

    Returns
    -------
    signal : array
        Filtered signal.
    sampling_rate : float
        Sampling frequency (Hz).
    params : dict
        Filter parameters.

    Notes
    -----
    * Uses a forward-backward filter implementation. Therefore, the combined
      filter has linear phase.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify a signal to filter.")

	# get filter
	b, a = get_filter(ftype=ftype,
					  order=order,
					  frequency=frequency,
					  sampling_rate=sampling_rate,
					  band=band, **kwargs)

	# filter
	filtered, _ = _filter_signal(b, a, signal, check_phase=True)

	# output
	params = {
		'ftype': ftype,
		'order': order,
		'frequency': frequency,
		'band': band,
	}
	params.update(kwargs)

	args = (filtered, sampling_rate, params)
	names = ('signal', 'sampling_rate', 'params')

	return utils.ReturnTuple(args, names)


class OnlineFilter(object):
	"""Online filtering.

    Parameters
    ----------
    b : array
        Numerator coefficients.
    a : array
        Denominator coefficients.

    """

	def __init__(self, b=None, a=None):
		# check inputs
		if b is None:
			raise TypeError('Please specify the numerator coefficients.')

		if a is None:
			raise TypeError('Please specify the denominator coefficients.')

		# self things
		self.b = b
		self.a = a

		# reset
		self.reset()

	def reset(self):
		"""Reset the filter state."""

		self.zi = None

	def filter(self, signal=None):
		"""Filter a signal segment.

        Parameters
        ----------
        signal : array
            Signal segment to filter.

        Returns
        -------
        filtered : array
            Filtered signal segment.

        """

		# check input
		if signal is None:
			raise TypeError('Please specify the input signal.')

		if self.zi is None:
			self.zi = signal[0] * ss.lfilter_zi(self.b, self.a)

		filtered, self.zi = ss.lfilter(self.b, self.a, signal, zi=self.zi)

		return utils.ReturnTuple((filtered,), ('filtered',))


def smoother(signal=None, kernel='boxzen', size=10, mirror=True, **kwargs):
	"""Smooth a signal using an N-point moving average [MAvg]_ filter.

    This implementation uses the convolution of a filter kernel with the input
    signal to compute the smoothed signal [Smit97]_.

    Availabel kernels: median, boxzen, boxcar, triang, blackman, hamming, hann,
    bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann,
    kaiser (needs beta), gaussian (needs std), general_gaussian (needs power,
    width), slepian (needs width), chebwin (needs attenuation).

    Parameters
    ----------
    signal : array
        Signal to smooth.
    kernel : str, array, optional
        Type of kernel to use; if array, use directly as the kernel.
    size : int, optional
        Size of the kernel; ignored if kernel is an array.
    mirror : bool, optional
        If True, signal edges are extended to avoid boundary effects.
    ``**kwargs`` : dict, optional
        Additional keyword arguments are passed to the underlying
        scipy.signal.windows function.

    Returns
    -------
    signal : array
        Smoothed signal.
    params : dict
        Smoother parameters.

    Notes
    -----
    * When the kernel is 'median', mirror is ignored.

    References
    ----------
    .. [MAvg] Wikipedia, "Moving Average",
       http://en.wikipedia.org/wiki/Moving_average
    .. [Smit97] S. W. Smith, "Moving Average Filters - Implementation by
       Convolution", http://www.dspguide.com/ch15/1.htm, 1997

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify a signal to smooth.")

	length = len(signal)

	if isinstance(kernel, six.string_types):
		# check length
		if size > length:
			size = length - 1

		if size < 1:
			size = 1

		if kernel == 'boxzen':
			# hybrid method
			# 1st pass - boxcar kernel
			aux, _ = smoother(signal,
							  kernel='boxcar',
							  size=size,
							  mirror=mirror)

			# 2nd pass - parzen kernel
			smoothed, _ = smoother(aux,
								   kernel='parzen',
								   size=size,
								   mirror=mirror)

			params = {'kernel': kernel, 'size': size, 'mirror': mirror}

			args = (smoothed, params)
			names = ('signal', 'params')

			return utils.ReturnTuple(args, names)

		elif kernel == 'median':
			# median filter
			if size % 2 == 0:
				raise ValueError(
					"When the kernel is 'median', size must be odd.")

			smoothed = ss.medfilt(signal, kernel_size=size)

			params = {'kernel': kernel, 'size': size, 'mirror': mirror}

			args = (smoothed, params)
			names = ('signal', 'params')

			return utils.ReturnTuple(args, names)

		else:
			win = _get_window(kernel, size, **kwargs)

	elif isinstance(kernel, np.ndarray):
		win = kernel
		size = len(win)

		# check length
		if size > length:
			raise ValueError("Kernel size is bigger than signal length.")

		if size < 1:
			raise ValueError("Kernel size is smaller than 1.")

	else:
		raise TypeError("Unknown kernel type.")

	# convolve
	w = win / win.sum()
	if mirror:
		aux = np.concatenate(
			(signal[0] * np.ones(size), signal, signal[-1] * np.ones(size)))
		smoothed = np.convolve(w, aux, mode='same')
		smoothed = smoothed[size:-size]
	else:
		smoothed = np.convolve(w, signal, mode='same')

	# output
	params = {'kernel': kernel, 'size': size, 'mirror': mirror}
	params.update(kwargs)

	args = (smoothed, params)
	names = ('signal', 'params')

	return utils.ReturnTuple(args, names)


def analytic_signal(signal=None, N=None):
	"""Compute analytic signal, using the Hilbert Transform.

    Parameters
    ----------
    signal : array
        Input signal.
    N : int, optional
        Number of Fourier components; default is `len(signal)`.

    Returns
    -------
    amplitude : array
        Amplitude envelope of the analytic signal.
    phase : array
        Instantaneous phase component of the analystic signal.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	# hilbert transform
	asig = ss.hilbert(signal, N=N)

	# amplitude envelope
	amp = np.absolute(asig)

	# instantaneous
	phase = np.angle(asig)

	return utils.ReturnTuple((amp, phase), ('amplitude', 'phase'))


def phase_locking(signal1=None, signal2=None, N=None):
	"""Compute the Phase-Locking Factor (PLF) between two signals.

    Parameters
    ----------
    signal1 : array
        First input signal.
    signal2 : array
        Second input signal.
    N : int, optional
        Number of Fourier components.

    Returns
    -------
    plf : float
        The PLF between the two signals.

    """

	# check inputs
	if signal1 is None:
		raise TypeError("Please specify the first input signal.")

	if signal2 is None:
		raise TypeError("Please specify the second input signal.")

	if len(signal1) != len(signal2):
		raise ValueError("The input signals must have the same length.")

	# compute analytic signal
	asig1 = ss.hilbert(signal1, N=N)
	phase1 = np.angle(asig1)

	asig2 = ss.hilbert(signal2, N=N)
	phase2 = np.angle(asig2)

	# compute PLF
	plf = np.absolute(np.mean(np.exp(1j * (phase1 - phase2))))

	return utils.ReturnTuple((plf,), ('plf',))


def power_spectrum(signal=None,
				   sampling_rate=1000.,
				   pad=None,
				   pow2=False,
				   decibel=True):
	"""Compute the power spectrum of a signal (one-sided).

    Parameters
    ----------
    signal : array
        Input signal.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    pad : int, optional
        Padding for the Fourier Transform (number of zeros added);
        defaults to no padding..
    pow2 : bool, optional
        If True, rounds the number of points `N = len(signal) + pad` to the
        nearest power of 2 greater than N.
    decibel : bool, optional
        If True, returns the power in decibels.

    Returns
    -------
    freqs : array
        Array of frequencies (Hz) at which the power was computed.
    power : array
        Power spectrum.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	npoints = len(signal)

	if pad is not None:
		if pad >= 0:
			npoints += pad
		else:
			raise ValueError("Padding must be a positive integer.")

	# power of 2
	if pow2:
		npoints = 2 ** (np.ceil(np.log2(npoints)))

	Nyq = float(sampling_rate) / 2
	hpoints = npoints // 2

	freqs = np.linspace(0, Nyq, hpoints)
	power = np.abs(np.fft.fft(signal, npoints)) / npoints

	# one-sided
	power = power[:hpoints]
	power[1:] *= 2
	power = np.power(power, 2)

	if decibel:
		power = 10. * np.log10(power)

	return utils.ReturnTuple((freqs, power), ('freqs', 'power'))


def welch_spectrum(signal=None,
				   sampling_rate=1000.,
				   size=None,
				   overlap=None,
				   window='hanning',
				   window_kwargs=None,
				   pad=None,
				   decibel=True):
	"""Compute the power spectrum of a signal using Welch's method (one-sided).

    Parameters
    ----------
    signal : array
        Input signal.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    size : int, optional
        Number of points in each Welch segment;
        defaults to the equivalent of 1 second;
        ignored when 'window' is an array.
    overlap : int, optional
        Number of points to overlap between segments; defaults to `size / 2`.
    window : str, array, optional
        Type of window to use.
    window_kwargs : dict, optional
        Additional keyword arguments to pass on window creation; ignored if
        'window' is an array.
    pad : int, optional
        Padding for the Fourier Transform (number of zeros added);
        defaults to no padding.
    decibel : bool, optional
        If True, returns the power in decibels.

    Returns
    -------
    freqs : array
        Array of frequencies (Hz) at which the power was computed.
    power : array
        Power spectrum.

    Notes
    -----
    * Detrends each Welch segment by removing the mean.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	length = len(signal)
	sampling_rate = float(sampling_rate)

	if size is None:
		size = int(sampling_rate)

	if window_kwargs is None:
		window_kwargs = {}

	if isinstance(window, six.string_types):
		win = _get_window(window, size, **window_kwargs)
	elif isinstance(window, np.ndarray):
		win = window
		size = len(win)

	if size > length:
		raise ValueError('Segment size must be smaller than signal length.')

	if overlap is None:
		overlap = size // 2
	elif overlap > size:
		raise ValueError('Overlap must be smaller than segment size.')

	nfft = size
	if pad is not None:
		if pad >= 0:
			nfft += pad
		else:
			raise ValueError("Padding must be a positive integer.")

	freqs, power = ss.welch(
		signal,
		fs=sampling_rate,
		window=win,
		nperseg=size,
		noverlap=overlap,
		nfft=nfft,
		detrend='constant',
		return_onesided=True,
		scaling='spectrum',
	)

	# compensate one-sided
	power *= 2

	if decibel:
		power = 10. * np.log10(power)

	return utils.ReturnTuple((freqs, power), ('freqs', 'power'))


def band_power(freqs=None, power=None, frequency=None, decibel=True):
	"""Compute the avearge power in a frequency band.

    Parameters
    ----------
    freqs : array
        Array of frequencies (Hz) at which the power was computed.
    power : array
        Input power spectrum.
    frequency : list, array
        Pair of frequencies defining the band.
    decibel : bool, optional
        If True, input power is in decibels.

    Returns
    -------
    avg_power : float
        The average power in the band.

    """

	# check inputs
	if freqs is None:
		raise TypeError("Please specify the 'freqs' array.")

	if power is None:
		raise TypeError("Please specify the input power spectrum.")

	if len(freqs) != len(power):
		raise ValueError(
			"The input 'freqs' and 'power' arrays must have the same length.")

	if frequency is None:
		raise TypeError("Please specify the band frequencies.")

	try:
		f1, f2 = frequency
	except ValueError:
		raise ValueError("Input 'frequency' must be a pair of frequencies.")

	# make frequencies sane
	if f1 > f2:
		f1, f2 = f2, f1

	if f1 < freqs[0]:
		f1 = freqs[0]
	if f2 > freqs[-1]:
		f2 = freqs[-1]

	# average
	sel = np.nonzero(np.logical_and(f1 <= freqs, freqs <= f2))[0]

	if decibel:
		aux = 10 ** (power / 10.)
		avg = np.mean(aux[sel])
		avg = 10. * np.log10(avg)
	else:
		avg = np.mean(power[sel])

	return utils.ReturnTuple((avg,), ('avg_power',))


def signal_stats(signal=None):
	"""Compute various metrics describing the signal.

    Parameters
    ----------
    signal : array
        Input signal.

    Returns
    -------
    mean : float
        Mean of the signal.
    median : float
        Median of the signal.
    min : float
        Minimum signal value.
    max : float
        Maximum signal value.
    max_amp : float
        Maximum absolute signal amplitude, in relation to the mean.
    var : float
        Signal variance (unbiased).
    std_dev : float
        Standard signal deviation (unbiased).
    abs_dev : float
        Mean absolute signal deviation around the median.
    kurtosis : float
        Signal kurtosis (unbiased).
    skew : float
        Signal skewness (unbiased).

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	# ensure numpy
	signal = np.array(signal)

	# mean
	mean = np.mean(signal)

	# median
	median = np.median(signal)

	# min
	minVal = np.min(signal)

	# max
	maxVal = np.max(signal)

	# maximum amplitude
	maxAmp = np.abs(signal - mean).max()

	# variance
	sigma2 = signal.var(ddof=1)

	# standard deviation
	sigma = signal.std(ddof=1)

	# absolute deviation
	ad = np.mean(np.abs(signal - median))

	# kurtosis
	kurt = stats.kurtosis(signal, bias=False)

	# skweness
	skew = stats.skew(signal, bias=False)

	# output
	args = (mean, median, minVal, maxVal, maxAmp, sigma2, sigma, ad, kurt, skew)
	names = ('mean', 'median', 'min', 'max', 'max_amp', 'var', 'std_dev',
			 'abs_dev', 'kurtosis', 'skewness')

	return utils.ReturnTuple(args, names)


def normalize(signal=None, ddof=1):
	"""Normalize a signal to zero mean and unitary standard deviation.

    Parameters
    ----------
    signal : array
        Input signal.
    ddof : int, optional
        Delta degrees of freedom for standard deviation computation;
        the divisor is `N - ddof`, where `N` is the number of elements;
        default is one.

    Returns
    -------
    signal : array
        Normalized signal.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	# ensure numpy
	signal = np.array(signal)

	normalized = signal - signal.mean()
	normalized /= normalized.std(ddof=ddof)

	return utils.ReturnTuple((normalized,), ('signal',))


def zero_cross(signal=None, detrend=False):
	"""Locate the indices where the signal crosses zero.

    Parameters
    ----------
    signal : array
        Input signal.
    detrend : bool, optional
        If True, remove signal mean before computation.

    Returns
    -------
    zeros : array
        Indices of zero crossings.

    Notes
    -----
    * When the signal crosses zero between samples, the first index
      is returned.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	if detrend:
		signal = signal - np.mean(signal)

	# zeros
	df = np.diff(np.sign(signal))
	zeros = np.nonzero(np.abs(df) > 0)[0]

	return utils.ReturnTuple((zeros,), ('zeros',))


def find_extrema(signal=None, mode='both'):
	"""Locate local extrema points in a signal.

    Based on Fermat's Theorem [Ferm]_.

    Parameters
    ----------
    signal : array
        Input signal.
    mode : str, optional
        Whether to find maxima ('max'), minima ('min'), or both ('both').

    Returns
    -------
    extrema : array
        Indices of the extrama points.
    values : array
        Signal values at the extrema points.

    References
    ----------
    .. [Ferm] Wikipedia, "Fermat's theorem (stationary points)",
       https://en.wikipedia.org/wiki/Fermat%27s_theorem_(stationary_points)

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	if mode not in ['max', 'min', 'both']:
		raise ValueError("Unknwon mode %r." % mode)

	aux = np.diff(np.sign(np.diff(signal)))

	if mode == 'both':
		aux = np.abs(aux)
		extrema = np.nonzero(aux > 0)[0] + 1
	elif mode == 'max':
		extrema = np.nonzero(aux < 0)[0] + 1
	elif mode == 'min':
		extrema = np.nonzero(aux > 0)[0] + 1

	values = signal[extrema]

	return utils.ReturnTuple((extrema, values), ('extrema', 'values'))


def windower(signal=None,
			 size=None,
			 step=None,
			 fcn=None,
			 fcn_kwargs=None,
			 kernel='boxcar',
			 kernel_kwargs=None):
	"""Apply a function to a signal in sequential windows, with optional overlap.

    Availabel window kernels: boxcar, triang, blackman, hamming, hann,
    bartlett, flattop, parzen, bohman, blackmanharris, nuttall, barthann,
    kaiser (needs beta), gaussian (needs std), general_gaussian (needs power,
    width), slepian (needs width), chebwin (needs attenuation).

    Parameters
    ----------
    signal : array
        Input signal.
    size : int
        Size of the signal window.
    step : int, optional
        Size of window shift; if None, there is no overlap.
    fcn : callable
        Function to apply to each window.
    fcn_kwargs : dict, optional
        Additional keyword arguments to pass to 'fcn'.
    kernel : str, array, optional
        Type of kernel to use; if array, use directly as the kernel.
    kernel_kwargs : dict, optional
        Additional keyword arguments to pass on window creation; ignored if
        'kernel' is an array.

    Returns
    -------
    index : array
        Indices characterizing window locations (start of the window).
    values : array
        Concatenated output of calling 'fcn' on each window.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify an input signal.")

	if fcn is None:
		raise TypeError("Please specify a function to apply to each window.")

	if fcn_kwargs is None:
		fcn_kwargs = {}

	if kernel_kwargs is None:
		kernel_kwargs = {}

	length = len(signal)

	if isinstance(kernel, six.string_types):
		# check size
		if size > length:
			raise ValueError("Window size must be smaller than signal length.")

		win = _get_window(kernel, size, **kernel_kwargs)
	elif isinstance(kernel, np.ndarray):
		win = kernel
		size = len(win)

		# check size
		if size > length:
			raise ValueError("Window size must be smaller than signal length.")

	if step is None:
		step = size

	if step <= 0:
		raise ValueError("Step size must be at least 1.")

	# number of windows
	nb = 1 + (length - size) // step

	# check signal dimensionality
	if np.ndim(signal) == 2:
		# time along 1st dim, tile window
		nch = np.shape(signal)[1]
		win = np.tile(np.reshape(win, (size, 1)), nch)

	index = []
	values = []
	for i in range(nb):
		start = i * step
		stop = start + size
		index.append(start)

		aux = signal[start:stop] * win

		# apply function
		out = fcn(aux, **fcn_kwargs)
		values.append(out)

	# transform to numpy
	index = np.array(index, dtype='int')
	values = np.array(values)

	return utils.ReturnTuple((index, values), ('index', 'values'))


def synchronize(x=None, y=None, detrend=True):
	"""Align two signals based on cross-correlation.

    Parameters
    ----------
    x : array
        First input signal.
    y : array
        Second input signal.
    detrend : bool, optional
        If True, remove signal means before computation.

    Returns
    -------
    delay : int
        Delay (number of samples) of 'x' in relation to 'y';
        if 'delay' < 0 , 'x' is ahead in relation to 'y';
        if 'delay' > 0 , 'x' is delayed in relation to 'y'.
    corr : float
        Value of maximum correlation.
    synch_x : array
        Biggest possible portion of 'x' in synchronization.
    synch_y : array
        Biggest possible portion of 'y' in synchronization.

    """

	# check inputs
	if x is None:
		raise TypeError("Please specify the first input signal.")

	if y is None:
		raise TypeError("Please specify the second input signal.")

	n1 = len(x)
	n2 = len(y)

	if detrend:
		x = x - np.mean(x)
		y = y - np.mean(y)

	# correlate
	corr = np.correlate(x, y, mode='full')
	d = np.arange(-n2 + 1, n1, dtype='int')
	ind = np.argmax(corr)

	delay = d[ind]
	maxCorr = corr[ind]

	# get synchronization overlap
	if delay < 0:
		c = min([n1, len(y[-delay:])])
		synch_x = x[:c]
		synch_y = y[-delay:-delay + c]
	elif delay > 0:
		c = min([n2, len(x[delay:])])
		synch_x = x[delay:delay + c]
		synch_y = y[:c]
	else:
		c = min([n1, n2])
		synch_x = x[:c]
		synch_y = y[:c]

	# output
	args = (delay, maxCorr, synch_x, synch_y)
	names = ('delay', 'corr', 'synch_x', 'synch_y')

	return utils.ReturnTuple(args, names)


def pearson_correlation(x=None, y=None):
	"""Compute the Pearson Correlation Coefficient bertween two signals.

    The coefficient is given by:

    .. math::

        r_{xy} = \\frac{E[(X - \\mu_X) (Y - \\mu_Y)]}{\\sigma_X \\sigma_Y}

    Parameters
    ----------
    x : array
        First input signal.
    y : array
        Second input signal.

    Returns
    -------
    rxy : float
        Pearson correlation coefficient, ranging between -1 and +1.

    Raises
    ------
    ValueError
        If the input signals do not have the same length.

    """

	# check inputs
	if x is None:
		raise TypeError("Please specify the first input signal.")

	if y is None:
		raise TypeError("Please specify the second input signal.")

	# ensure numpy
	x = np.array(x)
	y = np.array(y)

	n = len(x)

	if n != len(y):
		raise ValueError('Input signals must have the same length.')

	mx = np.mean(x)
	my = np.mean(y)

	Sxy = np.sum(x * y) - n * mx * my
	Sxx = np.sum(np.power(x, 2)) - n * mx ** 2
	Syy = np.sum(np.power(y, 2)) - n * my ** 2

	rxy = Sxy / (np.sqrt(Sxx) * np.sqrt(Syy))

	# avoid propagation of numerical errors
	if rxy > 1.0:
		rxy = 1.0
	elif rxy < -1.0:
		rxy = -1.0

	return utils.ReturnTuple((rxy,), ('rxy',))


def rms_error(x=None, y=None):
	"""Compute the Root-Mean-Square Error between two signals.

    The error is given by:

    .. math::

        rmse = \\sqrt{E[(X - Y)^2]}

    Parameters
    ----------
    x : array
        First input signal.
    y : array
        Second input signal.

    Returns
    -------
    rmse : float
        Root-mean-square error.

    Raises
    ------
    ValueError
        If the input signals do not have the same length.

    """

	# check inputs
	if x is None:
		raise TypeError("Please specify the first input signal.")

	if y is None:
		raise TypeError("Please specify the second input signal.")

	# ensure numpy
	x = np.array(x)
	y = np.array(y)

	n = len(x)

	if n != len(y):
		raise ValueError('Input signals must have the same length.')

	rmse = np.sqrt(np.mean(np.power(x - y, 2)))

	return utils.ReturnTuple((rmse,), ('rmse',))


def get_heart_rate(beats=None, sampling_rate=1000., smooth=False, size=3):
	"""Compute instantaneous heart rate from an array of beat indices.

    Parameters
    ----------
    beats : array
        Beat location indices.
    sampling_rate : int, float, optional
        Sampling frequency (Hz).
    smooth : bool, optional
        If True, perform smoothing on the resulting heart rate.
    size : int, optional
        Size of smoothing window; ignored if `smooth` is False.

    Returns
    -------
    index : array
        Heart rate location indices.
    heart_rate : array
        Instantaneous heart rate (bpm).

    Notes
    -----
    * Assumes normal human heart rate to be between 40 and 200 bpm.

    """

	# check inputs
	if beats is None:
		raise TypeError("Please specify the input beat indices.")

	if len(beats) < 2:
		raise ValueError("Not enough beats to compute heart rate.")

	# compute heart rate
	ts = beats[1:]
	hr = sampling_rate * (60. / np.diff(beats))

	# physiological limits
	indx = np.nonzero(np.logical_and(hr >= 40, hr <= 200))
	ts = ts[indx]
	hr = hr[indx]

	# smooth with moving average
	if smooth and (len(hr) > 1):
		hr, _ = smoother(signal=hr, kernel='boxcar', size=size, mirror=True)

	return utils.ReturnTuple((ts, hr), ('index', 'heart_rate'))


def _pdiff(x, p1, p2):
	"""Compute the squared difference between two interpolators, given the
    x-coordinates.

    Parameters
    ----------
    x : array
        Array of x-coordinates.
    p1 : object
        First interpolator.
    p2 : object
        Second interpolator.

    Returns
    -------
    diff : array
        Squared differences.

    """

	diff = (p1(x) - p2(x)) ** 2

	return diff


def find_intersection(x1=None,
					  y1=None,
					  x2=None,
					  y2=None,
					  alpha=1.5,
					  xtol=1e-6,
					  ytol=1e-6):
	"""Find the intersection points between two lines using piecewise
    polynomial interpolation.

    Parameters
    ----------
    x1 : array
        Array of x-coordinates of the first line.
    y1 : array
        Array of y-coordinates of the first line.
    x2 : array
        Array of x-coordinates of the second line.
    y2 : array
        Array of y-coordinates of the second line.
    alpha : float, optional
        Resolution factor for the x-axis; fraction of total number of
        x-coordinates.
    xtol : float, optional
        Tolerance for the x-axis.
    ytol : float, optional
        Tolerance for the y-axis.

    Returns
    -------
    roots : array
        Array of x-coordinates of found intersection points.
    values : array
        Array of y-coordinates of found intersection points.

    Notes
    -----
    * If no intersection is found, returns the closest point.

    """

	# check inputs
	if x1 is None:
		raise TypeError("Please specify the x-coordinates of the first line.")
	if y1 is None:
		raise TypeError("Please specify the y-coordinates of the first line.")
	if x2 is None:
		raise TypeError("Please specify the x-coordinates of the second line.")
	if y2 is None:
		raise TypeError("Please specify the y-coordinates of the second line.")

	# ensure numpy
	x1 = np.array(x1)
	y1 = np.array(y1)
	x2 = np.array(x2)
	y2 = np.array(y2)

	if x1.shape != y1.shape:
		raise ValueError(
			"Input coordinates for the first line must have the same shape.")
	if x2.shape != y2.shape:
		raise ValueError(
			"Input coordinates for the second line must have the same shape.")

	# interpolate
	p1 = interpolate.BPoly.from_derivatives(x1, y1[:, np.newaxis])
	p2 = interpolate.BPoly.from_derivatives(x2, y2[:, np.newaxis])

	# combine x intervals
	x = np.r_[x1, x2]
	x_min = x.min()
	x_max = x.max()
	npoints = int(len(np.unique(x)) * alpha)
	x = np.linspace(x_min, x_max, npoints)

	# initial estimates
	pd = p1(x) - p2(x)
	zerocs, = zero_cross(pd)

	pd_abs = np.abs(pd)
	zeros = np.nonzero(pd_abs < ytol)[0]

	ind = np.unique(np.concatenate((zerocs, zeros)))
	xi = x[ind]

	# search for solutions
	roots = set()
	for v in xi:
		root, _, ier, _ = optimize.fsolve(
			_pdiff,
			v,
			args=(p1, p2),
			full_output=True,
			xtol=xtol,
		)
		if ier == 1 and x_min <= root <= x_max:
			roots.add(root[0])

	if len(roots) == 0:
		# no solution was found => give the best from the initial estimates
		aux = np.abs(pd)
		bux = aux.min() * np.ones(npoints, dtype='float')
		roots, _ = find_intersection(x, aux, x, bux,
									 alpha=1.,
									 xtol=xtol,
									 ytol=ytol)

	# compute values
	roots = list(roots)
	roots.sort()
	roots = np.array(roots)
	values = np.mean(np.vstack((p1(roots), p2(roots))), axis=0)

	return utils.ReturnTuple((roots, values), ('roots', 'values'))


def finite_difference(signal=None, weights=None):
	"""Apply the Finite Difference method to compute derivatives.

    Parameters
    ----------
    signal : array
        Signal to differentiate.
    weights : list, array
        Finite difference weight coefficients.

    Returns
    -------
    index : array
        Indices from `signal` for which the derivative was computed.
    derivative : array
        Computed derivative.

    Notes
    -----
    * The method assumes central differences weights.
    * The method accounts for the delay introduced by the algorithm.

    Raises
    ------
    ValueError
        If the number of weights is not odd.

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify a signal to differentiate.")

	if weights is None:
		raise TypeError("Please specify the weight coefficients.")

	N = len(weights)
	if N % 2 == 0:
		raise ValueError("Number of weights must be odd.")

	# diff
	weights = weights[::-1]
	derivative = ss.lfilter(weights, [1], signal)

	# trim delay
	D = N - 1
	D2 = D // 2

	index = np.arange(D2, len(signal) - D2, dtype='int')
	derivative = derivative[D:]

	return utils.ReturnTuple((index, derivative), ('index', 'derivative'))


def _init_dist_profile(m, n, signal):
	"""Compute initial time series signal statistics for distance profile.

    Implements the algorithm described in [Mueen2014]_, using the notation
    from [Yeh2016_a]_.

    Parameters
    ----------
    m : int
        Sub-sequence length.
    n : int
        Target signal length.
    signal : array
        Target signal.

    Returns
    -------
    X : array
        Fourier Transform (FFT) of the signal.
    sigma : array
        Moving standard deviation in windows of length `m`.

    References
    ----------
    .. [Mueen2014] Abdullah Mueen, Hossein Hamooni, "Trilce Estrada: Time
       Series Join on Subsequence Correlation", ICDM 2014: 450-459
    .. [Yeh2016_a] Chin-Chia Michael Yeh, Yan Zhu, Liudmila Ulanova,
       Nurjahan Begum, Yifei Ding, Hoang Anh Dau, Diego Furtado Silva,
       Abdullah Mueen, Eamonn Keogh, "Matrix Profile I: All Pairs Similarity
       Joins for Time Series: A Unifying View that Includes Motifs, Discords
       and Shapelets", IEEE ICDM 2016

    """

	# compute signal stats
	csumx = np.zeros(n + 1, dtype='float')
	csumx[1:] = np.cumsum(signal)
	sumx = csumx[m:] - csumx[:-m]

	csumx2 = np.zeros(n + 1, dtype='float')
	csumx2[1:] = np.cumsum(np.power(signal, 2))
	sumx2 = csumx2[m:] - csumx2[:-m]

	meanx = sumx / m
	sigmax2 = (sumx2 / m) - np.power(meanx, 2)
	sigma = np.sqrt(sigmax2)

	# append zeros
	x = np.concatenate((signal, np.zeros(n, dtype='float')))

	# compute FFT
	X = np.fft.fft(x)

	return X, sigma


def _ditance_profile(m, n, query, X, sigma):
	"""Compute the distance profile of a query sequence against a signal.

    Implements the algorithm described in [Mueen2014]_, using the notation
    from [Yeh2016]_.

    Parameters
    ----------
    m : int
        Query sub-sequence length.
    n : int
        Target time series length.
    query : array
        Query sub-sequence.
    X : array
        Target time series Fourier Transform (FFT).
    sigma : array
        Moving standard deviation in windows of length `m`.

    Returns
    -------
    dist : array
        Distance profile (squared).

    Notes
    -----
    * Computes distances on z-normalized data.

    References
    ----------
    .. [Mueen2014] Abdullah Mueen, Hossein Hamooni, "Trilce Estrada: Time
       Series Join on Subsequence Correlation", ICDM 2014: 450-459
    .. [Yeh2016] Chin-Chia Michael Yeh, Yan Zhu, Liudmila Ulanova,
       Nurjahan Begum, Yifei Ding, Hoang Anh Dau, Diego Furtado Silva,
       Abdullah Mueen, Eamonn Keogh, "Matrix Profile I: All Pairs Similarity
       Joins for Time Series: A Unifying View that Includes Motifs, Discords
       and Shapelets", IEEE ICDM 2016

    """

	# normalize query
	q = (query - np.mean(query)) / np.std(query)

	# reverse query and append zeros
	y = np.concatenate((q[::-1], np.zeros(2 * n - m, dtype='float')))

	# compute dot products fast
	Y = np.fft.fft(y)
	Z = X * Y
	z = np.fft.ifft(Z)
	z = z[m - 1:n]

	# compute distances (z-normalized squared euclidean distance)
	dist = 2 * m * (1 - z / (m * sigma))

	return dist


def distance_profile(query=None, signal=None, metric='euclidean'):
	"""Compute the distance profile of a query sequence against a signal.

    Implements the algorithm described in [Mueen2014]_.

    Parameters
    ----------
    query : array
        Input query signal sequence.
    signal : array
        Input target time series signal.
    metric : str, optional
        The distance metric to use; one of 'euclidean' or 'pearson'; default
        is 'euclidean'.

    Returns
    -------
    dist : array
        Distance of the query sequence to every sub-sequnce in the signal.

    Notes
    -----
    * Computes distances on z-normalized data.

    References
    ----------
    .. [Mueen2014] Abdullah Mueen, Hossein Hamooni, "Trilce Estrada: Time
       Series Join on Subsequence Correlation", ICDM 2014: 450-459

    """

	# check inputs
	if query is None:
		raise TypeError("Please specify the input query sequence.")

	if signal is None:
		raise TypeError("Please specify the input time series signal.")

	if metric not in ['euclidean', 'pearson']:
		raise ValueError("Unknown distance metric.")

	# ensure numpy
	query = np.array(query)
	signal = np.array(signal)

	m = len(query)
	n = len(signal)
	if m > n / 2:
		raise ValueError("Time series signal is too short relative to"
						 " query length.")

	# get initial signal stats
	X, sigma = _init_dist_profile(m, n, signal)

	# compute distance profile
	dist = _ditance_profile(m, n, query, X, sigma)

	if metric == 'pearson':
		dist = 1 - np.abs(dist) / (2 * m)
	elif metric == 'euclidean':
		dist = np.abs(np.sqrt(dist))

	return utils.ReturnTuple((dist,), ('dist',))


def signal_self_join(signal=None, size=None, index=None, limit=None):
	"""Compute the matrix profile for a self-similarity join of a time series.

    Implements the algorithm described in [Yeh2016_b]_.

    Parameters
    ----------
    signal : array
        Input target time series signal.
    size : int
        Size of the query sub-sequences.
    index : list, array, optional
        Starting indices for query sub-sequences; the default is to search all
        sub-sequences.
    limit : int, optional
        Upper limit for the number of query sub-sequences; the default is to
        search all sub-sequences.

    Returns
    -------
    matrix_index : array
        Matric profile index.
    matrix_profile : array
        Computed matrix profile (distances).

    Notes
    -----
    * Computes euclidean distances on z-normalized data.

    References
    ----------
    .. [Yeh2016_b] Chin-Chia Michael Yeh, Yan Zhu, Liudmila Ulanova,
       Nurjahan Begum, Yifei Ding, Hoang Anh Dau, Diego Furtado Silva,
       Abdullah Mueen, Eamonn Keogh, "Matrix Profile I: All Pairs Similarity
       Joins for Time Series: A Unifying View that Includes Motifs, Discords
       and Shapelets", IEEE ICDM 2016

    """

	# check inputs
	if signal is None:
		raise TypeError("Please specify the input time series signal.")

	if size is None:
		raise TypeError("Please specify the sub-sequence size.")

	# ensure numpy
	signal = np.array(signal)

	n = len(signal)
	if size > n / 2:
		raise ValueError("Time series signal is too short relative to desired"
						 " sub-sequence length.")

	if size < 4:
		raise ValueError("Sub-sequence length must be at least 4.")

	# matrix profile length
	nb = n - size + 1

	# get search index
	if index is None:
		index = np.random.permutation(np.arange(nb, dtype='int'))
	else:
		index = np.array(index)
		if not np.all(index < nb):
			raise ValueError("Provided `index` exceeds allowable sub-sequences.")

	# limit search
	if limit is not None:
		if limit < 1:
			raise ValueError("Search limit must be at least 1.")

		index = index[:limit]

	# exclusion zone (to avoid query self-matches)
	ezone = int(round(size / 4))

	# initialization
	matrix_profile = np.inf * np.ones(nb, dtype='float')
	matrix_index = np.zeros(nb, dtype='int')

	X, sigma = _init_dist_profile(size, n, signal)

	# compute matrix profile
	for idx in index:
		# compute distance profile
		query = signal[idx:idx + size]
		dist = _ditance_profile(size, n, query, X, sigma)
		dist = np.abs(np.sqrt(dist))  # to have euclidean distance

		# apply exlusion zone
		a = max([0, idx - ezone])
		b = min([nb, idx + ezone + 1])
		dist[a:b] = np.inf

		# find nearest neighbors
		pos = dist < matrix_profile
		matrix_profile[pos] = dist[pos]
		matrix_index[pos] = idx

		# account for exlusion zone
		neighbor = np.argmin(dist)
		matrix_profile[idx] = dist[neighbor]
		matrix_index[idx] = neighbor

	# output
	args = (matrix_index, matrix_profile)
	names = ('matrix_index', 'matrix_profile')

	return utils.ReturnTuple(args, names)


def signal_cross_join(signal1=None,
					  signal2=None,
					  size=None,
					  index=None,
					  limit=None):
	"""Compute the matrix profile for a similarity join of two time series.

    Computes the nearest sub-sequence in `signal2` for each sub-sequence in
    `signal1`. Implements the algorithm described in [Yeh2016_c]_.

    Parameters
    ----------
    signal1 : array
        Fisrt input time series signal.
    signal2 : array
        Second input time series signal.
    size : int
        Size of the query sub-sequences.
    index : list, array, optional
        Starting indices for query sub-sequences; the default is to search all
        sub-sequences.
    limit : int, optional
        Upper limit for the number of query sub-sequences; the default is to
        search all sub-sequences.

    Returns
    -------
    matrix_index : array
        Matric profile index.
    matrix_profile : array
        Computed matrix profile (distances).

    Notes
    -----
    * Computes euclidean distances on z-normalized data.

    References
    ----------
    .. [Yeh2016_c] Chin-Chia Michael Yeh, Yan Zhu, Liudmila Ulanova,
       Nurjahan Begum, Yifei Ding, Hoang Anh Dau, Diego Furtado Silva,
       Abdullah Mueen, Eamonn Keogh, "Matrix Profile I: All Pairs Similarity
       Joins for Time Series: A Unifying View that Includes Motifs, Discords
       and Shapelets", IEEE ICDM 2016

    """

	# check inputs
	if signal1 is None:
		raise TypeError("Please specify the first input time series signal.")

	if signal2 is None:
		raise TypeError("Please specify the second input time series signal.")

	if size is None:
		raise TypeError("Please specify the sub-sequence size.")

	# ensure numpy
	signal1 = np.array(signal1)
	signal2 = np.array(signal2)

	n1 = len(signal1)
	if size > n1 / 2:
		raise ValueError("First time series signal is too short relative to"
						 " desired sub-sequence length.")

	n2 = len(signal2)
	if size > n2 / 2:
		raise ValueError("Second time series signal is too short relative to"
						 " desired sub-sequence length.")

	if size < 4:
		raise ValueError("Sub-sequence length must be at least 4.")

	# matrix profile length
	nb1 = n1 - size + 1
	nb2 = n2 - size + 1

	# get search index
	if index is None:
		index = np.random.permutation(np.arange(nb2, dtype='int'))
	else:
		index = np.array(index)
		if not np.all(index < nb2):
			raise ValueError("Provided `index` exceeds allowable `signal2`"
							 " sub-sequences.")

	# limit search
	if limit is not None:
		if limit < 1:
			raise ValueError("Search limit must be at least 1.")

		index = index[:limit]

	# initialization
	matrix_profile = np.inf * np.ones(nb1, dtype='float')
	matrix_index = np.zeros(nb1, dtype='int')

	X, sigma = _init_dist_profile(size, n1, signal1)

	# compute matrix profile
	for idx in index:
		# compute distance profile
		query = signal2[idx:idx + size]
		dist = _ditance_profile(size, n1, query, X, sigma)
		dist = np.abs(np.sqrt(dist))  # to have euclidean distance

		# find nearest neighbor
		pos = dist <= matrix_profile
		matrix_profile[pos] = dist[pos]
		matrix_index[pos] = idx

	# output
	args = (matrix_index, matrix_profile)
	names = ('matrix_index', 'matrix_profile')

	return utils.ReturnTuple(args, names)


def mean_waves(data=None, size=None, step=None):
	"""Extract mean samples from a data set.

    Parameters
    ----------
    data : array
        An m by n array of m data samples in an n-dimensional space.
    size : int
        Number of samples to use for each mean sample.
    step : int, optional
        Number of samples to jump, controlling overlap; default is equal to
        `size` (no overlap).

    Returns
    -------
    waves : array
        An k by n array of mean samples.

    Notes
    -----
    * Discards trailing samples if they are not enough to satify the `size`
      parameter.

    Raises
    ------
    ValueError
        If `step` is an invalid value.
    ValueError
        If there are not enough samples for the given `size`.

    """

	# check inputs
	if data is None:
		raise TypeError("Please specify an input data set.")

	if size is None:
		raise TypeError("Please specify the number of samples for the mean.")

	if step is None:
		step = size

	if step < 0:
		raise ValueError("The step must be a positive integer.")

	# number of waves
	L = len(data) - size
	nb = 1 + L // step
	if nb <= 0:
		raise ValueError("Not enough samples for the given `size`.")

	# compute
	waves = [np.mean(data[i:i + size], axis=0) for i in range(0, L + 1, step)]
	waves = np.array(waves)

	return utils.ReturnTuple((waves,), ('waves',))


def median_waves(data=None, size=None, step=None):
	"""Extract median samples from a data set.

    Parameters
    ----------
    data : array
        An m by n array of m data samples in an n-dimensional space.
    size : int
        Number of samples to use for each median sample.
    step : int, optional
        Number of samples to jump, controlling overlap; default is equal to
        `size` (no overlap).

    Returns
    -------
    waves : array
        An k by n array of median samples.

    Notes
    -----
    * Discards trailing samples if they are not enough to satify the `size`
      parameter.

    Raises
    ------
    ValueError
        If `step` is an invalid value.
    ValueError
        If there are not enough samples for the given `size`.

    """

	# check inputs
	if data is None:
		raise TypeError("Please specify an input data set.")

	if size is None:
		raise TypeError("Please specify the number of samples for the median.")

	if step is None:
		step = size

	if step < 0:
		raise ValueError("The step must be a positive integer.")

	# number of waves
	L = len(data) - size
	nb = 1 + L // step
	if nb <= 0:
		raise ValueError("Not enough samples for the given `size`.")

	# compute
	waves = [np.median(data[i:i + size], axis=0) for i in range(0, L + 1, step)]
	waves = np.array(waves)

	return utils.ReturnTuple((waves,), ('waves',))