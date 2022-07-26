# Sound Systems

## Primer
Before we get started, it's good to describe a few things.

### Elementary Charge
The elementary charge is the electric charge of a single proton, or the magnitude of the negative electric charge of a single electron, measured in Coulombs.

```
e = 1.602176634*10^−19 coulombs
```

### Coulomb
The coulomb is a derived unit of electric charge, and is defined as

```
1C = 1A * 1s
```

Knowing that the elementary charge is

```
e = 1.602176634*10^−19 coulombs
```

we can determine that

```
1e = 1.602176634*10^−19C
1C = 1e / 1.602176634*10^−19 = 6241509074460762607.776e
```

I.e. roughly 6.2*10^18 elementary charges.

### Ampere
The ampere is the unit of electric current, and is defined as

```
1A = 1C / s = 6.2*10^18 elementary charges flowing past a point per second
```

### Voltage
Voltage (V) is the measure of electric potential between two points, measured in volt (V). More simply, it's the amount of energy that potentially can be provided when elementary charges are moving

```
1V = 1 joule / 1 coulomb
```

The higher the voltage, the more energy can potentially be provided.

### Restistance
Resistance (R) is the measure of an objects opposition to the flow of elementary charges, measured in Ohms (Ω). The higher the resistance, the less elementary charges will pass through the object per second.

### Impedance
Impedance (R) is the AC version of restiance: it's also the opposition to current. In addition to any resistance in the circuit, impedance also encompasses the effects induction and capacitance. It's also measured in Ohms (Ω).

### Electric Current
Electric current (I) is the measure of elementary charges moving through a conductor, measured in amperes. Ohm's law defines it as

```
I = V / R
```

### Alternating Electric Current
Alternating electric current (AC) is an electric current which periodically reverses its direction and changes magnitude contiuously with time. The alernation usually happens as a sine wave. The alternation thus naturally has a frequency.

### Direct Electric Current
Direct electric current (DC) is a one-directional flow of elementary charges. It can be viewed as alternating current with a frequency of 0.

### Watt
Watt (W) is a unit of power, and is measured in joules/s.

```
1W = 1V * 1A
1W = (1J / 1C) * (1C / 1s)
1W = 1J / 1s
```

### Root Mean Square
The root mean square (RMS) of a set of numbers is the square root of the mean square.

```
RMS = sqrt((x_0 + x_1 + ... + x_N) / N)
```

The RMS for AC is equal to the value of the constant DC that would produce the same power.

### Decibel
The decibel is a relative unit of measurement, equal to 1/10 of a bel. It expresses the ratio of two values of a power or root-power quantity on a logarithmic scale. Voltage, electric current and sound pressure are all root-power quanitites (quantities which the square of which is proportional to power). Two signals whose levels differ by one decibel have a power ratio of 10^1/10, or root-power ratio of 10^1/20.

An important aspect to notice is that being told that some sound pressure level is 20dB is only really useful if we know what the reference is. However, usually there's a common reference value unless another one is specified, and for sound pressure level (SPL) the reference is 20 micropascal (uPa). Knowing this, let's work out our example: what SPL is a sound if it's 20dB?

We know that a bel (B) is the ratio of two values on a logarithmic scale, i.e.

```
B = log10(x / y), y = reference
```

and since a decibel is 1/10 of a bel, we get

```
dB = 10log10(x / y)
```

However, since we're working with SPL, which is a root-power quantity, it is usual to use the squares of the quantities as the square of the quantity is proportional to its power

```
dB = 10log10(x^2 / y^2)
dB = 20log10(x / y)
x = 10^(dB / 20) * y
x = 10^(20dB / 20) * 0.000002Pa = 0.0002Pa
```

### Total Harmonic Distorition and Noise
https://en.wikipedia.org/wiki/Total_harmonic_distortion

### Signal-to-Noise-Ratio
Signal-to-noise-ratio (SNR) is a measure that compares the level of a desired signal to the level of the background noise. It's defined as the ratio between signal power and noise power, and is often expressed in decibels. A ratio higher than 0dB indicates more signal power than noise power.

