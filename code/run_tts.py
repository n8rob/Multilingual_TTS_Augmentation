import os
import azure.cognitiveservices.speech as speechsdk


def create_wav(text, speech_key, speech_region, voice_name, wav_file, verbose=True):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=wav_file)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=voice_name

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if verbose:
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

def check_zero_byte_audio_files(directory_path):
    zero_byte_files = []
    numbers = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory_path, filename)
            if os.path.getsize(file_path) == 0:
                zero_byte_files.append(filename)
                numbers.append(int(filename.split("_")[1].split(".")[0]))
    return zero_byte_files, numbers

