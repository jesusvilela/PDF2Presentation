# PDF2Presentation

Welcome to PDF2Presentation, a Python-based utility designed to transform your PDF files into fully-fledged PowerPoint presentations.

> :warning: **Alpha Version:** The project is currently in its alpha stage of development. As such, please note that certain features may not be fully stable or optimized. Your patience, feedback, and contributions are appreciated!

## Overview

PDF2Presentation uses a combination of sophisticated libraries such as `nltk`, `PyPDF2`, `fitz`, `openai`, `torch`, `re`, `pptx`, `diffusers`, `io`, `PIL`, and `os` to deliver a seamless experience of converting your PDF files into presentations. The tool not only extracts the text and images from your PDFs, but also leverages the power of OpenAI's GPT-3 model to generate section titles and summaries, further enriching your presentations.

## Why Use PDF2Presentation?

From a user's perspective, PDF2Presentation offers several advantages:

- **Saves Time**: Automatically converting a PDF into a presentation saves you hours of manual work.
- **Enhances Understanding**: Auto-generated summaries help highlight key points and improve the overall comprehension of the content.
- **Increases Aesthetics**: The tool intelligently generates a cover image and inserts images from the PDF, enhancing the visual appeal of your presentations.
- **Prepares Presenter Notes**: Auto-generated presenter notes can guide your speech and help maintain a smooth flow during your presentation.
  
## Installation

Ensure you have Python 3.6 or later installed. The necessary dependencies can be installed via pip:

```shell
pip install nltk PyPDF2 pymupdf openai torch python-pptx diffuser Pillow
```

## Usage

To use this script, simply run the main Python file:

```shell
python main.py
```

Please note that "document.pdf" in the `main()` function is a sample document. You'll need to replace it with the path of your desired PDF document. Also, remember to set your own OpenAI key as shown below:

```python
openai.api_key = "your_openai_key"
```

## Disclaimer

Since the code is in the alpha stage, there may be some bugs or issues that need to be resolved. Please feel free to report any problems you encounter, or better yet, contribute to improving the code!

## Contributions

We appreciate your interest in our project and welcome contributions. Feel free to open issues or pull requests to help improve PDF2Presentation.

Enjoy transforming your PDFs into impressive presentations!