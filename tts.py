import os
import yaml
from pathlib import Path
from fish_audio_sdk import Session, TTSRequest
from tqdm import tqdm

session = Session(os.getenv("FISH_AUDIO_API_KEY"))

with open("config/tts.yml") as f:
    config = yaml.safe_load(f)


def next_file_number(path):
    files = Path(path).glob(f"{config['name']}_*.mp3")
    numbers = (int(p.stem.split("_")[-1]) for p in files)
    return max(numbers, default=0) + 1


for i in tqdm(range(config["iterations"]), desc="Generating audio"):
    name = config["name"]
    output_dir = f"outputs/{name}"
    next_num = next_file_number(output_dir)
    filepath = f"{output_dir}/{name}_{next_num}.mp3"

    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "wb") as f:
        for chunk in session.tts(
            TTSRequest(
                reference_id=config["reference_id"],
                text=config["text"],
                chunk_length=300,
            )
        ):
            f.write(chunk)
