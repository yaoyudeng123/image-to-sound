# Image to Sound (Azure)

Convert text in an image to speech using **Microsoft Azure Cognitive Services**.

## Features
- OCR with Azure Computer Vision (Read API)
- Text-to-Speech with Azure Speech SDK
- Uses relative paths

## Run
```bash
pip install azure-cognitiveservices-vision-computervision azure-cognitiveservices-speech msrest
python app.py
```

Ensure `image.jpg` is in the same directory.

## Output
- `sound.mp3` generated in the project directory
