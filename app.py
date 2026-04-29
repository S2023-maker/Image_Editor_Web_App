import streamlit as st
from PIL import Image
from filters import apply_all_filters
from utils import pil_to_cv2, cv2_to_pil, cv2_to_bytes

# ── Page config ────────────────────────────────────────────────
st.set_page_config(page_title="Image Editor", page_icon="🎨", layout="wide")
st.title("🎨 Image Editor")
st.markdown("Upload an image, tweak the filters on the left, and download your result.")

# ── Sidebar controls ───────────────────────────────────────────
st.sidebar.header("🛠️ Filter Controls")

blur = st.sidebar.slider(
    "🌫️ Blur",
    min_value=1, max_value=51,
    value=1, step=2,
    help="1 = no blur. Higher = more blurry."
)

sharpness = st.sidebar.slider(
    "✨ Sharpness",
    min_value=0.0, max_value=3.0,
    value=0.0, step=0.1,
    help="0 = no sharpening. 3 = very sharp."
)

brightness = st.sidebar.slider(
    "☀️ Brightness",
    min_value=-100, max_value=100,
    value=0,
    help="Negative = darker. Positive = brighter."
)

contrast = st.sidebar.slider(
    "🔆 Contrast",
    min_value=0.5, max_value=3.0,
    value=1.0, step=0.1,
    help="1.0 = no change."
)

grayscale   = st.sidebar.checkbox("⬛ Grayscale", value=False)
edge_detect = st.sidebar.checkbox("🔲 Edge Detection", value=False)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# ── File uploader ──────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📁 Upload an image",
    type=["jpg", "jpeg", "png"]
)

# ── Main content ───────────────────────────────────────────────
if uploaded_file is not None:

    pil_img = Image.open(uploaded_file)
    cv2_img = pil_to_cv2(pil_img)

    processed = apply_all_filters(
        img=cv2_img,
        blur=blur,
        sharpness=sharpness,
        brightness=brightness,
        contrast=contrast,
        grayscale=grayscale,
        edge_detect=edge_detect,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🖼️ Original")
        st.image(pil_img, use_container_width=True)
        st.caption(f"Size: {pil_img.width} × {pil_img.height} px")

    with col2:
        st.subheader("✅ Processed")
        st.image(cv2_to_pil(processed), use_container_width=True)
        st.caption(
            f"Blur={blur} | Sharp={sharpness} | "
            f"Bright={brightness} | Contrast={contrast} | "
            f"Gray={'On' if grayscale else 'Off'} | "
            f"Edges={'On' if edge_detect else 'Off'}"
        )

    st.markdown("---")

    st.download_button(
        label="⬇️ Download Processed Image (PNG)",
        data=cv2_to_bytes(processed),
        file_name="edited_image.png",
        mime="image/png"
    )

else:
    st.info("👆 Upload a JPG or PNG image above to get started!")

    with st.expander("📖 Filter Reference"):
        st.markdown("""
| Filter | Control | Effect |
|---|---|---|
| **Blur** | Slider 1–51 | Smooths noise using Gaussian kernel |
| **Sharpness** | Slider 0.0–3.0 | Enhances edges with unsharp mask |
| **Brightness** | Slider -100 to 100 | Shifts pixel intensity up/down |
| **Contrast** | Slider 0.5–3.0 | Scales pixel values around midpoint |
| **Grayscale** | Checkbox | Converts to black & white |
| **Edge Detection** | Checkbox | Highlights edges using Canny algorithm |
        """)