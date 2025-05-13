import io
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
import langid

def detect_language(image: Image.Image) -> str:
    # Load image and get dimensions
    width, height = image.size

    # Define middle crop (e.g., 30% tall, vertically centered)
    crop_height = int(height * 0.3)
    top = (height - crop_height) // 2
    middle_crop = image.crop((0, top, width, top + crop_height))

    # Convert cropped image to bytes
    with io.BytesIO() as buffer:
        image.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

    # Run OCR on cropped region
    model = ocr_predictor(pretrained=True)
    doc = DocumentFile.from_images([image_bytes])  # Pass as a list of bytes
    result = model(doc)

    # Extract first ~50 words
    words = []
    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    words.append(word.value)
                    if len(words) >= 50:
                        break
                if len(words) >= 50:
                    break
            if len(words) >= 50:
                break
        if len(words) >= 50:
            break

    lang_input = " ".join(words)

    # Detect language using langid
    lang, _ = langid.classify(lang_input)

    # Return the detected language
    return lang