### Sensitivity
Sensitivity is a measure of how loud a sound a pear of headphones can create given a power consumption of 1mW. The higher the sensitivity, the less power is usually required to create loud sound. However, the efficiency (how efficient power is "converted" to sound) also impacts this. Low efficiency means a lower ratio between the dBSPL created with e.g. a 1mW and 0.9mW power consumption.

## The Audio Signal Journey
Let's imagine the following basic sound system:

```
          Optical/USB/Coax        RCA Cable        AUX
Computer ------------------> DAC -----------> AMP -----> Headphones
```

It has 4 main components:
1) Computer: outputs a digital audio signal 
2) DAC: converts the digital signal into an analog voltage signal
3) Amplifier: amplifies the analog voltage signal
4) Headphones: moves the speaker elements to create sound waves

The aim with this article is to highlight and explain this process in an understandable manner.

## Computer
Your computer has music stored on it in some digital form, but let's stick to raw uncompressed data for simplicity.

The digital audio data is stored on a per-channel and per-sample basis, with a specific number of bits used to encode each sample, and a specific number of samples per second. I.e. for 8-bit mono-channel audio stored at 44100KHz, there are 441000 samples stored for each second of audio data, each consuming 8 bits. If the audio instead was stereo, there would be twice as many samples stored for each second.

When the computer is instructed to play an audio file, this data is sent to another system which is able to convert this digital discrete signal to an analog continuous signal, a DAC. The format of the digital signal determines how the DAC converts the signal. E.g. with a 16-bit digital signal, each sample can have 65356 distinct values, usually in the range [-32768, 32767] (`int16_t`).

However, on modern computers it's very likely that more than one audio signal will be played at a time. E.g. you're listening to music, playing a video game, and get an email notification. Your music might be stereo 24-bit 44100KHz, the video game stereo 16-bit 48000KHz and the notification mono 16-bit 441000KHz. How should all these be played at the same time? Well, your OS will most likely be doing some kind of softare audio mixing behind the scenes, converting all the digital input signals to a predefined format, e.g. stereo 16-bit 48000KHz. This means you might not be listening to the quality of music you think you are, but it depends on the quality of the music and the mixing the OS does behind the scenes. 

Furthermore, this software mixing is also what allows you to adjust the audio volume through your OS. The volume of an audio signal is determined by the amplitude of the analog output signal, so how could the OS impact this by changing the digital signal? Well, simply by shrinking the samples from their original bit-depth to a smaller bit-depth, i.e. multiply each sample with a value < 1.

Finally, all of this mixing is likely to impact the quality of your original digital signal. It might have its sample rate changed, a change in bit-rate, a change in amplitude, and more. Any of these will impact the quality of your original digital signal, and if performed to a large enough extent can result in audible differences. However, e.g. in Windows it's possible for an audio application to get exclusive control (using the WASAPI) over an audio output device to avoid any OS mixing. 

## DAC
A DAC converts a digital signal to an analog one, in the case of audio to an electrical signal that varies in voltage. We know from Ohm's law that

```
I = V / R
```

so the voltage directly relates to how much current will flow through the electrical circuit, and end up moving the speaker elements at the end. The more voltage the more displaced the speaker elements will be. Thus, the larger the amplitudes in the signal are, the louder the created sound will be. DACs are typically rated with a maximum ouptut voltage, indicating the maximum amount of voltage they can output given any digital input signal.

A DAC's ability to reconstruct the original analog signal is limited by the bit-depth and the sample-rate of the digital input signal. A low bit-depth will not be able to represent as many different amplitudes as a higher bit-depth, and the highest possible frequency the DAC can reconstruct is half of the digital sample-rate (the Nyquist frequency). However, these properties are out of the DAC's control, so it can only work with what it gets.

