import pypdf
import sys

def extract_text(pdf_path, output_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text extracted to {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    extract_text(sys.argv[1], sys.argv[2])
