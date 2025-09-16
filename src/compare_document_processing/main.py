import difflib
import tempfile
import time
from io import BytesIO
from pathlib import Path

import streamlit as st
from docling.datamodel.base_models import DocumentStream
from docling.document_converter import DocumentConverter
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from st_diff_viewer import diff_viewer


@st.cache
def load_marker_models() -> dict:
    """Load Marker models"""
    return create_model_dict()

def extract_with_marker(pdf_bytes: bytes):
    """Extract text from PDF using Marker"""

    try:
        # Save bytes to temporary file since Marker needs a file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file_path = tmp_file.name

        # Initialize Marker converter
        converter = PdfConverter(
            artifact_dict=load_marker_models(),
        )

        # Time the conversion
        start_time = time.time()
        rendered = converter(tmp_file_path)
        text, _, images = text_from_rendered(rendered)
        end_time = time.time()

        # Clean up temp file
        Path(tmp_file_path).unlink()

        processing_time = end_time - start_time

        return text, processing_time, None

    except Exception as e:
        return None, None, str(e)


def extract_with_docling(pdf_bytes: bytes, filename: str):
    """Extract text from PDF using Docling"""

    try:
        # Create DocumentStream from bytes
        buf = BytesIO(pdf_bytes)
        source = DocumentStream(name=filename, stream=buf)

        # Initialize Docling converter
        converter = DocumentConverter()

        # Time the conversion
        start_time = time.time()
        result = converter.convert(source)
        markdown_text = result.document.export_to_markdown()
        end_time = time.time()

        processing_time = end_time - start_time

        
        return markdown_text, processing_time, None

    except Exception as e:
        return None, None, str(e)


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two texts"""
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def main() -> None:
    """
    Main function for the application, providing an interface for comparing PDF-to-Markdown
    extraction performance between the Marker library and the Docling library. The function
    is executed in a Streamlit environment and utilizes its widgets and layout.

    This function handles file uploads, extraction using the two libraries, and displays
    various processing metrics, outputs, and comparisons to the user in an accessible format.

    :raises ValueError: If invalid or unsupported inputs are provided during processing.
    """
    st.set_page_config(
        page_title="PDF Extraction Comparison: Marker vs Docling",
        page_icon="📄",
        layout="wide"
    )

    st.title("📄 PDF Extraction Comparison: Marker vs Docling")
    st.markdown("Compare PDF-to-Markdown extraction performance between Marker and Docling libraries")

    # File upload
    st.header("📤 Upload PDF Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a PDF document to compare extraction performance"
    )

    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        pdf_bytes = uploaded_file.read()

        # Process with both libraries
        st.header("🔄 Processing...")

        # Create columns for parallel processing display
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏷️ Marker Processing")
            marker_placeholder = st.empty()

        with col2:
            st.subheader("📋 Docling Processing")
            docling_placeholder = st.empty()

        # Process with Marker
        with marker_placeholder.container():
            with st.spinner("Processing with Marker..."):
                marker_text, marker_time, marker_error = extract_with_marker(pdf_bytes)

        # Process with Docling
        with docling_placeholder.container():
            with st.spinner("Processing with Docling..."):
                docling_text, docling_time, docling_error = extract_with_docling(pdf_bytes, uploaded_file.name)

        # Display results
        st.header("📊 Results")

        # Performance metrics
        if marker_time is not None and docling_time is not None:
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

            with metrics_col1:
                st.metric(
                    "Marker Processing Time",
                    f"{marker_time:.2f}s"
                )

            with metrics_col2:
                st.metric(
                    "Docling Processing Time",
                    f"{docling_time:.2f}s"
                )

            with metrics_col3:
                speed_diff = ((marker_time - docling_time) / docling_time) * 100
                faster_library = "Docling" if marker_time > docling_time else "Marker"
                st.metric(
                    f"{faster_library} is faster by",
                    f"{abs(speed_diff):.1f}%"
                )

        # Text comparison
        if marker_text is not None and docling_text is not None:
            # Calculate similarity
            similarity = calculate_similarity(marker_text, docling_text)
            st.subheader(f"📝 Text Similarity: {similarity:.1%}")

            # Length comparison
            len_col1, len_col2 = st.columns(2)
            with len_col1:
                st.info(f"Marker output: {len(marker_text)} characters")
            with len_col2:
                st.info(f"Docling output: {len(docling_text)} characters")

            # Side-by-side comparison
            st.subheader("📄 Markdown Output Comparison")

            tab1, tab2, tab3 = st.tabs(["Marker Output", "Docling Output", "Diff View"])

            with tab1:
                st.markdown("### Marker Output")
                st.text_area(
                    "Marker Markdown",
                    marker_text,
                    height=800,
                    key="marker_output"
                )

            with tab2:
                st.markdown("### Docling Output")
                st.text_area(
                    "Docling Markdown",
                    docling_text,
                    height=800,
                    key="docling_output"
                )

            with tab3:
                st.markdown("### Text Differences")
                try:
                    diff_viewer(
                        old_text=marker_text,
                        new_text=docling_text,
                        left_title="Marker",
                        right_title="Docling",
                    )
                except ImportError as e:
                    st.error(f"streamlit-diff-viewer not available: {e}")

        # Error handling
        if marker_error:
            st.error(f"Marker Error: {marker_error}")

        if docling_error:
            st.error(f"Docling Error: {docling_error}")

    else:
        st.info("👆 Please upload a PDF file to begin comparison")


if __name__ == "__main__":
    main()
