"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from google.cloud import speech

import csv
import random 
# from pydub import AudioSegment

# Instantiates a client
client = texttospeech.TextToSpeechClient()
text_path = 'gamayun4tts_3600.txt'

def synthesize_text(text, output_file, name, gender, output_dir):
    """Synthesizes speech from the input string of text."""
    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="it-IT",
        name=name,
        ssml_gender=gender,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MULAW
    )

    # audio_config = speech.RecognitionConfig(
    #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     sample_rate_hertz=16000,
    #     language_code="en-US",
    # )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_dir + "/" + output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file", output_file)


configurations = [
    ("it-IT-Standard-A", texttospeech.SsmlVoiceGender.FEMALE), 
    ("it-IT-Standard-B", texttospeech.SsmlVoiceGender.FEMALE),
    ("it-IT-Standard-C", texttospeech.SsmlVoiceGender.MALE), 
    ("it-IT-Standard-D", texttospeech.SsmlVoiceGender.MALE)]

filename = "gamayun4tts_3600"
csv_output_path = "italian_tts_full_mappings.csv"
fields = ["Sentence", "Audio file"]
rows = []
lines = []

# reading csv file
# with open(filename, 'r') as data_file:
    # creating a csv reader object
    # csvreader = csv.reader(data_file)
      
    # # extracting field names through first row
    # fields = next(csvreader)
  
    # # extracting each data row one by one
    # for row in csvreader:
    #     rows.append(row)

with open(filename + ".txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

for i, row in enumerate(lines):
    name, gender = configurations[random.randint(0, 3)]
    audio_file = filename + "_italian_" + str(i) + ".wav"
    rows.append([row, audio_file])
    synthesize_text(row, audio_file, name, gender, "italian")

# writing to csv file 
with open(csv_output_path, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)


