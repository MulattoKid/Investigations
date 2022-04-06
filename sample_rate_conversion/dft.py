import math
import matplotlib.pyplot as plt
import numpy as np

plot_sine = True
plot_sine_dft = True
plot_sine_upsampled = True
plot_sine_upsampled_dft = True
plot_sinc = False
plot_sinc_dft = False
plot_rectangular_window = False
plot_rectangular_window_sinc = False
plot_rectangular_window_sinc_dft = False
plot_hamming_window = False
plot_hamminh_window_sinc = False
plot_hamming_window_sinc_dft = False
plot_filter_sinc = False
plot_filter_hamming = False
plot_filter = False
plot_filter_normalized = False
plot_filter_sine_upsampled = True
plot_filter_sine_upsampled_dft = True
plot_filter_sine_upsampled_downsampled = True
plot_filter_sine_upsampled_downsampled_dft = True

plot_count = 0
if True: # Just for easier collapse :)
    if plot_sine:
        plot_count += 1
    if plot_sine_dft:
        plot_count += 1
    if plot_sine_upsampled:
        plot_count += 1
    if plot_sine_upsampled_dft:
        plot_count += 1
    if plot_sinc:
        plot_count += 1
    if plot_sinc_dft:
        plot_count += 1
    if plot_rectangular_window:
        plot_count += 1
    if plot_rectangular_window_sinc:
        plot_count += 1
    if plot_rectangular_window_sinc_dft:
        plot_count += 1
    if plot_hamming_window:
        plot_count += 1
    if plot_hamminh_window_sinc:
        plot_count += 1
    if plot_hamming_window_sinc_dft:
        plot_count += 1
    if plot_filter_sinc:
        plot_count += 1
    if plot_filter_hamming:
        plot_count += 1
    if plot_filter:
        plot_count += 1
    if plot_filter_normalized:
        plot_count += 1
    if plot_filter_sine_upsampled:
        plot_count += 1
    if plot_filter_sine_upsampled_dft:
        plot_count += 1
    if plot_filter_sine_upsampled_downsampled:
        plot_count += 1
    if plot_filter_sine_upsampled_downsampled_dft:
        plot_count += 1
if plot_count < 1:
    print("Nothing to plot...")
    exit(0)

fig, axs_tmp = plt.subplots(plot_count, 1)
# If there's only 1 subplot, an array isn't returned (sigh...), so let's make it an array
if plot_count == 1:
    axs = [ axs_tmp ]
else:
    axs = axs_tmp
plt.subplots_adjust(0.05, 0.05, 0.95, 0.95, 0.0, 1.0)
plot_index = 0

def DFT(in_dft_size, in_samples, in_sample_rate):
    out_bins = []

    dft_iter_count = len(in_samples) / in_dft_size
    dft_real = [0.0 for i in range(0, in_dft_size)]
    dft_img = [0.0 for i in range(0, in_dft_size)]
    for i in range(0, dft_iter_count):
        sample_index = i * in_dft_size
        for k in range(0, in_dft_size):
            real = 0.0
            img = 0.0
            for n in range(0, in_dft_size):
                sample = in_samples[sample_index + n]
                real += sample * math.cos((2.0 * math.pi * float(k) * float(n)) / float(in_dft_size))
                img  -= sample * math.sin((2.0 * math.pi * float(k) * float(n)) / float(in_dft_size))
            dft_real[k] += abs(real)
            dft_img[k] += abs(img)
    # Compute magnitude of real bins
    nyquist_limit_index = in_dft_size / 2
    bin_frequency_spacing = in_sample_rate / in_dft_size
    out_bins = []
    max_bin = 0
    max_bin_magnitude = 0.0
    for i in range(0, nyquist_limit_index):
        real = dft_real[i]
        img = dft_img[i]
        magnitude = 2.0 * math.sqrt((real * real) + (img * img)) / float(in_dft_size)
        out_bins.append(magnitude)
        if magnitude > max_bin_magnitude:
            max_bin_magnitude = magnitude
            max_bin = i
    print("Max bin:", max_bin)

    return out_bins

'''
https://en.wikipedia.org/wiki/Nyquist_frequency
The sample rate needs to be 2x the frequency of the signal, otherwise the Nyquist rule
is not upheld, and aliasing becomes a real problem.

https://www.mathsisfun.com/algebra/amplitude-period-frequency-phase-shift.html
The sine function takes two parameters we're intersted in: amplitude and period:
    y = amplitude * sin(period * x)
where
    period = 2pi / 1 / frequency
'''
#
# Sine wave
#
sine_amplitude = 1.0
sine_frequency = 1.0
sine_period = (2.0 * math.pi) / (1.0 / sine_frequency)
sine_sample_rate = 100
sine_step = 1.0 / sine_sample_rate
sine_time = 1.0
sine_sample_count = int(sine_time * sine_sample_rate)
sine_samples = [sine_amplitude * math.sin(sine_period * (i * sine_step)) for i in range(0, sine_sample_count)]
if plot_sine:
    axs[plot_index].plot([(sine_step * i) for i in range(0, sine_sample_count)], sine_samples)
    axs[plot_index].set_title('Sine Wave')
    axs[plot_index].set_xlim([0.0, sine_time])
    axs[plot_index].grid(True)
    plot_index += 1

