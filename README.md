# PDF Extraction Comparison: Marker vs Docling

A Streamlit web application that compares PDF-to-Markdown extraction performance between two popular Python libraries: **Marker** and **Docling**.

## 🏗️ Architecture

### Libraries Compared

1. **Marker** ([vikparuchuri/marker](https://github.com/vikparuchuri/marker))
   - Fast and accurate document conversion
   - Supports PDF, images, PPTX, DOCX, XLSX, HTML, EPUB
   - Preserves formatting, tables, equations, and code blocks
   - Uses AI models for enhanced accuracy

2. **Docling** ([docling-project/docling](https://github.com/docling-project/docling))
   - Advanced PDF understanding capabilities
   - Seamless integration with generative AI ecosystem
   - Supports various document formats
   - Optimized for RAG and agentic AI applications

### Application Structure

```
main.py
├── extract_with_marker()     # Marker processing pipeline
├── extract_with_docling()    # Docling processing pipeline
├── calculate_similarity()    # Similarity ratio calculation
└── main()                   # Streamlit UI and orchestration
```

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- uv package manager (recommended) or pip

### Setup

1. **Clone the project directory:**
   ```bash
   git clone https://github.com/ysif9/compare-document-processing
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   ```
3. **Download marker independently (recommended)**
   ```bash
   uv run src/compare_document_processing/marker_test_and_download.py
   ```

## 🎯 Usage

1. **Start the Streamlit application:**
   ```bash
   streamlit run src/compare_document_processing/main.py
   ```

2. **Open your web browser** and navigate to the displayed URL (typically `http://localhost:8501`)

3. **Upload a PDF file** using the file uploader interface

4. **Wait for processing** to complete - you'll see real-time progress indicators

5. **Review the results:**
   - **Performance Metrics**: Processing times and speed comparison
   - **Text Similarity**: Percentage similarity between outputs
   - **Output Comparison**: Side-by-side markdown content in tabs
   - **Diff View**: Unified diff showing exact differences

## 📊 Output Metrics

The application provides several comparison metrics:

- **Processing Time**: Execution time for each library in seconds
- **Speed Difference**: Percentage difference showing which library is faster
- **Text Similarity**: Similarity ratio between the two markdown outputs
- **Character Count**: Total characters in each extracted text
- **Split Diff**: Line-by-line differences between outputs