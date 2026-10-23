
import streamlit as st
import subprocess
import os

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Text Compression System",
    page_icon="📦",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
    color: #1e293b;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label {
    color: #1e293b;
}

.hero {
    background: linear-gradient(120deg, #142b4a, #2463a6);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 32px;
    margin-bottom: 8px;
}

.hero p {
    color: #e2eafa !important;
    font-size: 16px;
    margin-bottom: 0;
}

.nav-link {
    display: block;
    text-align: center;
    padding: 16px 10px;
    border-radius: 10px;
    background: #245fa6;
    border: 1px solid #245fa6;
    color: #ffffff !important;
    font-size: 17px;
    font-weight: 600;
    text-decoration: none !important;
    transition: 0.2s;
}

.nav-link:hover {
    background: #174777;
    border-color: #174777;
    color: #ffffff !important;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #142b4a !important;
    margin-top: 10px;
    margin-bottom: 8px;
}

.section-description {
    color: #475569 !important;
    font-size: 16px;
    margin-bottom: 18px;
}


/* Fix normal buttons */
div.stButton > button,
div.stButton > button p {
    background-color: #245fa6 !important;
    color: #ffffff !important;
    border: 1px solid #245fa6 !important;
    border-radius: 9px !important;
    min-height: 45px;
    font-weight: 600 !important;
}

/* Button hover */
div.stButton > button:hover,
div.stButton > button:hover p {
    background-color: #174777 !important;
    color: #ffffff !important;
    border-color: #174777 !important;
}

/* Fix download buttons */
div[data-testid="stDownloadButton"] > button,
div[data-testid="stDownloadButton"] > button p {
    background-color: #245fa6 !important;
    color: #ffffff !important;
    border: 1px solid #245fa6 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 45px;
}

/* Download button hover */
div[data-testid="stDownloadButton"] > button:hover,
div[data-testid="stDownloadButton"] > button:hover p {
    background-color: #174777 !important;
    color: #ffffff !important;
    border-color: #174777 !important;
}


[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 16px;
    border: 1px solid #dbe4f0;
    border-radius: 12px;
}

[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border-radius: 10px;
}

[data-testid="stFileUploader"] section {
    background-color: #ffffff;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small {
    color: #334155 !important;
}

[data-testid="stFileUploader"] button {
    color: #ffffff !important;
    background-color: #245fa6 !important;
    border: none !important;
}

.stTextArea label {
    color: #334155 !important;
}

.stTextArea textarea {
    background-color: #ffffff;
    color: #1e293b;
}

.stCaption {
    color: #475569 !important;
}

hr {
    border-color: #dbe4f0;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>📦 Text Compression System</h1>
    <p>
        Compress your text files and restore them whenever you need.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION LINKS ----------------
# Both links remain visible on the page.

st.markdown("""
<div style="display:flex; gap:16px; margin-bottom:28px;">
    <a class="nav-link" href="#compress-section" style="flex:1;">
        🗜️ Compress File
    </a>
    <a class="nav-link" href="#decompress-section" style="flex:1;">
        📂 Decompress File
    </a>
</div>
""", unsafe_allow_html=True)


# ---------------- C++ COMPILATION ----------------

def compile_cpp():
    return subprocess.run(
        ["g++", "compression.cpp", "-o", "compress"],
        capture_output=True,
        text=True
    )


# ---------------- SESSION STATE ----------------

if "compression_data" not in st.session_state:
    st.session_state.compression_data = None

if "compression_info" not in st.session_state:
    st.session_state.compression_info = None

if "restored_data" not in st.session_state:
    st.session_state.restored_data = None


# ==================================================
#                    COMPRESS FILE
# ==================================================

st.markdown(
    '<div id="compress-section"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">🗜️ Compress File</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select a text file to compress.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a text file (.txt)",
    type=["txt"],
    key="text_upload"
)

if uploaded_file is not None:

    original_data = uploaded_file.getvalue()

    st.success(f"Selected file: {uploaded_file.name}")

    st.caption(
        f"Original file size: {len(original_data):,} bytes"
    )

    with st.expander("Preview original text"):
        st.text_area(
            "File contents",
            value=original_data.decode(
                "utf-8", errors="replace"
            ),
            height=150,
            disabled=True,
            key="original_preview"
        )

    if st.button(
        "🚀 Compress File",
        key="compress_button",
        use_container_width=True
    ):

        os.makedirs("test_files", exist_ok=True)

        with open("test_files/sample.txt", "wb") as file:
            file.write(original_data)

        with st.spinner("Compressing your file..."):

            compile_result = compile_cpp()

            if compile_result.returncode != 0:

                st.error("C++ compilation failed.")
                st.code(compile_result.stderr)

            else:

                result = subprocess.run(
                    ["./compress"],
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:

                    st.error("Compression failed.")
                    st.code(result.stderr)

                elif not os.path.exists("compressed.huff"):

                    st.error(
                        "The compressed file was not created."
                    )

                else:

                    with open("compressed.huff", "rb") as file:
                        compressed_data = file.read()

                    st.session_state.compression_data = (
                        compressed_data
                    )

                    st.session_state.compression_info = {
                        "original_size": len(original_data),
                        "compressed_size": len(compressed_data)
                    }

                    st.success(
                        "Your file was compressed successfully!"
                    )


# ---------------- COMPRESSION RESULTS ----------------

if st.session_state.compression_data is not None:

    compressed_data = st.session_state.compression_data
    info = st.session_state.compression_info

    st.divider()
    st.subheader("📊 Compression Results")

    original_size = info["original_size"]
    compressed_size = info["compressed_size"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original Size",
        f"{original_size:,} bytes"
    )

    col2.metric(
        "Compressed Size",
        f"{compressed_size:,} bytes"
    )

    if original_size > 0:

        reduction = (
            1 - compressed_size / original_size
        ) * 100

        col3.metric(
            "Size Reduction",
            f"{reduction:.2f}%"
        )

    else:
        col3.metric("Size Reduction", "N/A")

    if compressed_size < original_size:

        st.success(
            "The compressed file is smaller than the original."
        )

    elif compressed_size > original_size:

        st.info(
            "The compressed file is larger. Small files can grow "
            "because the compressed file includes metadata."
        )

    else:

        st.info("Both files have the same size.")

    st.download_button(
        "⬇️ Download Compressed File",
        data=compressed_data,
        file_name="compressed.huff",
        mime="application/octet-stream",
        key="download_compressed",
        use_container_width=True
    )


# ==================================================
#                   DECOMPRESS FILE
# ==================================================

st.divider()

st.markdown(
    '<div id="decompress-section"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">📂 Decompress File</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select a previously compressed .huff file to restore it.'
    '</div>',
    unsafe_allow_html=True
)

compressed_upload = st.file_uploader(
    "Choose a compressed file (.huff)",
    type=["huff"],
    key="huff_upload"
)

if compressed_upload is not None:

    compressed_input_data = compressed_upload.getvalue()

    st.success("Compressed file selected.")

    st.caption(
        f"Compressed file size: "
        f"{len(compressed_input_data):,} bytes"
    )

    if st.button(
        "🔄 Decompress File",
        key="decompress_button",
        use_container_width=True
    ):

        with open("compressed.huff", "wb") as file:
            file.write(compressed_input_data)

        with st.spinner("Restoring your original file..."):

            compile_result = compile_cpp()

            if compile_result.returncode != 0:

                st.error("C++ compilation failed.")
                st.code(compile_result.stderr)

            else:

                result = subprocess.run(
                    ["./compress", "decompress"],
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:

                    st.error("Decompression failed.")
                    st.code(result.stderr)

                elif not os.path.exists("decompressed.txt"):

                    st.error(
                        "The restored file was not created."
                    )

                else:

                    with open("decompressed.txt", "rb") as file:
                        restored_data = file.read()

                    st.session_state.restored_data = restored_data

                    st.success(
                        "Your file was restored successfully!"
                    )


# ---------------- RESTORED FILE RESULTS ----------------

if st.session_state.restored_data is not None:

    restored_data = st.session_state.restored_data

    st.divider()
    st.subheader("✅ Restored File")

    st.metric(
        "Restored Size",
        f"{len(restored_data):,} bytes"
    )

    with st.expander("Preview restored text"):

        st.text_area(
            "Restored contents",
            value=restored_data.decode(
                "utf-8", errors="replace"
            ),
            height=150,
            disabled=True,
            key="restored_preview"
        )

    st.download_button(
        "⬇️ Download Restored Text File",
        data=restored_data,
        file_name="decompressed.txt",
        mime="text/plain",
        key="download_restored",
        use_container_width=True
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption("Text Compression System | DAA Mini Project")
