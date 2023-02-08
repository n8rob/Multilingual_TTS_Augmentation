import os
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
common_voice_dir = "common_voice"
zero_byte_files, numbers = check_zero_byte_audio_files(common_voice_dir)
