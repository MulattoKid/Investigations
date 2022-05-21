# Sound

## The Absolute Basics
Audio (or sound) is are waves that move through some medium (for our purposes let's stick to air). The waves are caused by some vibration. The faster the vibration the higher the frequency, and the slower the vibration the lower the frequency.
The larger the vibration the louder, and the smaller the vibration the quiter. Humans can on average perceive (hear) waves that are in the range 20 Hz to 20'000 kHz, while the quietest sound we can hear is 0 dB (we'll get to what that means later).

## Decibel
The `decibel` is a relative unit of measurement (one tenth of a `bel`), and expresses the ratio of two power values on a logarithmic scale (`10log(A/B)`). Thus, two signals who's power levels differ by `1 dB` have a power ratio of `10^(1/10)`.
For root-power values, such as sound pressure, it's common to use the following formula instead: `2log(A^2/B^2) = 20log(A/B)`.

Now, the confusing thing to me about decibel is that, as mentioned above, it's a relative unit of measure. Saying that some sound is 10 dB doesn't really mean anything unless we know what we're comparing against. However, 0 dB is usually defined
20 micro-Pascal (uPa). Pascal is the unit of pressure, with 20 uPa being considered the threshold of what human ears can perceive (roughly the sound of a mosquito flying 3 m away according to Wikipedia).

Let's look at a basic example: what does it mean if we say a guitar produces a sound that's 100 dB? Well, using our formula it means that
```
100 dB = 20*log(X / 20 uPa)
10^(100 / 20) = X / 20
X = 20*10^(100 / 20) = 2 000 000 uPa
2000000 / 20 = 100 000
```
the guitar is 100K times louder than what the human ear can perceive.

So, to summarize, decibel is the ratio between two values, and usually the reference value is 20 uPa when talking about sound.

## Gain
## ADC (Analog to Digital Converter)
## DAC (Digital to Analog Converter)
## Amplifier
## DC Offset
## DC Gain

## Links
- https://en.wikipedia.org/wiki/Decibel#Audio_electronics
- https://en.wikipedia.org/wiki/Sound_pressure#Sound_pressure_level
- https://en.wikipedia.org/wiki/Power,_root-power,_and_field_quantities
- https://en.wikipedia.org/wiki/Pascal_(unit)