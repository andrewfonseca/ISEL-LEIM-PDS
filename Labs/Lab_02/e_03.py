# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
from SoundPlay import soundPlay

import notasdic


FS = 11025
NFFT = 512 * 2

dur = 2.
plt.close("all")

#Musica
song = ["C",4],["D",4],["E",4],["F",4]

marioSong = (
	('E5', 8), ('E5', 8), ('E5', 8), ('C5', 8), ('E5', 8),
	('G5', 4), ('G4', 4),
	('C5', 4), ('G4', 4), ('E4', 4),
	('A4', 4), ('B4', 4), ('Bb4', 8), ('A4', 4),
	('G4', 4), ('E5', 4), ('G5', 4), ('A5', 4), ('F5', 8), ('G5', 8),
	('E5', 8), ('C5', 8), ('D5', 8), ('B4', 8)
)

    


def music(song):
    
        
        
    noteList6 = []
    notedur6 = []
    for i, x in enumerate(song):
        #guarda na lista noteList6 o nome das notas
        noteList6 = np.hstack((noteList6, x[0]))
        
        #guarda na lista notedur6 a duração de cada uma das notas da musica
        notedur6 = np.hstack((notedur6, dur / x[1]))
    
    
    intDur = 0.05
    #define o tipo de onda das notas musicais
    wavType = 1
    #frequência de cada nota(11025 para se conseguir reproduzir no mediaplayer etc..)
    FS = 11025
    
    x = np.array([])
    
    #ciclo responsável por criar cada nota musical com a sua 
    for i in range(0, len(noteList6)):
        xtmp = Note_tone(noteList6[i], notedur6[i], intDur, wavType, FS)
        
        t = np.arange(0, notedur6[i], 1 / FS)
        
        xEnv = ADSR_env1(len(xtmp))
        xtmp = xtmp * xEnv
        
        x = np.hstack((x,xtmp))
        
        
        plt.plot(t[0:1000], x[0:1000], 'k')
        plt.axis([0,0.08,-1,1])
        plt.title('Sinal Nota -'+noteList6[i])
        plt.xlabel(r'$t$ (segundos)')
        
        plt.ylabel('Intensidade')
        plt.show()  
        
        
        
        
    return (x)

#Envelope ADSR para emular o efeito aquando se toca uma nota
def ADSR_env1(N = []):

    Dur = (0.1, 0.2, 0.6, 0.1)
    nA = np.floor(N * Dur[0])
    nD = np.floor(N * Dur[1])
    nS = np.floor(N * Dur[2])
    nR = N - nA - nD - nS
    

    #linha(recta) que vai de 0 a 1 com nA pontos
    xA = np.linspace(0,1, nA)
    #linha(recta) que vai de 1 a 0.8 com nD pontos
    xD = np.linspace(1, 0.8, nD)
    #linha(recta) que se mantêm constante com nS pontos
    xS = np.ones(nS) * 0.8
    #linha(recta) que vai de 0.8 a 0 com nR pontos
    xR = np.linspace(0.8, 0, nR)

#    t = np.arange(0, notedur6[i], 1 / FS)
        
    xEnv=np.hstack((xA, xD, xS, xR))

    
    return xEnv
    

    
    
def Note_tone(nota = [], notaDur = [], intDur = [], wavType = [], Fs = []):

    notasDic = notasdic.notasDic()
    for i in range(len(nota)):
        if(i == 0):
            strTmp = nota[0][0].upper()
        else:
            strTmp = strTmp + nota[i]
  
    fc = notasDic[strTmp]

    t = np.arange(0, notaDur, 1 / Fs)

    if wavType == 1:
        x = np.cos(2 * np.pi * fc * t)
        
    elif wavType == 2:
        x = np.square(2 * np.pi * fc * t)
    elif wavType == 3:
        x = np.sawtooth(2 * np.pi * fc * t, 0.5)
    elif wavType == 4:
        x = np.sawtooth(2 * np.pi * fc * t)
    else:
        print ('\n wave type (%d) not available (only ints 1-4)\n'%wavType)
    
    return x




N = 4096
x = music(song)
plt.figure(facecolor = 'w', figsize = (10, 20))
plt.title('Sinal')
plt.plot(x)
plt.axis('tight')
plt.savefig("lab2ex3_Sinal.png", bbox_inches = 'tight', transparent = False)
plt.show()

    
soundPlay.soundPlay(x,FS)
filename = 'x3.wav'
x1Int = np.int16(x * 2**13)
wavfile.write(filename, FS, x1Int)

xfft = np.fft.fft(x[0:N])

freq1 = np.fft.fftfreq(len(xfft)) * FS
x1mag = np.abs(xfft) / N
Xfase = np.angle(xfft)

plt.figure(facecolor = 'w', figsize = (10, 20))

#Espectro amplitude
plt.stem(freq1, x1mag, 'k', linewidth = 3)


plt.ylabel('Espectro amplitude', fontsize = 18)
plt.xlabel('f(Hz)', fontsize = 18)
plt.xticks(fontsize = 22)
plt.yticks(fontsize = 22)
plt.grid()
plt.savefig("lab2ex3_espectroAmplitude.png", bbox_inches = 'tight', transparent = False)
plt.figure(facecolor = 'w', figsize = (10, 20))

#Espectro Fase
Xfase = np.angle(xfft)
plt.stem(freq1, Xfase, 'k', linewidth = 3)
plt.axis([-1100, 1100, -np.pi, np.pi])

plt.ylabel('Espectro de fase', fontsize = 18)
plt.xlabel('f(Hz)', fontsize = 18)
plt.xticks(fontsize = 22)
plt.yticks(fontsize = 22)
plt.grid()
plt.savefig("lab2ex3_espectroFase.png", bbox_inches = 'tight', transparent = False)
plt.show()

#Espectrograma

plt.figure(facecolor = 'w', figsize = (30, 20))
#plt.specgram(x, NFFT=N*2, Fs=FS*2, noverlap=0)
plt.specgram(x, NFFT = NFFT, Fs = FS, noverlap = 0)
plt.savefig("lab2ex3_espectrograma.png", bbox_inches = 'tight', transparent = False)
plt.xlabel('Tempo(s)', fontsize = 18)
plt.ylabel('f(Hz)', fontsize = 18)
plt.axis('tight')
plt.show()
