#!/usr/bin/env python
from scipy import signal
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import wave, argparse, sys, time

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", help="Name of the unfiltered audio.")
    parser.add_argument("-l", "--lowpass", help="Low pass filter. Default value: 5000.", type=int)
    parser.add_argument("-hi", "--highpass", help="High pass filter. Default value: 5000.", type=int)
    parser.add_argument("-bp", "--bandpass", help="Band pass filter. Default value: [5000,10000].", type=int)
    parser.add_argument("-bs", "--bandstop", help="Band Stop filter. Default value: [5000,10000].", type=int)
    parser.add_argument("-o", "--output", help="Name of the output wav file. Default value: output.wav.")
    parser.add_argument("-s", "--sampling", help="Sampling rate. Default value: same as input.", type=int)
    args = parser.parse_args()

    filterfreq = [5000]
    output = "output.wav"

    if args.output:
        output = args.output
    else if args.lowpass:
        filterfreq[0] = args.lowpass
        filtertype = "lowpass"
    else if args.highpass:
        filterfreq[0] = args.highpass
        filtertype = "highpass"
    else if args.bandpass:
        filterfreq[1] = [10000]
        filterfreq = args.bandpass
        filtertype = "bandpass"
    else if args.bandstop:
        filterfreq[1] = [10000]
        filterfreq = args.bandstop
        filtertype = "bandstop"
    else :
        print("You have to choose a filter.")
        time.sleep(2)
        sys.exit()

    original = wave.open(args.INPUT, 'rb')
    samplingrate = wave.Wave_read.getframerate(original)
    nyqfreq = samplingrate / 2
    original.close()

    if args.bandpass == True or args.bandstop == True :
        cutoff[0] = filterfreq[0] / nyqfreq
        cutoff[1] = filterfreq[0] / nyqfreq
    else :
        cutoff = filterfreq[0] / nyqfreq

    if args.sampling:
        samplingrate = args.sampling

    print('Input file: %s.' % args.INPUT)
    print('Output file: %s.' % output)
    print('Sampling rate: %d.' % samplingrate)
    if args.lowpass :
        print('Low pass filter: %d.' % filterfreq)
    if args.highpass :
        print('High pass filter: %d.' % filterfreq)
    if args.bandpass :
        print('Band pass filter: %d.' % filterfreq)
    if args.bandstop :
        print('Band stop filter: %d.' % filterfreq)

    return (args.INPUT, output, filtertype, samplingrate, cutoff, nyqfreq)

def filter(inpt, output, filtertype, samplingrate, cutoff, nyqfreq):
    input_data = read(inpt)
    audio = input_data[1]
    b, a = signal.butter(8, cutoff, btype=filtertype)
    filteredaudio = signal.filtfilt(b, a, audio)
    write(output, samplingrate, filteredaudio)
    write("output.wav", samplingrate, output)

    ### Screens
    #Comparison
    plt.plot(audio, label='Original Audio')
    plt.plot(filteredaudio, label='Filtered Audio')
    plt.title('Filtered & Unfiltered comparison', fontsize=14)
    plt.xlabel('Time (Hz)')
    plt.ylabel('Range')
    plt.legend()
    plt.savefig('comparison.png')

    ### Screens
    # Comparison
    f, FFT = signal.periodogram(audio, samplingrate)
    e, EET = signal.periodogram(filteredaudio, samplingrate)
    plt.plot(f, FFT)
    plt.plot(e, EET)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('comparison2.png')
    # Original only
    plt.plot(f, FFT)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('original.png')
    # Filtered only
    plt.plot(e, EET)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('filtered.png')


if __name__ == '__main__':
    inpt = parser()
    filter(*inpt)