import os
from utils import (
    extract_arabic_sentences,
    preprocessing,
    not_needed,
    write_lines_to_csv,
    read_file_content,
)

chats_dir = "./Chats"


def extract_to_one_file(base_dir):
    all_lines = []
    for file_path in os.listdir(chats_dir):
        text = read_file_content(f"{chats_dir}/{file_path}")
        arabic_sentences = extract_arabic_sentences(text, preprocessing, not_needed)
        for line in arabic_sentences:
            all_lines.append(line)

    write_lines_to_csv(f"{base_dir}/all-processed-chats.csv", all_lines)


def extract_to_multi_files(base_dir):
    for file_path in os.listdir(chats_dir):
        text = read_file_content(f"{chats_dir}/{file_path}")
        arabic_sentences = extract_arabic_sentences(text, preprocessing, not_needed)
        write_lines_to_csv(
            f"{base_dir}/{file_path[:-5]}-processed.csv", arabic_sentences
        )


if __name__ == "__main__":
    # extract_to_multi_files("data/processed")
    extract_to_one_file("data")
