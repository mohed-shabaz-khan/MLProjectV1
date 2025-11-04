import re, json
from pathlib import Path


def extract_dates(text):
    pattern = r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)"
    return re.findall(pattern, text)


def run(input_path='data/raw', output_path='data/processed'):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in input_path.glob('*.txt'):
        text = p.read_text()
        dates = extract_dates(text)
        rows.append({'file': p.name, 'text': text, 'dates': dates})
    out_file = output_path / 'processed.json'
    out_file.write_text(json.dumps(rows, indent=2))
    print(f"✅ Processed {len(rows)} files and saved to {out_file}")


if __name__ == '__main__':
    run()