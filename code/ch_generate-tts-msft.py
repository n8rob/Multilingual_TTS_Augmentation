# Install Azure SDK -> pip install azure-cognitiveservices-speech
import os
import time
from random import seed, randint, choices

from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

'''
This file can be used to generate speech from Microsoft TTS.
Start by setting up a python environment for Azure TTS. 
Microsoft TTS API Docs: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python
We will use the generating German synthetic speech as an example.
'''

prompts_file = open("microsoft-tts-prompts", "r")  # the file containing your prompts
prompts_list = [line.strip() for line in prompts_file.readlines()]

numbers_to_redo = [int(line.strip()) for line in open("de-CH-regenerate-numbers").readlines()]

speech_config = SpeechConfig(subscription="645a3342cd5c40b79b720c055573e550", region="eastus")

# Define the voices you want to use. In our case Kiswahili has two dialects and each dialect has 2 voices.
# language support list source = https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support
lang_voice = {
    "de-AT": {"voices": ["de-AT-JonasNeural", "de-AT-IngridNeural"], "configs": []},
    "de-DE": {"voices": ["de-DE-AmalaNeural", "de-DE-BerndNeural", "de-DE-ChristophNeural", "de-DE-ElkeNeural",
                         "de-DE-KasperNeural", "de-DE-KatjaNeural",
                         "de-DE-ConradNeural", "de-DE-ElkeNeural", "de-DE-GiselaNeural", "de-DE-KillianNeural",
                         "de-DE-KlarissaNeural", "de-DE-KlausNeural", "de-DE-LouisaNeural", "de-DE-MajaNeural",
                         "de-DE-RalfNeural", "de-DE-TanjaNeural",
                         ], "configs": []}
}
for lang in lang_voice:
    for voice in lang_voice[lang]['voices']:
        lang_speech_config = SpeechConfig(subscription="6116becea404442bbad269e105997374", region="eastus")
        lang_speech_config.speech_synthesis_language = lang  # e.g. "de-DE"
        lang_speech_config.speech_synthesis_voice_name = voice
        lang_voice[lang]['configs'].append(lang_speech_config)

# audio_config = AudioOutputConfig(use_default_speaker=True)  # uncomment to hear on your speaker.Don't to save in a file
# To store audio in a file called file.wav use the config below. Don't uncomment if you want custom names
# audio_config = AudioOutputConfig( filename="file.wav")

seed(1)
n_langs = len(lang_voice)
langs = list(lang_voice.keys())

# This file will list the mapping of the audio file and the corresponding voice that was used
voice_no_f = open("de-ch-msft-voice-number_map.csv", "a+")

directory = "gutenberg/"  # Folder to save your audio
if not os.path.exists(directory):
    os.makedirs(directory)
lang_options = langs
lang_no_voices = {}
for lang in langs:
    lang_no_voices[lang] = len(lang_voice[lang]["voices"])

weights = [0.2, 0.8]
for k in range(len(numbers_to_redo)):
    i = numbers_to_redo[k]
    lang = choices(lang_options, weights)[0]  # randomly choose a dialect
    voice_idx = randint(0, lang_no_voices[lang] - 1)  # randomly choose a voice
    config = lang_voice[lang]["configs"][voice_idx]
    voice = lang_voice[lang]["voices"][voice_idx]
    no = str(i).zfill(5)
    filename = "de_" + no
    audio_config = AudioOutputConfig(filename=directory + filename + ".wav")
    synthesizer = SpeechSynthesizer(speech_config=config, audio_config=audio_config)
    synthesizer.speak_text_async(prompts_list[i])  # generate the audio
    time.sleep(1)  # wait - there might be delays and to avoid being blocked.
    voice_no_f.write(no + ", " + voice + "\n")
voice_no_f.close()

print("Finished the generation loop !")
