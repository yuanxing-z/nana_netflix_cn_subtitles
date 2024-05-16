import os
import pysubs2


def extend_subtitles_for_episode(episode_number, en_folder_path, cn_folder_path, output_folder_path):
    # Format the file names based on episode number
    jp_file_name = f'NANA.S01E{episode_number:02d}.WEBRip.Netflix.ja[cc].srt'
    cn_file_name = f'NANA.2006.DVDrip.EP{episode_number:02d}.WMV9.AC3-CalChi.srt'

    # Construct the full paths to the files
    jp_file_path = os.path.join(en_folder_path, jp_file_name)
    cn_file_path = os.path.join(cn_folder_path, cn_file_name)
    output_file_path = os.path.join(output_folder_path, cn_file_name)  # Save using Chinese filename format

    # Load the subtitle files
    jp_subs = pysubs2.load(jp_file_path, encoding="utf-8")
    chi_subs = pysubs2.load(cn_file_path, encoding="utf-8")

    # Extend the end time of Chinese subtitles if applicable
    for i, chi_sub in enumerate(chi_subs):
        next_chi_start = chi_subs[i + 1].start if i + 1 < len(chi_subs) else chi_sub.end + 10000  # Handle last subtitle

        # Find the next Japanese subtitle before the start of the next Chinese subtitle
        for jp_sub in jp_subs:
            if chi_sub.end < jp_sub.start < next_chi_start:
                chi_sub.end = jp_sub.end  # Extend the end time to the end of this Japanese subtitle

    # Save the adjusted Chinese subtitles
    chi_subs.save(output_file_path, encoding="utf-8", format='srt')


def process_all_episodes(start_ep, end_ep, en_folder_path, cn_folder_path, output_folder_path):
    for episode_number in range(start_ep, end_ep + 1):
        extend_subtitles_for_episode(episode_number, en_folder_path, cn_folder_path, output_folder_path)
        print(f"Processed episode {episode_number}")


# Specify the folders and range of episodes
en_folder_path = 'nf_downloaded_srt_jp'
cn_folder_path = 'aligned_jp'
output_folder_path = 'aligned_jp_extend'

# Example: Process episodes from 11 to 47
process_all_episodes(11, 47, en_folder_path, cn_folder_path, output_folder_path)
