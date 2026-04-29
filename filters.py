import cv2
import numpy as np


def apply_blur(img: np.ndarray, ksize: int) -> np.ndarray:
    """Gaussian blur. ksize must be odd (1 = no blur)."""
    if ksize <= 1:
        return img
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(img, (ksize, ksize), 0)


def apply_sharpness(img: np.ndarray, alpha: float) -> np.ndarray:
    """Unsharp mask sharpening. alpha=0 = no change, alpha=3 = very sharp."""
    if alpha == 0.0:
        return img
    blurred = cv2.GaussianBlur(img, (0, 0), 3)
    return cv2.addWeighted(img, 1.0 + alpha, blurred, -alpha, 0)


def apply_brightness_contrast(img: np.ndarray,
                               brightness: int,
                               contrast: float) -> np.ndarray:
    """Brightness shifts pixels up/down. Contrast scales pixel values."""
    return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)


def apply_grayscale(img: np.ndarray) -> np.ndarray:
    """Convert to black & white, keep 3 channels so pipeline works."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_edge_detection(img: np.ndarray,
                          thresh1: int = 100,
                          thresh2: int = 200) -> np.ndarray:
    """Canny edge detection — white edges on black background."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, thresh1, thresh2)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def apply_all_filters(img: np.ndarray,
                      blur: int,
                      sharpness: float,
                      brightness: int,
                      contrast: float,
                      grayscale: bool,
                      edge_detect: bool) -> np.ndarray:
    """Stack all filters in sequence on the image."""
    result = img.copy()
    result = apply_blur(result, blur)
    result = apply_sharpness(result, sharpness)
    result = apply_brightness_contrast(result, brightness, contrast)
    if grayscale:
        result = apply_grayscale(result)
    if edge_detect:
        result = apply_edge_detection(result)
    return result