When reconstructing the analog signal a DAC is likely to introduce some harnomic distortion and noise (THD+N). This is expressed as a percentage of the output signal. A low percentage is desirable here, as we want as little of the output signal to be noise, and rather our converted voltage signal.

## Amplifier
An amplifier, as the name suggests, amplifies an input signal, i.e. increases the amplitude of the signal. With audio signals this results in louder a sound being created by the speakers, as more current ends up at the speakers.

Just as with a DAC, an amplifier will introduce noise to its output signal. This noise is also amplified along with the input signal, so increasing the amplification will not decrease the percentage of noise in the output signal. It's also likely than when amplifying a signal more, more noise is also introduced by the amplifier, i.e. the signal-to-noise-ratio (SNR) increases. The SNR is often expressed in dB, and is the ratio of the output signal to the noise in the output signal, with a higher value being desirable.

An important point when picking an amplifier is making sure it's a good fit with the DAC, as the DAC is feeding the amplifier. The key point here is impedance matching, i.e. making sure that the output impedance of the DAC and the input impedance of the amplifier are a good match. A good match here is defined as allowing as much of the voltage signal being outputted from the DAC into the amplifier, but as little current as possible. This is because the audio signal is in the voltage signal, but we don't want current feeding into the amplifier as this will create additional artifacts. So, what creates this desirable scenario? A low DAC output impedance, and a high amplifier input impedance. The reason this is good is that the two impedances act as a voltage divider:

```
DAC -- R1 -- -- AMP
            |
           R2
```

where R1 is the DAC output impedance, and R2 is the amplifier input impedance. R1 being small allows most of the voltage signal to pass from the DAC to the amplifier. R2 being large limits the current flowing in the entire circuit.

Finally, the amplifier also has an output impedance, which generally should be as small as possible. The larger it is, the more the output voltage signal will be reduced, and we need as much of it as possible to drive our speaker elements.

## Headphones
Finally, we end up at our headphones. Given some current, the elements in them will move, producing sound waves. The more current, the more the elements move, and conversely. Headphones have several important specifications, but two are extra important: impedance, and sensitivity.

High impedance headphones require a more amplified signal, simply because less current reaches the sound elements. This means that high impedance headphones usually require a dedicated amplifier, and cannot be powered by mobile units, e.g. phones.

High sensitivity headphones produce a louder sound with a given current than headphones with a low sensitivity.

Combining these two aspects we get four scenarios:
- Low impedance, low sensitivity: more current reaches the sound elements, and relatively more current is needed to produce a loud sound
- Low impedance, high sensitivity: more current reaches the sound elements, and relatively little current is needed to produce a loud sound
- High impedance, low sensitivity: less current reaches the sound elements, and relatively more current is needed to produce a loud sound
- High impedance, high sensitivity: less current reaches the sound elements, and relatively little current is needed to produce a loud sound

There's also the efficiency aspect, but that's usually not as important.

## Audio System Example
We start with the output device, the headphones (Jerry Harvey JH7). They're specifications are
- Sensitivity: 124dB @ 1mW
- Impedance: 17Ω

These headphones have relatively low impedance, meaning a lot of ampilification probably isn't necessary. They are also relatively sensitive, so not a lot of power is needed for them to create loud sounds.

Next is the ampilifier, Schiit Magni 2. Its specifications are
- Max power @ 16Ω: 1.8W RMS per channel
- Output impedance: 0.2Ω
- Input impedance: 25kΩ

16Ω is pretty close to 17Ω which the headphones are rated at, so it's fair to use that for reasoning. At max ampilification the Magni 2 can at most output 1.8W; that's far more than the 1mW needed by the headphones to create a 124dB sound. Combined with the fact that the total impedance will be around 17Ω, allowing most of the current through the circuit, means it's likely that very little amplification is needed when using the amplifier with this pair of headphones.

Finally, the DAC, Schiit Modi 2 Über. Its specifications are
- Max output: 2V
- Output impedance: 75Ω

We see that the output impedance of the DAC and the input impedance of the amplifier create a good voltage divider, which is good.
