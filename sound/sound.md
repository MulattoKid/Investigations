# Sound

## The Absolute Basics
Audio (or sound) are waves that move through some medium (for our purposes let's stick to air). The waves are caused by some vibration. The faster the vibration the higher the frequency, and the slower the vibration the lower the frequency.
The larger the vibration (amplitude) the louder the sound, and the smaller the vibration the quiter the sound. Humans can on average perceive (hear) waves that are in the range 20 Hz to 20'000 kHz, while the quietest sound we can hear is 0 dB (we'll get to what that means below).

## Decibel
The `decibel` is a relative unit of measurement (one tenth of a `bel`), and expresses the ratio of two power values on a logarithmic scale (`10log(A/B)`). Thus, two signals who's power levels differ by `1 dB` have a power ratio of `10^(1/10)`.
For root-power values, such as sound pressure, it's common to use the following formula instead: `2log(A^2/B^2) = 20log(A/B)`.

Now, the confusing thing to me about decibel is that, as mentioned above, it's a relative unit of measure. Saying that some sound is 10 dB doesn't really mean anything unless we know what we're comparing against. However, usually 0 dB is defined as 20 micro-Pascal (uPa). Pascal is the unit of pressure, with 20 uPa being considered the threshold of what human ears can perceive (roughly the sound of a mosquito flying 3m away according to Wikipedia).

Let's look at a basic example: what does it mean if we say a guitar produces a sound that's 100 dB? Well, using our formula it means that
```
100 dB = 20*log(X / 20 uPa)
100 / 20 = log(X / 20)
10^(100 / 20) = X / 20
X = 20 * 10^(100 / 20) = 2 000 000 uPa
---
2000000 uPa Guitar / 20 uPa Base = 100000x
```
the guitar is 100K times louder than what the human ear can perceive.

So, to summarize, decibel is the ratio between two values, and usually the reference value is 20 uPa when talking about sound.

## Bandwidth
Bandwidth is the difference between the highest and lowest frequencies in a signal. E.g. if an analog signal has frequencies between 20 Hz and 100 Hz, its bandwidth is 80 Hz. Now, while the bandwidth of a signal is determined by the signal itself, the ability of an ADC to capture all the frequencies in the signal depends on its sample rate. Due to the Nyquist theorem, an ADC can only capture frequencies up to 1/2 of its sample rate. Thus, the bandwidth of an ADC is usually referred to as the frequency range it can capture, i.e. [0, sample rate / 2].

## Quantization
Quantization is the process of mapping inputs from a large set of values (often a continuous set) to a set of output values (often with a finite number of elements). The larger the set of output values is, the higher resolution/quality the quantizied data will be.

## ADC (Analog to Digital Converter)
An ADC isa system that converts a continuous-time and continuous-amplitude analog signal to a discrete-time and discrete-amplitude digital signal. An ADC system consists of two parts:
1) a sampler, which samples the analog signal at a fixed frequency/sample-rate (usually)
2) a quantizizer, which converts the sampled real value with an approximation from a fixed set (integer, floating-point, etc.)

THe quality of an ADC comes down to two things:
1) the sample rate, which directly impacts the bandwidth the ADC is able to capture
2) the quantization rate (bitrate), which directly impacts the level of error/noise in the captured samples

An ADC typicall sits after a microphone in a recording setting. The micrpohone's diaphragm (a thin piece of material, often metal) is "hit" by the sound waves and vibrates, thus passing the energy contained in the sound waves through the rest of the microphone, which at the end is output as an electrical signal. The ADC takes this analog electrical signal/current as an input and produces the digital output signal.

## DAC (Digital to Analog Converter)


## Amplifier


## Gain


## DC Offset


## DC Gain


## Links
- https://en.wikipedia.org/wiki/Decibel#Audio_electronics
- https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level
- https://en.wikipedia.org/wiki/Power,_root-power,_and_field_quantities
- https://en.wikipedia.org/wiki/Pascal_(unit)
- https://en.wikipedia.org/wiki/Bandwidth_(signal_processing)
- https://en.wikipedia.org/wiki/Quantization_(signal_processing)#Analog-to-digital_converter
- https://en.wikipedia.org/wiki/Analog-to-digital_converter
- https://en.wikipedia.org/wiki/Gain_(electronics)