import csv
import re

TO_REMOVE = ["شكرا لتواصلكم معنا", "اهلا و مرحبا بكم"]
arabic_pattern = re.compile("[\u0600-\u06FF]+")


def _remove_datetime(line):
    return re.sub(r"\(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\) ", "", line)


def _remove_visitor_name(line):
    return re.sub(r"Visitor \d+: ", "", line)


def _remove_gemma(line):
    return re.sub(r"Gemma: ", "", line)


def _remove_one_words(line):
    if len(line.split()) <= 1:
        return True
    return False


def _remove_static_sent(line):
    for rem in TO_REMOVE:
        if line in rem:
            return True
    return False


def not_needed(line: str) -> bool:
    return _remove_one_words(line) or _remove_static_sent(line)


def preprocessing(line):
    return _remove_datetime(_remove_visitor_name(_remove_gemma(line)))


def extract_arabic_sentences(
        text, preprocessing=lambda line: line, not_needed=lambda line: False
):
    lines = text.split("\n")
    arabic_sentences = []
    for line in lines:
        if arabic_pattern.search(line):
            sender = "Gemma" if "Gemma" in line else "Visitor"
            line = preprocessing(line)
            if not not_needed(line):
                arabic_sentences.append((sender, line))
    return arabic_sentences


def write_lines_to_csv(file_path, lines):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sender", "sentences"])
        for line in lines:
            writer.writerow([*line])


def read_file_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
