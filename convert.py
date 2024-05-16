import os
import webvtt
import pysubs2


def convert_ass_to_srt(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # List all the files in the input directory
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".ass"):
            # Construct the full file path
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace(".ass", ".srt"))

            # Load the ASS file
            subs = pysubs2.load(input_file_path)

            # Convert and save as SRT
            subs.save(output_file_path, format_='srt')


def convert_vtt_to_srt(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Define a helper function to convert VTT time format to milliseconds
    def time_to_ms(time_str):
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        # Seconds and milliseconds are separated by a dot
        seconds, milliseconds = map(int, parts[2].split('.'))
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
        return total_ms

    # List all files in the input directory
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".ja[cc].vtt"):
            # Construct the full file path
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace(".vtt", ".srt"))

            # Read the VTT file using webvtt-py
            vtt = webvtt.read(input_file_path)

            # Create a new Subs2 object
            subs = pysubs2.SSAFile()

            # Convert each caption into a pysubs2 event
            for caption in vtt:
                start_time = time_to_ms(caption.start)
                end_time = time_to_ms(caption.end)
                text = caption.text.replace('\n', '\\N')  # pysubs2 uses '\\N' for new lines
                subs.append(pysubs2.SSAEvent(start=start_time, end=end_time, text=text))

            # Save the subtitles in SRT format
            subs.save(output_file_path, format_='srt')


# # Specify your input and output folders
# en_input_folder = 'simplified_cn'
# en_output_folder = 'simplified_cn_srt'
#
# convert_ass_to_srt(en_input_folder, en_output_folder)
# print("Ass Conversion complete!")

# Specify your input and output folders
input_folder = 'nf_downloaded'
output_folder = 'nf_downloaded_srt_jp'

convert_vtt_to_srt(input_folder, output_folder)

print("Vtt Conversion complete!")
