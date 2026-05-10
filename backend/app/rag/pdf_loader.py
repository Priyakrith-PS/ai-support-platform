import os
from PyPDF2 import PdfReader


def load_pdfs(folder_path):
    all_texts = []

    print("FILES:", os.listdir(folder_path))  # debug

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)
            print("Reading:", path)

            reader = PdfReader(path)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            print("Extracted length:", len(text))

            if text.strip():
                all_texts.append(text)

    return all_texts