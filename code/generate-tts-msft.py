from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from random import seed, randint
import os, time

'''
This file can be used to generate speech from Microsoft TTS.
Start by setting up a python environment for Azure TTS. 
Microsoft TTS API Docs: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python
We will use the generating Kiswahili synthetic speech as an example.
'''

prompts_file = open("microsoft-tts-prompts", "r")  # the file containing your prompts
prompts_list = [line.strip() for line in prompts_file.readlines()]

speech_config = SpeechConfig(subscription="6116becea404442bbad269e105997374", region="eastus")

# Define the voices you want to use. In our case Kiswahili has two dialects and each dialect has 2 voices.
# language support list source = https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support
lang_voice = {
    "sw-KE": {"voices": ["sw-KE-ZuriNeural", "sw-KE-RafikiNeural"], "configs": []},
    "sw-TZ": {"voices": ["sw-TZ-RehemaNeural", "sw-TZ-DaudiNeural"], "configs": []}
}
for lang in lang_voice:
    for voice in lang_voice[lang]['voices']:
        lang_speech_config = SpeechConfig(subscription="6116becea404442bbad269e105997374", region="eastus")
        lang_speech_config.speech_synthesis_language = lang  # e.g. "de-DE"
        lang_speech_config.speech_synthesis_voice_name = voice
        lang_voice[lang]['configs'].append(lang_speech_config)

# audio_config = AudioOutputConfig(use_default_speaker=True)  # uncomment to hear on your speaker
audio_config = AudioOutputConfig(
    filename="file.wav")  # the audio are going to be temporarily stored in a file called file.wav

seed(1)
n_langs = len(lang_voice)
langs = list(lang_voice.keys())

# This file will list the mapping of the audio file and the corresponding voice that was used
voice_no_f = open("sw-msft-voice-number_map.csv", "a+")

for i in range(len(prompts_list)):
    lang_idx = randint(0, n_langs - 1)  # randomly choose a dialect
    voice_idx = randint(0, 1)  # randomly choose a voice
    config = lang_voice[langs[lang_idx]]["configs"][voice_idx]
    voice = lang_voice[langs[lang_idx]]["voices"][voice_idx]
    synthesizer = SpeechSynthesizer(speech_config=config, audio_config=audio_config)
    synthesizer.speak_text_async(prompts_list[i])  # generate the audio
    time.sleep(1)  # wait - there might be delays due to network latency
    no = str(i).zfill(5)
    filename = "swa_" + no
    os.rename('file.wav', "swa-msft-tts/" + filename + ".wav")
    voice_no_f.write(no + ", " + voice + "\n")
voice_no_f.close()
