import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# ---------------------------
# Load colors dataset
# ---------------------------
@st.cache_data
def load_colors():
    df = pd.read_csv("colors.csv")
    if list(df.columns) != ['color', 'color_name', 'hex', 'R', 'G', 'B']:
        df = pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=0)
    return df

df_colors = load_colors()

# ---------------------------
# Function to get closest color name
# ---------------------------
def get_color_name(R, G, B, df_colors):
    R, G, B = int(R), int(G), int(B)
    min_dist = float('inf')
    cname = None
    for _, row in df_colors.iterrows():
        try:
            r_val, g_val, b_val = int(row["R"]), int(row["G"]), int(row["B"])
            d = abs(R - r_val) + abs(G - g_val) + abs(B - b_val)
            if d < min_dist:
                min_dist = d
                cname = row["color_name"]
        except:
            continue
    return cname

# ---------------------------
# Streamlit App
# ---------------------------
st.title("🎨 Color Detection App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    st.write("Input pixel coordinates (X, Y) to detect color:")

    # Convert image to RGB
    img_rgb = img.convert("RGB")
    pixels = img_rgb.load()
    
    # Input pixel coordinates
    x = st.number_input("X-coordinate", min_value=0, max_value=img.width-1, value=50)
    y = st.number_input("Y-coordinate", min_value=0, max_value=img.height-1, value=50)
    
    if st.button("Detect Color"):
        r, g, b = pixels[x, y]
        rgb_text = f"RGB: ({r}, {g}, {b})"
        hex_text = f"HEX: #{r:02x}{g:02x}{b:02x}"
        cname = get_color_name(r, g, b, df_colors)
        
        st.write(f"**Closest Color Name:** {cname}")
        st.write(rgb_text)
        st.write(hex_text)
        
        # Show color box
        color_box = np.zeros((100, 100, 3), dtype=np.uint8)
        color_box[:, :] = [r, g, b]
        st.image(color_box, caption="Color Reference", width=100)
