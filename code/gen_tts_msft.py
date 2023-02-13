import argparse
import json
import os
import random
import time

from run_tts import *

MAX_ITERS = 10

# create_wav(text, speech_key, speech_region, voice_name, wav_file, verbose=True)

def gen_tts(args):
    """
    args:
        seed (int)
        config_dict (str)
        prompts_file (str)
        wav_dir (str)
        lang (str)
        speech_key (str)
        speech_region (str)
        out_csv (str)
    """
    # Make dirs --------------------------------------------------------
    if not os.path.exists(args.wav_dir):
        os.makedirs(args.wav_dir)
    # Set seed ---------------------------------------------------------
    random.seed(args.seed)
    # Retrieve voices list ---------------------------------------------
    with open(args.config_dict, 'r') as f:
        config_dict = json.load(f)
    try:
        voices = config_dict[args.lang]
    except KeyError:
        print("WARNING: You may want to add an entry for "\
                f"{args.lang} to the config file {args.config_dict}")
        raise
    # Read prompts -----------------------------------------------------
    with open(args.prompts_file, 'r') as f:
        prompts = f.readlines()
    prompts = [p.strip() for p in prompts]
    # Cycle through prompts --------------------------------------------
    no2voice = {}
    indices = list(range(len(prompts)))
    for I in range(MAX_ITERS):
        print(f"~-~-~-~ {I} -~-~-~-", flush=True)
        print(f"Zero-byte files left: {len(indices)}")
        for i in indices:
            prompt = prompts[i]
            no = str(i).zfill(5)
            wav_file = os.path.join(args.wav_dir, f"{args.lang}-{no}.wav")
            voice_name = random.choice(voices)
            create_wav(text=prompt, speech_key=args.speech_key,\
                    speech_region=args.speech_region, voice_name=voice_name,\
                    wav_file=wav_file, verbose=False)
            sleep_time = round(1.5 ** I)
            time.sleep(sleep_time)
            no2voice[no] = voice_name
            print(i, end=' ', flush=True)
        print()
        indices = check_zero_byte_audio_files(args.wav_dir)
    # Print number voice matches to out csv file -----------------------
    with open(args.out_csv, 'w') as f:
        for no in no2voice:
            f.write(f"{no}, {no2voice[no]}\n")
    return


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("--seed", type=int, default=sum(b'lti'))
    parser.add_argument("--config-dict", type=str, required=True,\
            help="JSON file of dictionary mapping langs to voices")
    parser.add_argument("--prompts-file", type=str, required=True,\
            help="Text file containing all prompts")
    parser.add_argument("--wav-dir", type=str, required=True,\
            help="Dir to write wav files to")
    parser.add_argument("--lang", type=str, required=True,\
            help="Language code in Azure format")
    parser.add_argument("--speech-key", type=str,\
            default="780dfc2fdaea4bf89a0de176b65467e1",\
            help="Key for Azure use")
    parser.add_argument("--speech-region", type=str, default="eastus",
            help="Speech region for Azure use")
    parser.add_argument("--out-csv", type=str, required=True,\
            help="CSV file to write file-to-voice mappings to")

    args = parser.parse_args()

    gen_tts(args)

    """
    python3 gen-tts-msft.py --config-dict azure-voices.json --prompts-file tts-prompts/arctic/arctic-kor-lines.txt --wav-dir tts-audio/kor/ --lang ko-KR --out-csv voice_csvs/kor-msft.csv
    """
