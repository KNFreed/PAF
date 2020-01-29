#!/usr/bin/env python

from scipy import signal
from scipy.io.wavfile import read, write
import numpy as np
import matplotlib.pyplot as plt
import wave, argparse, sys, time

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", help="Name of the unfiltered audio.")
    parser.add_argument("-l", "--lowpass", help="Low pass filter. Default value: 5000.", type=int)
    parser.add_argument("-hi", "--highpass", help="High pass filter. Default value: 5000.", type=int)
    parser.add_argument("-bp", "--bandpass", help="Band pass filter. Default value: [5000,10000].", nargs='+', type=int)
    parser.add_argument("-bs", "--bandstop", help="Band Stop filter. Default value: [5000,10000].", type=list)
    parser.add_argument("-o", "--output", help="Name of the output wav file. Default value: output.wav.")
    parser.add_argument("-s", "--sampling", help="Sampling rate. Default value: same as input.", type=int)
    args = parser.parse_args()

    filterfreq = [5000,10000]
    output = "output.wav"

    if args.output:
        output = args.output
    elif args.lowpass:
        filterfreq[0] = args.lowpass
        filtertype = "lowpass"
    elif args.highpass:
        filterfreq[0] = args.highpass
        filtertype = "highpass"
    elif args.bandpass:
        filterfreq = args.bandpass
        filtertype = "bandpass"
    elif args.bandstop:
        filterfreq = args.bandstop
        filtertype = "bandstop"
    else:
        print("You have to choose a filter.")
        time.sleep(2)
        sys.exit()

    original = wave.open(args.INPUT, 'rb')
    samplingrate = wave.Wave_read.getframerate(original)
    nyqfreq = samplingrate / 2
    original.close()
    if (filtertype == "bandstop") or (filtertype =="bandpass"):
        cutoff = [filterfreq[0]/nyqfreq, filterfreq[1]/nyqfreq]
        cutoffreq = filterfreq
    else:
        cutoff = filterfreq[0] / nyqfreq
        cutoffreq = filterfreq[0]

    if args.sampling:
        samplingrate = args.sampling

    print('Input file: %s.' % args.INPUT)
    print('Output file: %s.' % output)
    print('Sampling rate: %d.' % samplingrate)
    if args.lowpass :
        print('Low pass filter: %d.' % filterfreq[0])
    if args.highpass :
        print('High pass filter: %d.' % filterfreq[0])
    if args.bandpass :
        print('Band pass filter: %d - %d.' % (filterfreq[0],filterfreq[1]))
    if args.bandstop :
        print('Band stop filter: %d - %d.' % (filterfreq[0],filterfreq[1]))

    return (args.INPUT, output, filtertype, samplingrate, cutoff, nyqfreq, cutoffreq)

def filter(inpt, output, filtertype, samp, cutoff, nyqfreq, cutoffreq):
    input_data = read(inpt)
    audio = input_data[1]
    b, a = signal.butter(5, cutoff, btype=filtertype)
    filteredaudio = signal.lfilter(b, a, audio)

    ### Screens
    #Bode
    w, H = signal.freqz(b, a, worN=8000)
    w *= samp / (2 * np.pi)  # Convert from rad/sample to Hz
    plt.title('Bode Diagram')
    H_dB = 20 * np.log10(abs(H))  # Convert to dB
    plt.plot(w, H_dB)
    plt.ylabel('Magnitude [dB]')
    plt.xlim(0, samp / 2)
    plt.ylim(-80, 6)
    if filtertype == "lowpass" or filtertype == "highpass":
        plt.axvline(cutoffreq, color='red')
    else :
        plt.axvline(cutoffreq[0], color='red')
        plt.axvline(cutoffreq[1], color='red')
    plt.axhline(-3, linewidth=0.8, color='black', linestyle=':')
    plt.grid()
    plt.savefig('bode.png')
    plt.close()

    # Plot the phase response
    phi = np.angle(H)  # Argument of H
    phi = np.unwrap(phi)  # Remove discontinuities
    phi *= 180 / np.pi  # convert to degrees
    plt.suptitle('Bode Diagram')
    plt.semilogx(w,phi)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Phase [°]')
    plt.xlim(0, samp / 2)
    plt.ylim(-360, 0)
    plt.yticks([-360, -270, -180, -90, 0])
    if filtertype == "lowpass" or filtertype == "highpass":
        plt.axvline(cutoffreq, color='red')
    else:
        plt.axvline(cutoffreq[0], color='red')
        plt.axvline(cutoffreq[1], color='red')
    plt.grid()
    plt.savefig('phase.png')
    plt.close()

    #Comparison
    plt.plot(audio, label='Original Audio')
    plt.plot(filteredaudio, label='Filtered Audio')
    plt.title('Filtered & Unfiltered comparison', fontsize=14)
    plt.xlabel('Time (Hz)')
    plt.ylabel('Range')
    plt.legend()
    plt.savefig('comparison.png')
    plt.close()

    ### Screens
    # Comparison
    f, FFT = signal.periodogram(audio, samp)
    e, EET = signal.periodogram(filteredaudio, samp)
    plt.plot(f,FFT)
    plt.plot(e,EET)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('comparison2.png')
    plt.close()

    # Original only
    plt.plot(f, FFT)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('original.png')
    plt.close()
    # Filtered only
    plt.plot(e, EET)
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Module')
    plt.xlim(0, nyqfreq)
    plt.ylim(0, 100)
    plt.grid()
    plt.title('Freq visualisation', fontsize=14)
    plt.savefig('filtered.png')
    plt.close()

    #Audio spectrum of filtered audio
    Outputfile = np.fft.ifft(FFT)
    plt.plot(Outputfile)
    plt.ylabel('Amplitude')
    plt.xlim(0, 2000)
    plt.grid()
    plt.title('Signal after filter', fontsize=14)
    plt.savefig('Signal.png')
    plt.close()

    Outputfile = Outputfile.astype('uint8')
    write(output, samp, Outputfile)


if __name__ == '__main__':
    inpt = parser()
    filter(*inpt)