#
# DFT
#
# N
#     Number of samples we perform DFT on (our sample window)
#     If it matches the sample_rate, each frequency bin will directly map to a frequency the sample_rate is able
#      to capture as per the Nyquist rule (sample_rate / 2)
# 
# nyquist_limit_index
#     Only the first half of the frequency bins are useful when the sampled input signal is a real signal
#      (the rest are redundant complex conjugates, i.e. the same but with a negative imaginary part)
# 
# magnitude
#     Just the regular length of a vector = 2.0 * sqrt(x*x + y*y) / N
#
sine_wave_dft = DFT(sine_sample_rate, sine_samples, sine_sample_rate)
if plot_sine_dft:
    axs[plot_index].bar([i for i in range(0, sine_sample_rate / 2)], sine_wave_dft)
    axs[plot_index].set_title('Sine Wave DFT')
    axs[plot_index].set_xlim([0, sine_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Upsampled sine wave
#
upsample_factor = 6
sine_upsampled_sample_rate = sine_sample_rate * upsample_factor
sine_upsampled_step = 1.0 / sine_upsampled_sample_rate
sine_upsampled_sample_count = int(sine_time * sine_upsampled_sample_rate)
sine_upsampled_samples = []
for i in range(0, sine_upsampled_sample_count):
    if i % upsample_factor == 0:
        sine_upsampled_samples.append(sine_samples[i / upsample_factor])
    else:
        sine_upsampled_samples.append(0.0)
if plot_sine_upsampled:
    axs[plot_index].plot([(sine_upsampled_step * i) for i in range(0, sine_upsampled_sample_count)], sine_upsampled_samples)
    axs[plot_index].set_title('Sine Wave Upsampled')
    axs[plot_index].set_xlim([0.0, sine_time])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Upsampled sine wave DFT
#
sine_wave_upsampled_dft = DFT(sine_upsampled_sample_rate, sine_upsampled_samples, sine_upsampled_sample_rate)
if plot_sine_upsampled_dft:
    axs[plot_index].bar([i for i in range(0, sine_upsampled_sample_rate / 2)], sine_wave_upsampled_dft)
    axs[plot_index].set_title('Upsampled Sine Wave DFT')
    axs[plot_index].set_xlim([0, sine_upsampled_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Sinc function
#
sinc_samples = []
sinc_range = 32.0
sinc_start = -sinc_range + (sinc_range / 2.0)
sinc_end = sinc_range - (sinc_range / 2.0)
sinc_sample_rate = 100
sinc_delta = 1.0 / float(sinc_sample_rate)
while sinc_start <= sinc_end:
    value = 2.0
    if sinc_start != 0.0:
        value = math.sin(2.0 * math.pi * 1.0 * sinc_start) / (math.pi * sinc_start)
    sinc_samples.append(value)
    sinc_start += sinc_delta
sinc_sample_count = len(sinc_samples)
sinc_start = -sinc_range + (sinc_range / 2.0)
if plot_sinc:
    axs[plot_index].plot([(sinc_start + (i * sinc_delta)) for i in range(0, sinc_sample_count)], sinc_samples)
    axs[plot_index].set_title('Sinc Function')
    axs[plot_index].set_xlim([sinc_start, sinc_end])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Sinc function DFT
#
sinc_dft = DFT(sinc_sample_rate, sinc_samples, sinc_sample_rate)
if plot_sinc_dft:
    axs[plot_index].bar([i for i in range(0, sinc_sample_rate / 2)], sinc_dft)
    axs[plot_index].set_title('Sinc Function DFT')
    axs[plot_index].set_xlim([0, sinc_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Rectangular window
#
rectangular_window_start = -8.0
rectangular_window_end = 8.0
rectangular_window_samples = []
rectangular_window_sample = sinc_start
while rectangular_window_sample < sinc_end:
    value = 0.0
    if (rectangular_window_sample >= rectangular_window_start) and (rectangular_window_sample <= rectangular_window_end):
        value = 1.0
    rectangular_window_samples.append(value)
    rectangular_window_sample += sinc_delta
if plot_rectangular_window:
    axs[plot_index].plot([(sinc_start + (i * sinc_delta)) for i in range(0, sinc_sample_count)], rectangular_window_samples)
    axs[plot_index].set_title('Rectangular Window')
    axs[plot_index].set_xlim([sinc_start, sinc_end])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Rectangular Windowed Sinc function
#
sinc_rectangular_windowed_samples = []
for i in range(0, sinc_sample_count):
    value = sinc_samples[i] * rectangular_window_samples[i]
    sinc_rectangular_windowed_samples.append(value)
if plot_rectangular_window_sinc:
    axs[plot_index].plot([(sinc_start + (i * sinc_delta)) for i in range(0, sinc_sample_count)], sinc_rectangular_windowed_samples)
    axs[plot_index].set_title('Rectangular Windowed Sinc Function')
    axs[plot_index].set_xlim([sinc_start, sinc_end])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Rectangular Windowed Sinc function DFT
#
sinc_rectangluar_window_dft = DFT(sinc_sample_rate, sinc_rectangular_windowed_samples, sinc_sample_rate)
if plot_rectangular_window_sinc_dft:
    axs[plot_index].bar([i for i in range(0, sinc_sample_rate / 2)], sinc_rectangluar_window_dft)
    axs[plot_index].set_title('Rectangular Windowed Sinc Function DFT')
    axs[plot_index].set_xlim([0, sinc_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Hamming window function
#
hamming_a0 = 0.54
hamming_window_start = -8.0
hamming_window_end = 8.0
hamming_window_length = hamming_window_end - hamming_window_start
hamming_window_samples = []
hamming_window_sample = sinc_start
while hamming_window_sample < sinc_end:
    value = 0.0
    if (hamming_window_sample >= hamming_window_start) and (hamming_window_sample <= hamming_window_end):
        # +8 to center the sample to start at 0 when it's -8
        value = hamming_a0 - (1.0 - hamming_a0) * math.cos((2.0 * math.pi * float(hamming_window_sample + 8.0)) / float(hamming_window_length - 1))
    hamming_window_samples.append(value)
    hamming_window_sample += sinc_delta
if plot_hamming_window:
    axs[plot_index].plot([(sinc_start + (i * sinc_delta)) for i in range(0, sinc_sample_count)], hamming_window_samples)
    axs[plot_index].set_title('Hamming Window Function')
    axs[plot_index].set_xlim([sinc_start, sinc_end])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Hamming Windowed Sinc function
#
sinc_hamming_windowed_samples = []
for i in range(0, sinc_sample_count):
    value = sinc_samples[i] * hamming_window_samples[i]
    sinc_hamming_windowed_samples.append(value)
if plot_hamminh_window_sinc:
    axs[plot_index].plot([(sinc_start + (i * sinc_delta)) for i in range(0, sinc_sample_count)], sinc_hamming_windowed_samples)
    axs[plot_index].set_title('Hamming Windowed Sinc Function')
    axs[plot_index].set_xlim([sinc_start, sinc_end])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Hamming Windowed Sinc function DFT
#
if plot_hamming_window_sinc_dft:
    sinc_hamming_window_dft = DFT(sinc_sample_rate, sinc_hamming_windowed_samples, sinc_sample_rate)
    axs[plot_index].bar([i for i in range(0, sinc_sample_rate / 2)], sinc_hamming_window_dft)
    axs[plot_index].set_title('Hamming Windowed Sinc Function DFT')
    axs[plot_index].set_xlim([0, sinc_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Perform actual filtering on upsampled Sine wave
#
# Create filter
filter_sample_rate = sine_upsampled_sample_rate
sample_delta_time = 1.0 / float(filter_sample_rate)
filter_cutoff_freq = 10
filter_length = 32 # [-8,7] = sample points
filter_shift = filter_length / 2 # Moves [-8,7] -> [0,15]
hamming_a0 = 0.54
# Compute Sinc filter and Hamming window
sinc_filter_values = []
hamming_window_values = []
filter_values = []
filter_sum = 0.0
for i in range(0, filter_length):
    sample_index_shifted = i
    sample_index = i - filter_shift
    sample_time = float(sample_index) * sample_delta_time

    sinc_value = 2.0 * float(filter_cutoff_freq)
    if sample_index != 0:
        sinc_value = math.sin(2.0 * math.pi * float(filter_cutoff_freq) * sample_time) / (math.pi * sample_time)
    sinc_filter_values.append(sinc_value)

    hamming_value = hamming_a0 - ((1.0 - hamming_a0) * math.cos((2.0 * math.pi * float(sample_index_shifted)) / float(filter_length - 1)))
    hamming_window_values.append(hamming_value)

    filter_values.append(sinc_value * hamming_value)
    filter_sum += abs(filter_values[i])
filter_normalized_values = []
#filter_normalized_values = [ -0.0032906, -0.0052635, -0.0068811, 0.0, 0.0254209, 0.0724719, 0.1311260, 0.1805961, 0.2, 0.1805961, 0.1311260, 0.0724719, 0.0254209, 0.0, -0.0068811, -0.0052635 ]
for i in range(0, filter_length):
    filter_normalized_values.append(filter_values[i] / filter_sum)
print(filter_normalized_values)
if plot_filter_sinc:
    axs[plot_index].plot([float(i) * sample_delta_time for i in range(0, filter_length)], sinc_filter_values)
    axs[plot_index].set_title('Sinc filter')
    axs[plot_index].set_xlim([0.0, float(i) * sample_delta_time])
    axs[plot_index].grid(True)
    plot_index += 1
if plot_filter_hamming:
    axs[plot_index].plot([float(i) * sample_delta_time for i in range(0, filter_length)], hamming_window_values)
    axs[plot_index].set_title('Hamming window')
    axs[plot_index].set_xlim([0.0, float(i) * sample_delta_time])
    axs[plot_index].grid(True)
    plot_index += 1
if plot_filter:
    axs[plot_index].plot([float(i) * sample_delta_time for i in range(0, filter_length)], filter_values)
    axs[plot_index].set_title('Filter')
    axs[plot_index].set_xlim([0.0, float(i) * sample_delta_time])
    axs[plot_index].grid(True)
    plot_index += 1
if plot_filter_normalized:
    axs[plot_index].plot([float(i) * sample_delta_time for i in range(0, filter_length)], filter_normalized_values)
    axs[plot_index].set_title('Filter normalized')
    axs[plot_index].set_xlim([0.0, float(i) * sample_delta_time])
    axs[plot_index].grid(True)
    plot_index += 1
# Perform filtering
sine_upsampled_filtered_samples = []
for i in range(0, sine_upsampled_sample_count):
    value = 0.0
    filter_length_for_sample = min(filter_length, sine_upsampled_sample_count - i)
    for j in range(0, filter_length_for_sample):
        value += sine_upsampled_samples[i + j] * filter_normalized_values[j]
    sine_upsampled_filtered_samples.append(value)
# Plot
if plot_filter_sine_upsampled:
    axs[plot_index].plot([(sine_upsampled_step * i) for i in range(0, sine_upsampled_sample_count)], sine_upsampled_filtered_samples)
    axs[plot_index].set_title('Sine Wave Upsampled Filtered')
    axs[plot_index].set_xlim([0.0, sine_time])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Sine Wave Upsampled Filtered DFT
#
if plot_filter_sine_upsampled_dft:
    sine_wave_upsampled_filtered_dft = DFT(sine_upsampled_sample_rate, sine_upsampled_filtered_samples, sine_upsampled_sample_rate)
    axs[plot_index].bar([i for i in range(0, sine_upsampled_sample_rate / 2)], sine_wave_upsampled_filtered_dft)
    axs[plot_index].set_title('Filtered Upsampled Sine Wave DFT')
    axs[plot_index].set_xlim([0, sine_upsampled_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Downsample
#
# Perform downsampling
downsample_factor = 5
sine_downsampled_sample_rate = sine_upsampled_sample_rate / downsample_factor
sine_downsampled_step = 1.0 / sine_downsampled_sample_rate
sine_downsampled_sample_count = sine_upsampled_sample_count / downsample_factor
sine_downsampled_samples = []
for i in range(0, sine_downsampled_sample_count):
    sine_downsampled_samples.append(sine_upsampled_filtered_samples[i * downsample_factor])
# Plot
if plot_filter_sine_upsampled_downsampled:
    axs[plot_index].plot([(sine_downsampled_step * i) for i in range(0, sine_downsampled_sample_count)], sine_downsampled_samples)
    axs[plot_index].set_title('Sine Wave Downsampled')
    axs[plot_index].set_xlim([0.0, sine_time])
    axs[plot_index].grid(True)
    plot_index += 1

#
# Downsample DFT
#
if plot_filter_sine_upsampled_downsampled_dft:
    sine_wave_upsampled_filtered_downsampled_dft = DFT(sine_downsampled_sample_rate, sine_downsampled_samples, sine_downsampled_sample_rate)
    axs[plot_index].bar([i for i in range(0, sine_downsampled_sample_rate / 2)], sine_wave_upsampled_filtered_downsampled_dft)
    axs[plot_index].set_title('Downsampled Sine Wave DFT')
    axs[plot_index].set_xlim([0, sine_downsampled_sample_rate / 2])
    axs[plot_index].grid(True)
    plot_index += 1

plt.show()