#!/usr/bin/env python
# coding: utf-8

# In[6]:


import nltk
import pyaudio
import subprocess
import wave
import os
import urllib
import time
import math
import speech_recognition as sr
from googletrans import Translator


# In[7]:


TOTAL_DURATION = 0
time_start=[]
time_end=[]
sentstring=''

def time_notation(sec):
    secs = sec%60
    mins = sec/60
    hours = round(mins/60)
    mins = round(mins%60)
    

    if hours<10:
        hours = str(0)+str(hours)
    if mins<10:
        mins = str(0)+str(mins)
    if secs<10:
        secs = str(0)+str(secs)

    return str(hours)+":"+str(mins)+":"+str(secs)


# In[8]:


def speech_to_text(audio_fname): #converts audio stream to flac and sends our flac file to google speech API where it gets converted to text
    '''filename = audio_fname
    del_flac = False
    if 'flac' not in filename:
        del_flac = True
        print("Converting to flac")
        subprocess.call(['ffmpeg', '-i', filename.split('.')[0]+'.flac',
                   'filename'])
        print("Converted to flac")'''
    
    r = sr.Recognizer()
    flac_cont=sr.AudioFile('OSR_us_000_0010_8k.wav')
    with flac_cont as source:
        audio=r.record(source)
    res=r.recognize_google(audio)
    sentstring+=res
    return res
    try:
        print("Successful")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def correct_silences(silence):
    pos_to_delete = []
    for i in range(len(silence)-1):
        if(silence[i]==silence[i+1]):
            pos_to_delete.append(i)
    #reverse list
    pos_to_delete = pos_to_delete[::-1]
    for i in pos_to_delete:
        silence.pop(i)
    return silence

def get_timestamp(silence):
    speech_mins = []
    speech_sec = []
    temp1 = ""
    temp2 = ""
    for i in range(len(silence)-1):
        temp1 = str(time_notation(silence[i])) + " --> " + str(time_notation(silence[i+1]))
        temp2 = str(silence[i]) + " --> " + str(silence[i+1])
        speech_mins.append(temp1)
        speech_sec.append(temp2)
    return speech_mins,speech_sec

def write_srt_file(speech_mins,speech_sec):
    f = open('sub.srt', 'a')
    write_chunk = ""
    for i in range(len(speech_mins)):
        string = split_audio_file(speech_sec[i])
        print(string)
        
        if not string:
            write_chunk = str(i+1) + "\n" + str(speech_mins[i]) + "\n\n"
        elif string:
            write_chunk = str(i+1) + "\n" + str(speech_mins[i]) + "\n" + str(string[0]) + "\n\n"

        f.write(write_chunk)
    f.close()
    

def split_audio_file(time):
    time = time.split()
    if float(time[0])<1:
        startTime = str(time[0])
        duration = str(float(time[2]) - float(time[0]) + 1)
    elif(float(time[2])>=TOTAL_DURATION-1):
        startTime = str(float(time[0])-1)
        duration = str(float(time[2]) - float(time[0]))
    else:
        startTime = str(float(time[0])-1)
        duration = str(float(time[2]) - float(time[0]) + 1)
    subprocess.call(['ffmpeg', '-ss',startTime,'-t',duration,'-i','audio.wav','-vn','-ac','1','-ar',
                     '16000','-acodec','flac','convert.flac'])
    string =  speech_to_text('nlp.flac')
    
    #subprocess.call(['rm' 'convert.flac'])
    #
    return string

def mainprog():
    print("Calculating time stamps based on silence intervals\n")
    try:
        subprocess.call(['del','audio.wav'])
    except:
        pass
    subprocess.call(['ffmpeg', '-i', 'nlp.mp4','-vn','audio.wav'])
    w = wave.open('audio.wav','r')
    frame = True
    start = 0
    THRESHOLD = 90
    MAJORITY = 0.6
    CHUNK = int(math.floor(w.getframerate()/3))
    num_of_chunks = 0
    silence = []
    fi = 1
    count = 1
    while frame:
        frame = w.readframes(CHUNK)
        flag = True
        count = 0
        for i in range(len(frame)):
            try:
                if ord(frame[i])<THRESHOLD:
                    count+=1
            except:
                if frame[i]<THRESHOLD:
                    count+=1
        num_of_chunks+=1
        #print count, w.getframerate()
        if (float(count)/w.getframerate()) > MAJORITY:
            silence.append(float(w.tell()-CHUNK)/w.getframerate())        
    TOTAL_DURATION = float(num_of_chunks)/3
    silence.append(int(TOTAL_DURATION))
    silence = correct_silences(silence)
    print(silence)
    speech_mins,speech_sec = get_timestamp(silence)
    print(speech_mins)
    print('\n\n')
    print(speech_sec)
    print('timestamps calculated, now sending data to google speech api')
    write_srt_file(speech_mins,speech_sec)
    

    
        


# In[9]:


mainprog()
from nltk.tokenize import sent_tokenize, word_tokenize

translator = Translator()
translated_text=translator.translate(string)
b=word_tokenize(string)
time_proportion=[time_end[i]-time_start[i] for i in len(time_start)]
sumtime=sum(time_proportion)
for i in len(time_proportion):
    time_proportion[i]/=sumtime
no_of_stamped_words=[int(i*len(b)) for i in time_proportion]
stamp_sentence=[]
num=0
for i in no_of_stamped_words:
    stamp_sentences.append(b[num:num+i])
    num+=i

for i in time_start: 
    write_to_srt(get_timestamp(time_start[i],time_end[i]),stamp_sentence[i])
   


# In[5]:





# In[ ]:


#This code is not implemented and should be placed in main program
from nltk.tokenize import sent_tokenize, word_tokenize

translator = Translator()
translated_text=translator.translate(string)
b=word_tokenize(string)
time_proportion=[time_end[i]-time_start[i] for i in len(time_start)]
sumtime=sum(time_proportion)
for i in len(time_proportion):
    time_proportion[i]/=sumtime
no_of_stamped_words=[int(i*len(b)) for i in time_proportion]
stamp_sentence=[]
num=0
for i in no_of_stamped_words:
    stamp_sentences.append(b[num:num+i])
    num+=i

for i in time_start: 
    write_to_srt(get_timestamp(time_start[i],time_end[i]),stamp_sentence[i])


# In[ ]:




