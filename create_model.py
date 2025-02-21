import os
import sys
import yaml
from fish_audio_sdk import Session

if len(sys.argv) != 2:
    print("Usage: python script.py <config_name>")
    sys.exit(1)

config_name = sys.argv[1]
config_path = f"./config/models/{config_name}.yml"

session = Session(os.getenv("FISH_AUDIO_API_KEY"))

with open(config_path) as f:
    config = yaml.safe_load(f)

voices = []
texts = []
for sample in config["samples"]:
    with open(sample["voice"], "rb") as f:
        voices.append(f.read())
    texts.append(sample["text"])

print(f"Creating TTS model for {config["title"]}...")
model = session.create_model(
    title=config["title"],
    visibility="private",
    voices=voices,
    texts=texts,
)

print("Success! Model ID:", model.id)
