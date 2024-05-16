import os
import pysubs2


def align_subtitles_for_episode(episode_number, en_folder_path, cn_folder_path, output_folder_path):
    # Format the file names based on episode number
    en_file_name = f'NANA.S01E{episode_number:02d}.WEBRip.Netflix.ja[cc].srt'
    cn_file_name = f'NANA.2006.DVDrip.EP{episode_number:02d}.WMV9.AC3-CalChi.srt'

    # Construct the full paths to the files
    en_file_path = os.path.join(en_folder_path, en_file_name)
    cn_file_path = os.path.join(cn_folder_path, cn_file_name)
    output_file_path = os.path.join(output_folder_path, cn_file_name)  # Save using English filename format

    # Load the subtitle files
    eng_subs = pysubs2.load(en_file_path, encoding="utf-8")
    chi_subs = pysubs2.load(cn_file_path, encoding="utf-8")

    # Create a new subtitle file
    output_subs = pysubs2.SSAFile()

    # Prepare a dictionary to append Chinese subtitles to the closest English timestamps
    eng_to_chi_mapping = {i: [] for i in range(len(eng_subs))}

    # Map each Chinese subtitle to the closest English timestamp within 3000 ms tolerance
    for chi_sub in chi_subs:
        closest_eng_index = None
        min_distance = float('inf')

        for i, eng_sub in enumerate(eng_subs):
            time_difference = abs(eng_sub.start - chi_sub.start)
            if time_difference < min_distance:
                min_distance = time_difference
                closest_eng_index = i

        # Only add the text if it's within the 3000 ms tolerance
        if min_distance <= 3000:
            eng_to_chi_mapping[closest_eng_index].append(chi_sub.text)

    # Generate the final subtitles by combining mapped Chinese subtitles with English timings
    for i, chi_texts in eng_to_chi_mapping.items():
        if chi_texts:  # Ensure there are Chinese texts to include
            combined_text = '\\N'.join(chi_texts)  # Join texts with newline character
            event = pysubs2.SSAEvent(start=eng_subs[i].start, end=eng_subs[i].end, text=combined_text)
            output_subs.append(event)

    # Save the aligned subtitles
    output_subs.save(output_file_path, encoding="utf-8", format_='srt')


def process_all_episodes(start_ep, end_ep, en_folder_path, cn_folder_path, output_folder_path):
    for episode_number in range(start_ep, end_ep + 1):
        align_subtitles_for_episode(episode_number, en_folder_path, cn_folder_path, output_folder_path)
        print(f"Processed episode {episode_number}")


# Specify the folders and range of episodes
en_folder_path = 'nf_downloaded_srt_jp'
cn_folder_path = 'simplified_cn_srt'
output_folder_path = 'aligned_jp'

process_all_episodes(11, 47, en_folder_path, cn_folder_path, output_folder_path)
