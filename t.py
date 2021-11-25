from re import S
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat, ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import AudioOutputConfig

import io
import wave
import os
import time
import sys

from Scraper import ScraperWuxiaworld


class TTS:
    cfg = []
    path = "./"

    def SetConfig(self, i):
        if i>=len(self.cfg) or i<0:
            print("\nError: Limit count cfg")
            sys.exit()

        self.speech_config = SpeechConfig(
            subscription = self.cfg[i][0],
            region = self.cfg[i][1]
        )

        self.speech_config.speech_recognition_language = "ru-RU"
        self.speech_config.speech_synthesis_voice_name = "ru-RU-DariyaNeural"
        self.speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])

        self.synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

    def Start(self, startPage, step):
        self.SetConfig(2)

        scraper = ScraperWuxiaworld()
        scraper.InitLinksLOM()

        text = []
        for i in range(startPage, startPage + step):
            text += scraper.LordOfMysteries(i)
        
        gText = ""
        countWav = 0
        for i in range(len(text)):
            gText += text[i]
            
            if len(gText) > 7000 or i == len(text)-1:
                tPath = f"temp/speech{countWav}.wav"
                ttPath = f"temp/speech{countWav+1}.wav"

                if (not os.path.isfile(tPath)): #or (not os.path.isfile(ttPath)):
                    self.SynthesizeVoice(gText, countWav)

                gText = ""
                countWav += 1
            
            print(f"\r{round( (i*100)/len(text) )}% ", end="")

        self.ConcatWav(f"{startPage}-{startPage + step - 1}")
        self.ClearAll()

    def SynthesizeVoice(self, text, index):
        fileName = self.path + f"temp/speech{index}.wav"
        flag = True
        attempts = 0
        attempts2 = 0

        while flag:
            result = self.synthesizer.speak_text_async(text).get()

            if result.reason == ResultReason.SynthesizingAudioCompleted:
                flag = False
                attempts = 0

                stream = AudioDataStream(result)
                stream.save_to_wav_file_async(fileName)
            else:
                attempts += 1

                print(f"\nCanceled: {result.cancellation_details.reason}", end="")
                if result.cancellation_details.reason == CancellationReason.Error:
                    error_details = result.cancellation_details.error_details
                    print(f"\rError details: {error_details}")
                    if error_details.find("1007") > 0:
                        attempts = 0
                        attempts2 += 1
                        self.SetConfig(attempts2)
                
                if attempts == 5:
                    print("\nExhausted 5 attempts")
                    # sys.exit()
                    attempts = 0
                    time.sleep(60)


    def ConcatWav(self, resultFileName):
        outfile = f"result/{resultFileName}.wav"

        data= []
        countWav = 0
        while True:
            tPath = f"temp/speech{countWav}.wav"
            countWav += 1
            if os.path.isfile(tPath): 
                w = wave.open(self.path + tPath, 'rb')
                data.append( [w.getparams(), w.readframes(w.getnframes())] )
                w.close()
            else:
                break
            
        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()

    def ClearAll(self):
        countWav = 0
        while True:
            tPath = f"temp/speech{countWav}.wav"
            countWav += 1
            if os.path.isfile(tPath): 
                os.remove(self.path + tPath)
            else:
                break


tts = TTS()

tts.path = "C:/projects/experements/tts-test/"

tts.cfg = [
    ["9904e7dce94e426e8ef02d5f040c28fe","northeurope"],
    ["3f6cbd2d66f64b6f966d8e05e5049202","westeurope"],
    ["62cae38d254f422a9532b1c9a96f6e38","switzerlandnorth"],
    ["b22febe5b0514088805e9678c10c82cc","francecentral"]
]

tts.Start(int(sys.argv[1]), 10)
# tts.Start(1395, 5)