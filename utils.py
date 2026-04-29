import io
import numpy as np
import cv2
from PIL import Image


def pil_to_cv2(pil_img: Image.Image) -> np.ndarray:
    """PIL (RGB) → NumPy BGR array for OpenCV."""
    rgb = np.array(pil_img.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image:
    """NumPy BGR array → PIL (RGB) image."""
    rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def cv2_to_bytes(cv2_img: np.ndarray) -> bytes:
    """NumPy BGR array → PNG bytes (for download button)."""
    pil_img = cv2_to_pil(cv2_img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    return buffer.getvalue()