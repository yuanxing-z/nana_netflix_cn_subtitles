import pysubs2


def add_time_to_subtitles(file_path, output_file_path, time_to_add_ms):
    # Load the subtitles from the file
    subs = pysubs2.load(file_path, encoding="utf-8")

    # Add the specified amount of time to all timestamps
    for line in subs:
        line.start += time_to_add_ms
        line.end += time_to_add_ms

    # Save the modified subtitles to the output file
    subs.save(output_file_path, encoding="utf-8", format_='srt')


ep = 47

# Path to the SRT file
file_path = f'simplified_cn_srt/NANA.2006.DVDrip.EP{ep}.WMV9.AC3-CalChi.srt'
output_file_path = f'simplified_cn_srt/NANA.2006.DVDrip.EP{ep}.WMV9.AC3-CalChi.srt'

# Time to add in milliseconds (1139 ms)
time_to_add_ms = 962

# Call the function
add_time_to_subtitles(file_path, output_file_path, time_to_add_ms)

print("Time added and file saved!")
