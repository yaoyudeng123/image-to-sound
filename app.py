from pathlib import Path
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from msrest.authentication import CognitiveServicesCredentials

VISION_KEY = "YOUR_VISION_KEY"
VISION_ENDPOINT = "YOUR_VISION_ENDPOINT"

SPEECH_KEY = "YOUR_SPEECH_KEY"
SPEECH_REGION = "YOUR_SPEECH_REGION"


def image_to_sound(image_path, output_audio_path):
    # ---------- OCR (Read API) ----------
    vision_client = ComputerVisionClient(
        VISION_ENDPOINT,
        CognitiveServicesCredentials(VISION_KEY)
    )

    with open(image_path, "rb") as image_stream:
        read_response = vision_client.read_in_stream(image_stream, raw=True)

    operation_location = read_response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    while True:
        result = vision_client.get_read_result(operation_id)
        if result.status.lower() not in ["notstarted", "running"]:
            break
        time.sleep(1)

    lines = []
    if result.status == "succeeded":
        for page in result.analyze_result.read_results:
            for line in page.lines:
                lines.append(line.text)

    text = " ".join(lines)
    print("OCR result:", text)

    if not text:
        print("No text detected")
        return

    # ---------- Text To Speech ----------
    speech_config = SpeechConfig(
        subscription=SPEECH_KEY,
        region=SPEECH_REGION
    )
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    audio_config = AudioConfig(filename=str(output_audio_path))
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    synthesizer.speak_text(text)
    print(f"Audio generated: {output_audio_path}")


if __name__ == "__main__":
    # ✅ 以脚本所在目录作为相对路径根
    BASE_DIR = Path(__file__).parent

    image_path = BASE_DIR / "image.jpg"
    audio_path = BASE_DIR / "sound.mp3"

    image_to_sound(image_path, audio_path)
