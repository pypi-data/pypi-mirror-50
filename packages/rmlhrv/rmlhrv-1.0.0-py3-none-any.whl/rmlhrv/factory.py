# -*- coding: utf-8 -*-
"""

:copyright: (c) 2019 by Ryerson Multimedia Lab
:license: BSD 3-clause, see LICENSE for more details.

"""

from __future__ import division, print_function

import warnings
import numpy as np
import matplotlib as mpl
import scipy as sp
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import welch, lombscargle
from rmlhrv import tools, utils

class TimeDomain(object):

    @staticmethod
    def nni_parameters(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        args = (int(nn.size), nn.mean(), nn.min(), nn.max())
        names = ('nni_counter', 'nni_mean', 'nni_min', 'nni_max')
        return utils.ReturnTuple(args, names)

    @staticmethod
    def nni_differences_parameters(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        nnd = tools.nni_diff(nn)
        args = (float(nnd.mean()), int(nnd.min()), int(nnd.max()),)
        names = ('nni_diff_mean', 'nni_diff_min', 'nni_diff_max',)
        return utils.ReturnTuple(args, names)

    @staticmethod
    def hr_parameters(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        hr = tools.heart_rate(nn)
        args = (hr.mean(), hr.min(), hr.max(), hr.std(ddof=1))
        names = ('hr_mean', 'hr_min', 'hr_max', 'hr_std')
        return utils.ReturnTuple(args, names)

    @staticmethod
    def sdnn(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        args = [tools.std(nn)]
        names = ['sdnn']
        return utils.ReturnTuple(args, names)

    @staticmethod
    def sdnn_index(nni=None, rpeaks=None, full=True, overlap=False, duration=300):
        nn = tools.check_input(nni, rpeaks)
        segments, seg = tools.segmentation(nn, full=full, overlap=overlap, duration=duration)
        if seg:
            sdnn_values = [TimeDomain.sdnn(x)['sdnn'] for x in segments]
            sdnn_index = np.mean(sdnn_values)
        else:
            sdnn_index = float('nan')
            if tools.WARN:
                warnings.warn("Signal duration too short for SDNN index computation.")
        args = [sdnn_index]
        names = ['sdnn_index']
        return utils.ReturnTuple(args, names)

    @staticmethod
    def sdann(nni=None, rpeaks=None, full=True, overlap=False, duration=300):
        nn = tools.check_input(nni, rpeaks)
        segments, seg = tools.segmentation(nn, full=full, overlap=overlap, duration=duration)

        if seg:
            mean_values = [np.mean(x) for x in segments]
            sdann_ = tools.std(mean_values)
        else:
            sdann_ = float('nan')
            if tools.WARN:
                warnings.warn("Signal duration too short for SDANN computation.")
        args = [sdann_]
        names = ['sdann']
        return utils.ReturnTuple(args, names)

    @staticmethod
    def rmssd(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        nnd = tools.nni_diff(nn)
        rmssd_ = np.sum(x ** 2 for x in nnd)
        rmssd_ = np.sqrt(1. / nnd.size * rmssd_)
        args = (rmssd_,)
        names = ('rmssd',)
        return utils.ReturnTuple(args, names)

    @staticmethod
    def sdsd(nni=None, rpeaks=None):
        nn = tools.check_input(nni, rpeaks)
        nnd = tools.nni_diff(nn)
        sdsd_ = tools.std(nnd)
        args = [sdsd_]
        names = ['sdsd']
        return utils.ReturnTuple(args, names)

    @staticmethod
    def nnXX(nni=None, rpeaks=None, threshold=None):
        nn = tools.check_input(nni, rpeaks)
        if threshold is None:
            raise TypeError("No threshold specified. Please specify a [ms] threshold.")
        if threshold <= 0:
            raise ValueError("Invalid value for 'threshold'. Value must not be <= 0.")
        nnd = tools.nni_diff(nn)
        nnxx = sum(i > threshold for i in nnd)
        pnnxx = nnxx / len(nnd) * 100
        args = (nnxx, pnnxx)
        names = ('nn%i' % threshold, 'pnn%i' % threshold)
        return utils.ReturnTuple(args, names)

    @staticmethod
    def nn50(nni=None, rpeaks=None):
        return TimeDomain.nnXX(nni=nni, rpeaks=rpeaks, threshold=50)

    @staticmethod
    def nn20(nni=None, rpeaks=None):
        return TimeDomain.nnXX(nni=nni, rpeaks=rpeaks, threshold=20)

    @staticmethod
    def tinn(nni=None, rpeaks=None, binsize=7.8125, plot=True, show=True, figsize=None, legend=True):
        nn = tools.check_input(nni, rpeaks)
        # Get Histogram data (with or without histogram plot figure)
        if plot:
            fig, ax, D, bins = TimeDomain._get_histogram(nn, figsize=figsize, binsize=binsize, legend=legend, plot=plot)
        else:
            D, bins = TimeDomain._get_histogram(nn, figsize=figsize, binsize=binsize, legend=legend, plot=plot)

        # Use only all bins except the last one to avoid indexing error with 'D' (otherwise bins.size = D.size + 1)
        # bins = np.asarray(bins[:-1])

        # Get bins of the triangular's N side (left side of the bin with the highest value of the distribution)
        n_bins = [bin for bin in bins if bin < bins[np.argmax(D)]]

        # Get bins of the triangular's M side (right side of the bin with the highest value of the distribution)
        m_bins = [bin for bin in bins if bin > bins[np.argmax(D)]]

        # Set a maximum error
        min_error = 2 ** 14
        N = 0
        M = 0

        # Compute triangle and error for each possible N value within the bins
        for n in n_bins:
            # Compute triangle and error for each possible M value within the bins
            for m in m_bins:
                # Get bin indices and time array that are valid for q(t) (i.e. q(t)!=0 for N < t < M)
                qi = np.zeros(bins.size)
                for i, bin in enumerate(bins):
                    qi[i] = (True if n <= bin <= m else False)
                t = bins[[i for i, q in enumerate(qi) if q]]

                # Compute linear function that describes the N side of the triangle (q(N) = 0 to q(X) = max(D(X)))
                qn = interp1d([t[0], bins[np.argmax(D)]], [0, np.max(D)], 'linear', bounds_error=False)
                qn = qn(bins)

                # Compute linear function that describes the M side of the triangle (q(X) = max(D(X)) to q(M) = 0)
                qm = interp1d([bins[np.argmax(D)], t[-1]], [np.max(D), 0], 'linear', bounds_error=False)
                qm = qm(bins)

                # Join the linear functions of both sides to single array
                q = np.zeros(len(bins))
                for i, val in enumerate(bins):
                    if str(qn[i]) != 'nan':
                        q[i] = qn[i]
                    elif str(qm[i]) != 'nan':
                        q[i] = qm[i]
                    else:
                        q[i] = 0

                # Compute squared error
                error = np.sum([(D[i] - q[i]) ** 2 for i, _ in enumerate(bins)])

                # Save N and M value if error is < smaller than before
                if error < min_error:
                    N, M, min_error = n, m, error
                    qf = q

        # Compute TINN
        tinn = M - N

        # If plot figure required, add interpolated triangle and other specified plot characteristics
        if plot:
            # Add triangle to the plot
            ax.plot([N, bins[np.argmax(D)]], [0, D.max()], 'r--', linewidth=0.8)
            ax.plot([bins[np.argmax(D)], M], [D.max(), 0], 'r--', linewidth=0.8)

            # Add legend
            if legend:
                h = mpl.patches.Patch(facecolor='skyblue')
                tri = mpl.lines.Line2D([0, 0], [0, 0], linestyle='--', linewidth=0.8, color='r')
                x = mpl.patches.Patch(facecolor='g', alpha=0.0)
                dx = mpl.patches.Patch(facecolor='g', alpha=0.0)
                n = mpl.patches.Patch(facecolor='white', alpha=0.0)
                m = mpl.patches.Patch(facecolor='white', alpha=0.0)
                tinn_ = mpl.patches.Patch(facecolor='white', alpha=0.0)
                ax.legend(
                    [h, tri, x, dx, n, m, tinn_],
                    ['Histogram D(NNI)', 'Triangular Interpol.', 'D(X): %i' % D.max(),
                     'X: %.3f$ms$' % bins[np.argmax(D)],
                     'N: %.3f$ms$' % N, 'M: %.3fms' % M, 'TINN: %.3fms' % tinn],
                    loc=0
                )

            # Show plot
            if show:
                plt.show()

            # Output
            args = (fig, N, M, tinn,)
            names = ('tinn_histogram', 'tinn_n', 'tinn_m', 'tinn',)
        else:
            # Output
            args = (N, M, tinn,)
            names = ('tinn_n', 'tinn_m', 'tinn',)

        return utils.ReturnTuple(args, names)

    @staticmethod
    def triangular_index(nni=None, rpeaks=None, binsize=7.8125, plot=True, show=True, figsize=None, legend=True):
        nn = tools.check_input(nni, rpeaks)
        # If histogram should be plotted
        if plot:
            # Get histogram values
            fig, ax, D, bins = TimeDomain._get_histogram(nn, figsize=figsize, binsize=binsize, legend=legend, plot=plot)

            # Compute Triangular index: number of nn intervals / maximum value of the distribution
            tri_index = nn.size / D.max()

            # Add legend
            if legend:
                h = mpl.patches.Patch(facecolor='skyblue')
                x = mpl.patches.Patch(facecolor='g', alpha=0.0)
                dx = mpl.patches.Patch(facecolor='g', alpha=0.0)
                tri = mpl.patches.Patch(facecolor='white', alpha=0.0)
                ax.legend(
                    [h, x, dx, tri],
                    ['Histogram D(NNI)', 'D(X): %i' % D.max(), 'X: %.3f' % bins[np.argmax(D)],
                     'TriIndex: %.3f' % tri_index],
                    loc=0
                )

            # Show plot
            if show:
                plt.show()

            # Output
            args = (fig, tri_index,)
            names = ('tri_histogram', 'tri_index',)

        # If histogram should not be plotted
        else:
            D, bins = TimeDomain._get_histogram(nn, figsize=figsize, binsize=binsize, legend=legend, plot=plot)

            # Compute Triangular index: number of nn intervals / maximum value of the distribution
            tri_index = nn.size / D.max()

            # Output
            args = (tri_index,)
            names = ('tri_index',)

        return utils.ReturnTuple(args, names)

    @staticmethod
    def _get_histogram(nn=None, plot=True, figsize=None, binsize=None, legend=True):
        if nn is None:
            raise TypeError("No input data provided for 'nn'.")
        else:
            nn = np.asarray(nn)

        if binsize is None:
            raise TypeError("No input data provided for 'binsize'")

        # Create bins array
        bins = np.arange(0, np.max(nn) + binsize, binsize)

        # Get histogram plot and data
        if plot:
            # Check figsize
            if figsize is None:
                figsize = (6, 6)

            # Prepare plot figure
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            vals, bins, patches = ax.hist(nn, bins, density=False, align='left', facecolor='skyblue', edgecolor='black')
            bins = bins[:-1]

            # Highlight bin of the histograms maximum value with a different color and prepare legend
            if legend:
                ax.vlines(bins[np.argmax(vals)], 0, (vals.max() * 1.1),
                          linestyles='--', color='g', linewidth=0.6)
                pos = (bins[np.argmax(vals)], vals.max() * 1.11)
                ax.annotate('D(X)', xy=pos, xytext=pos, ha='center', color='g')

            # Configure figure and plot
            ax.axis([nn.min() - (3 * binsize), nn.max() + (3 * binsize), 0, vals.max() * 1.15])
            ax.set_xlabel('NNI Bins [ms]')
            ax.set_ylabel('D(NNI) [-]')
            ax.set_title('NNI Histogram')
            return fig, ax, vals, bins

        else:
            vals, bins = np.histogram(nn, bins, density=False)
            return vals, bins[:-1]

    @staticmethod
    def geometrical_parameters(nni=None, rpeaks=None, binsize=7.815, plot=True, show=True, figsize=None,
                               legend=True):
        nn = tools.check_input(nni, rpeaks)

        # Get Histogram data & plot (optional)
        if plot:
            fig, ax, D, bins = TimeDomain._get_histogram(nn, figsize=figsize, binsize=binsize, legend=legend, plot=plot)
        else:
            fig = None

        # Get TINN values without plot figure
        tinn_vals = TimeDomain.tinn(nni=nn, rpeaks=rpeaks, binsize=binsize, show=False, legend=False, figsize=figsize,
                              plot=False)

        # Get triangular index without plot figure
        trindex = TimeDomain.triangular_index(nni=nn, rpeaks=rpeaks, binsize=binsize, show=False, legend=False, plot=False)[
            'tri_index']

        # Histogram plot & settings
        if plot:
            # Plot triangular interpolation
            N, M = tinn_vals['tinn_n'], tinn_vals['tinn_m']
            ax.plot([N, bins[np.argmax(D)]], [0, D.max()], 'r--', linewidth=0.8)
            ax.plot([bins[np.argmax(D)], M], [D.max(), 0], 'r--', linewidth=0.8)

            # Add Legend
            if legend:
                l1 = mpl.patches.Patch(facecolor='skyblue', label='Histogram D(NNI)')
                l2 = mpl.lines.Line2D([0, 0], [0, 0], linestyle='--', linewidth=0.8, color='r', label='Tri. Interpol.')
                l3 = mpl.patches.Patch(facecolor='g', alpha=0.0, label='D(X): %i' % D.max())
                l4 = mpl.patches.Patch(facecolor='g', alpha=0.0, label='X: %.3f$ms$' % bins[np.argmax(D)])
                l5 = mpl.patches.Patch(facecolor='white', alpha=0.0, label='N: %.3f$ms$' % tinn_vals['tinn_n'])
                l6 = mpl.patches.Patch(facecolor='white', alpha=0.0, label='M: %.3fms' % tinn_vals['tinn_m'])
                l7 = mpl.patches.Patch(facecolor='white', alpha=0.0, label='TINN: %.3fms' % tinn_vals['tinn'])
                l8 = mpl.patches.Patch(facecolor='white', alpha=0.0, label='Tri. Index: %.3f' % trindex)
                ax.legend(handles=[l1, l2, l3, l4, l5, l6, l7, l8], loc=0, ncol=1)

            # Show plot
            if show:
                plt.show()

        # Output
        args = (fig, tinn_vals['tinn_n'], tinn_vals['tinn_m'], tinn_vals['tinn'], trindex)
        names = ('nni_histogram', 'tinn_n', 'tinn_m', 'tinn', 'tri_index')
        return utils.ReturnTuple(args, names)
    
class FrequencyDomain(object):

    @staticmethod
    def welch_psd(nni=None,
                  rpeaks=None,
                  fbands=None,
                  nfft=2 ** 12,
                  detrend=True,
                  window='hamming',
                  show=True,
                  show_param=True,
                  legend=True,
                  mode='normal'):
        nn = tools.check_input(nni, rpeaks)

        # Verify or set default frequency bands
        fbands = FrequencyDomain._check_freq_bands(fbands)

        # Resampling (with 4Hz) and interpolate
        # Because RRi are unevenly spaced we must interpolate it for accurate PSD estimation.
        fs = 4
        t = np.cumsum(nn)
        t -= t[0]
        f_interpol = sp.interpolate.interp1d(t, nn, 'cubic')
        t_interpol = np.arange(t[0], t[-1], 1000. / fs)
        nn_interpol = f_interpol(t_interpol)

        # Subtract mean value from each sample for surpression of DC-offsets
        if detrend:
            nn_interpol = nn_interpol - np.mean(nn_interpol)

        # Adapt 'nperseg' according to the total duration of the NNI series (5min threshold = 300000ms)
        if t.max() < 300000:
            nperseg = nfft
        else:
            nperseg = 300

        # Compute power spectral density estimation (where the magic happens)
        frequencies, powers = welch(
            x=nn_interpol,
            fs=fs,
            window=window,
            nperseg=nperseg,
            nfft=nfft,
            scaling='density'
        )

        # Metadata
        args = (nfft, window, fs, 'cubic')
        names = ('fft_nfft', 'fft_window', 'fft_resampling_frequency', 'fft_interpolation',)
        meta = utils.ReturnTuple(args, names)

        if mode not in ['normal', 'dev', 'devplot']:
            warnings.warn("Unknown mode '%s'. Will proceed with 'normal' mode." % mode, stacklevel=2)
            mode = 'normal'

        # Normal Mode:
        # Returns frequency parameters, PSD plot figure and no frequency & power series/arrays
        if mode == 'normal':
            # Compute frequency parameters
            params, freq_i = FrequencyDomain._compute_parameters('fft', frequencies, powers, fbands)

            # Plot PSD
            figure = FrequencyDomain._plot_psd('fft', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure,), ('fft_plot',))

            # Output
            return tools.join_tuples(params, figure, meta)

        # Dev Mode:
        # Returns frequency parameters and frequency & power series/array; does not create a plot figure nor plot the data
        elif mode == 'dev':
            # Compute frequency parameters
            params, _ = FrequencyDomain._compute_parameters('fft', frequencies, powers, fbands)

            # Output
            return tools.join_tuples(params, meta), frequencies, (powers / 10 ** 6)

        # Devplot Mode:
        # Returns frequency parameters, PSD plot figure, and frequency & power series/arrays
        elif mode == 'devplot':
            # Compute frequency parameters
            params, freq_i = FrequencyDomain._compute_parameters('fft', frequencies, powers, fbands)

            # Plot PSD
            figure = FrequencyDomain._plot_psd('fft', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure,), ('fft_plot',))

            # Output
            return tools.join_tuples(params, figure, meta), frequencies, (powers / 10 ** 6)

    @staticmethod
    def lomb_psd(
            nni=None,
            rpeaks=None,
            fbands=None,
            nfft=2 ** 8,
            ma_size=None,
            show=True,
            show_param=True,
            legend=True,
            mode='normal'
    ):
        nn = tools.check_input(nni, rpeaks)

        # Verify or set default frequency bands
        fbands = FrequencyDomain._check_freq_bands(fbands)
        t = np.cumsum(nn)
        t -= t[0]

        # Compute PSD according to the Lomb-Scargle method
        # Specify frequency grid
        frequencies = np.linspace(0, 0.41, nfft)
        # Compute angular frequencies
        a_frequencies = np.asarray(2 * np.pi / frequencies)
        powers = np.asarray(lombscargle(t, nn, a_frequencies, normalize=True))

        # Fix power = inf at f=0
        powers[0] = 2

        # Apply moving average filter
        if ma_size is not None:
            powers = tools.smoother(powers, size=ma_size)['signal']

        # Define metadata
        meta = utils.ReturnTuple((nfft, ma_size,), ('lomb_nfft', 'lomb_ma'))

        if mode not in ['normal', 'dev', 'devplot']:
            warnings.warn("Unknown mode '%s'. Will proceed with 'normal' mode." % mode, stacklevel=2)
            mode = 'normal'

        # Normal Mode:
        # Returns frequency parameters, PSD plot figure and no frequency & power series/arrays
        if mode == 'normal':
            # ms^2 to s^2
            powers = powers * 10 ** 6

            # Compute frequency parameters
            params, freq_i = FrequencyDomain._compute_parameters('lomb', frequencies, powers, fbands)

            # Plot parameters
            figure = FrequencyDomain._plot_psd('lomb', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure,), ('lomb_plot',))

            # Complete output
            return tools.join_tuples(params, figure, meta)

        # Dev Mode:
        # Returns frequency parameters and frequency & power series/array; does not create a plot figure nor plot the data
        elif mode == 'dev':
            # Compute frequency parameters
            params, _ = FrequencyDomain._compute_parameters('lomb', frequencies, powers, fbands)

            # Complete output
            return tools.join_tuples(params, meta), frequencies, powers

        # Devplot Mode:
        # Returns frequency parameters, PSD plot figure, and frequency & power series/arrays
        elif mode == 'devplot':
            # ms^2 to s^2
            powers = powers * 10 ** 6

            # Compute frequency parameters
            params, freq_i = FrequencyDomain._compute_parameters('lomb', frequencies, powers, fbands)

            # Plot parameters
            figure = FrequencyDomain._plot_psd('lomb', frequencies, powers, freq_i, params, show, show_param, legend)
            figure = utils.ReturnTuple((figure,), ('lomb_plot',))

            # Complete output
            return tools.join_tuples(params, figure, meta), frequencies, powers

    @staticmethod
    def _compute_parameters(method, frequencies, power, freq_bands):
        # Compute frequency resolution
        df = (frequencies[1] - frequencies[0])

        # Get indices of freq values within the specified freq bands
        ulf_i, vlf_i, lf_i, hf_i = FrequencyDomain._get_frequency_indices(frequencies, freq_bands)
        ulf_f, vlf_f, lf_f, hf_f = FrequencyDomain._get_frequency_arrays(frequencies, ulf_i, vlf_i, lf_i, hf_i)

        # Absolute powers
        if freq_bands['ulf'] is not None:
            ulf_power = np.sum(power[ulf_i]) * df
        vlf_power = np.sum(power[vlf_i]) * df
        lf_power = np.sum(power[lf_i]) * df
        hf_power = np.sum(power[hf_i]) * df
        abs_powers = (vlf_power, lf_power, hf_power,) if freq_bands['ulf'] is None else (ulf_power, vlf_power, lf_power,
                                                                                         hf_power,)
        total_power = np.sum(abs_powers)

        # Peak frequencies
        if freq_bands['ulf'] is not None:
            ulf_peak = ulf_f[np.argmax(power[ulf_i])]

        # Compute Peak values and catch exception caused if the number of PSD samples is too low
        try:
            vlf_peak = vlf_f[np.argmax(power[vlf_i])]
            lf_peak = lf_f[np.argmax(power[lf_i])]
            hf_peak = hf_f[np.argmax(power[hf_i])]
            peaks = (vlf_peak, lf_peak, hf_peak,) if freq_bands['ulf'] is None else (
            ulf_peak, vlf_peak, lf_peak, hf_peak,)
        except ValueError as e:
            if 'argmax of an empty sequence' in str(e):
                raise ValueError(
                    "'nfft' is too low: not enough PSD samples to compute the frequency parameters. Try to "
                    "increase 'nfft' to avoid this error.")

        # Relative, logarithmic powers & LF/HF ratio
        rels = tuple([float(x) / total_power * 100 for x in abs_powers])
        logs = tuple([float(np.log(x)) for x in abs_powers])
        ratio = float(lf_power) / hf_power

        # Normalized powers
        norms = tuple([100 * x / (lf_power + hf_power) for x in [lf_power, hf_power]])

        # Prepare parameters for plot
        args = (freq_bands, peaks, abs_powers, rels, logs, norms, ratio, total_power)
        names = (
            '%s_bands' % method, '%s_peak' % method, '%s_abs' % method,
            '%s_rel' % method, '%s_log' % method, '%s_norm' % method,
            '%s_ratio' % method, '%s_total' % method)

        # Output
        params = utils.ReturnTuple(args, names)
        freq_i = utils.ReturnTuple((ulf_i, vlf_i, lf_i, hf_i), ('ulf', 'vlf', 'lf', 'hf'))
        return params, freq_i

    @staticmethod
    def _check_freq_bands(freq_bands):
        if freq_bands is None:
            # Set default values
            ulf = None
            vlf = (0.000, 0.04)
            lf = (0.04, 0.15)
            hf = (0.15, 0.4)
            args = (ulf, vlf, lf, hf)
            names = ('ulf', 'vlf', 'lf', 'hf')
        else:
            # Check available data
            args_ = []
            names_ = []

            # ULF band
            ulf = freq_bands['ulf'] if 'ulf' in freq_bands.keys() else (0, 0)
            args_.append(ulf)
            names_.append('ulf')

            # VLF band
            vlf = freq_bands['vlf'] if 'vlf' in freq_bands.keys() else (0.003, 0.04)
            args_.append(vlf)
            names_.append('vlf')

            # LF band
            lf = freq_bands['lf'] if 'lf' in freq_bands.keys() else (0.04, 0.15)
            args_.append(lf)
            names_.append('lf')

            # HF band
            hf = freq_bands['hf'] if 'hf' in freq_bands.keys() else (0.15, 0.4)
            args_.append(hf)
            names_.append('hf')

            # Check if freq_band limits are valid
            # Rule: top frequency of a lower frequency band must not be higher than the lower frequency of a higher
            # frequency band
            invalid = False
            args_ = [list(x) for x in args_ if x is not None]
            for i, val in enumerate(args_[:-1]):
                if val != (0, 0):
                    if args_[i][1] > args_[i + 1][0]:
                        subs = args_[i][1]
                        args_[i][1] = args_[i + 1][0]
                        args_[i + 1][0] = subs
                        invalid = True
                else:
                    args_[i] = None

            if invalid:
                raise ValueError("Invalid or overlapping frequency band limits.")

            args = args_
            names = names_

        return utils.ReturnTuple(args, names)

    @staticmethod
    def _get_frequency_indices(freq, freq_bands):
        indices = []
        for key in freq_bands.keys():
            if freq_bands[key] is None:
                indices.append(None)
            else:
                indices.append(np.where((freq_bands[key][0] <= freq) & (freq <= freq_bands[key][1])))

        if indices[0] is None or len(indices) == 3:
            return None, indices[1][0], indices[2][0], indices[3][0]
        else:
            return indices[0][0], indices[1][0], indices[2][0], indices[3][0]

    @staticmethod
    def _get_frequency_arrays(freq, ulf_i, vlf_i, lf_i, hf_i):
        ulf_f = np.asarray(freq[ulf_i]) if ulf_i is not None else None
        vlf_f = np.asarray(freq[vlf_i])
        lf_f = np.asarray(freq[lf_i])
        hf_f = np.asarray(freq[hf_i])
        return ulf_f, vlf_f, lf_f, hf_f

    @staticmethod
    def _plot_psd(method, freq, power, freq_indices, parameters, show, show_param, legend):
        power = power / 10 ** 6
        fbands = parameters['%s_bands' % method]
        colors = {'ulf': 'b', 'vlf': 'yellowgreen', 'lf': 'salmon', 'hf': 'lightskyblue'}
        df = freq[1] - freq[0]

        if show_param:
            # Add second subplot with all computed parameters
            fig_psd = plt.figure(figsize=(12, 5))

            ax = fig_psd.add_subplot(121)
            ax2 = fig_psd.add_subplot(122)

            # Prepare parameter listing
            data = []
            index = 0

            for band in ['ulf', 'vlf', 'lf', 'hf']:
                if fbands[band] is not None:
                    # Add frequency band specific data
                    data.append(mpl.patches.Patch(facecolor=colors[band], label='%s: %.3fHz - %.3fHz' %
                                                                                (band.upper(), fbands[band][0],
                                                                                 fbands[band][1])))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Peak: %0.3f [$Hz$]' %
                                                                   parameters['%s_peak' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Abs:  %0.3f [$ms^2$]' %
                                                                   parameters['%s_abs' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Rel:  %0.3f [%%]' %
                                                                   parameters['%s_rel' % method][index]))
                    data.append(
                        mpl.patches.Patch(facecolor='white', label='Log:  %0.3f [$-$]' %
                                                                   parameters['%s_log' % method][index]))

                    if band == 'lf':
                        data.append(mpl.patches.Patch(facecolor='white', label='Norm: %0.3f [$-$]' %
                                                                               parameters['%s_norm' % method][0]))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                    elif band == 'hf':
                        data.append(mpl.patches.Patch(facecolor='white', label='Norm: %0.3f [$-$]' %
                                                                               parameters['%s_norm' % method][1]))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))

                    # Spacings, total power and LF/HF ratio to format
                    if band == 'ulf':
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))

                    if band == 'hf':
                        spacing = 2 if fbands['ulf'] is not None else 8
                        for i in range(spacing):
                            data.append(mpl.patches.Patch(facecolor='white', label=''))

                    if band == 'vlf':
                        data.append(mpl.patches.Patch(facecolor='white', label=''))
                        data.append(mpl.patches.Patch(facecolor='white', label=''))

                    if (fbands['ulf'] is not None and band == 'vlf') or (fbands['ulf'] is None and band == 'lf'):
                        data.append(mpl.patches.Patch(fc='white', label='Total Power: %.3f [$ms^2$]' % parameters[
                            '%s_total' % method]))
                        data.append(mpl.patches.Patch(fc='white', label='LF/HF: %.3f [-]' %
                                                                        parameters['%s_ratio' % method]))
                    index += 1
            ax2.legend(handles=data, ncol=2, frameon=False)
            ax2.axis('off')
        else:
            fig_psd = plt.figure()
            ax = fig_psd.add_subplot(111)

        # Highlight the individual frequency bands
        for band in fbands.keys():
            if fbands[band] is not None:
                ax.fill_between(freq[freq_indices[band]], power[freq_indices[band]],
                                facecolor=colors[band],
                                label='%s: %.3fHz - %.3fHz' % (band.upper(), fbands[band][0], fbands[band][1]))

                # Add lines
                if band != 'hf':
                    ax.vlines(fbands[band][1], 0, max(power) * (1 + 0.05),
                              linestyle='--', alpha=0.5, linewidth=0.5)

        # Plot PSD function as line (not for Lomb as it tends to decrease the clarity of the plot)
        if method in ['fft', 'ar']:
            ax.plot(freq, power, color='grey', linewidth=0.5)

        # Add legend
        if legend and not show_param:
            ax.legend()

        # Finalize plot customization
        if method == 'fft':
            ax.set_title("PSD - Welch's Method")
        elif method == 'ar':
            ax.set_title("PSD - Autoregressive (Order %i)" % parameters['ar_order'])
        elif method == 'lomb':
            ax.set_title("PSD - Lomb-Scargle Periodogram")

        ax.grid(alpha=0.3)
        ax.set_xlabel('Frequency [$Hz$]')
        ax.set_ylabel('PSD [$s^2/Hz$]')
        ax.axis([0, fbands['hf'][1], 0, max(power) * (1 + 0.05)])

        if show:
            plt.show()

        return fig_psd
