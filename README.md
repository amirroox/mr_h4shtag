# mr_h4shtag

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub Issues](https://img.shields.io/github/issues/sharpnova/mr_h4shtag)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)

**mr_h4shtag** is a specialized command-line interface (CLI) tool designed for extracting, analyzing, and reporting hashtags from text-based inputs. Built with Python, it caters to social media analysts, digital marketers, data scientists, and developers who need to process hashtag data efficiently. The tool supports multiple input formats, advanced filtering, and structured outputs, making it a versatile solution for tasks such as trend analysis, content categorization, and data preprocessing for machine learning pipelines.

This README provides a comprehensive guide to **mr_h4shtag**, aligned with the repository's actual structure and functionality as of the latest commit. It is formatted for optimal rendering on GitHub and includes detailed instructions for setup, usage, and contribution.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Examples](#examples)
- [Input and Output Specifications](#input-and-output-specifications)
  - [Supported Input Formats](#supported-input-formats)
  - [Supported Output Formats](#supported-output-formats)
- [Advanced Features](#advanced-features)
- [Performance Optimization](#performance-optimization)
- [Testing](#testing)
- [Extending the Tool](#extending-the-tool)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Support](#support)
- [Roadmap](#roadmap)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
**mr_h4shtag** is a lightweight, open-source tool that extracts hashtags (e.g., `#example`) from text inputs, providing detailed statistical analysis and flexible output options. It is designed for integration into data analysis workflows, offering robust support for processing social media datasets, generating reports, and automating hashtag-based tasks. The tool is maintained in the [sharpnova/mr_h4shtag](https://github.com/sharpnova/mr_h4shtag) GitHub repository and is actively developed with community contributions.

Key use cases include:
- Identifying trending hashtags in social media posts.
- Analyzing hashtag frequency for marketing campaigns.
- Preprocessing text data for natural language processing (NLP).
- Categorizing content based on hashtag metadata.

## Key Features
- **Hashtag Extraction**: Accurately identifies hashtags using regular expressions, supporting Unicode for multilingual hashtags.
- **Statistical Insights**: Computes total hashtag count, unique hashtags, frequency distribution, and top-N hashtags.
- **Multi-Format Input**: Processes plain text (`.txt`), JSON (`.json`), CSV (`.csv`), and STDIN inputs.
- **Flexible Output**: Outputs to terminal, text files, or JSON for human-readable or machine-readable results.
- **Advanced Filtering**: Supports filters for hashtag length, frequency, case sensitivity, and custom regex patterns.
- **Memory Efficiency**: Stream-based processing for handling large datasets.
- **Modular Design**: Easy to extend with new parsers, filters, or output formats.
- **Robust Error Handling**: Comprehensive validation and logging for production use.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Repository Structure
The repository is organized for clarity and maintainability, reflecting the actual structure of [sharpnova/mr_h4shtag](https://github.com/sharpnova/mr_h4shtag):

```
mr_h4shtag/
├── src/                            # Source code
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # CLI entry point
│   ├── hashtag_parser.py           # Hashtag extraction and analysis
│   ├── output_handler.py           # Output formatting and writing
│   ├── input_validator.py          # Input validation
│   └── utils.py                    # Utility functions
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_parser.py              # Tests for hashtag parsing
│   ├── test_output.py              # Tests for output handling
│   ├── test_input.py               # Tests for input validation
│   └── test_utils.py               # Tests for utilities
├── examples/                       # Sample input files
│   ├── sample.txt                  # Plain text sample
│   ├── sample.json                 # JSON sample
│   ├── sample.csv                  # CSV sample
│   └── large_dataset.txt           # Stress testing dataset
├── docs/                           # Documentation
│   ├── api.md                      # API reference
│   ├── changelog.md                # Changelog
│   └── contributing.md             # Contribution guidelines
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
└── README.md                         # Setup script for packaging
```

### Core Modules
- **`main.py`**: Parses CLI arguments and orchestrates the workflow.
- **`hashtag_parser.py`**: Implements hashtag extraction using the regex `r'#[\w]+'` and analysis logic.
- **`output_handler.py`**: Formats and writes results to terminal or files.
- **`input_validator.py`**: Validates input formats and handles edge cases.
- **`utils.py`**: Provides shared functions for logging, file I/O, and string processing.

## Prerequisites
To use **mr_h4shtag**, ensure the following are installed:
- **Python**: Version 3.8 or higher (tested up to 3.11).
- **pip**: Python package manager (included with Python).
- **Dependencies** (listed in `requirements.txt`):
  - Standard libraries: `argparse`, `json`, `csv`, `re`, `logging`, `pathlib`.
  - Optional: `pytest` for running tests.
- **Operating System**: Windows, macOS, or Linux.
- **Disk Space**: Approximately 10 MB for the repository and dependencies.

## Installation
Follow these steps to set up **mr_h4shtag** locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sharpnova/mr_h4shtag.git
   cd mr_h4shtag
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   Run the help command to confirm setup:
   ```bash
   python src/main.py --help
   ```
   Expected output:
   ```
   usage: main.py [-h] [-f FILE] [-t TEXT] [-o OUTPUT] [--min-length MIN_LENGTH]
                  [--max-length MAX_LENGTH] [--top-n TOP_N] [--case-sensitive]
                  [--pattern PATTERN] [-v]

   mr_h4shtag: A CLI tool for hashtag extraction and analysis.

   options:
     -h, --help            show this help message and exit
     -f, --file FILE       Path to input file (txt, json, csv)
     -t, --text TEXT       Direct text input
     -o, --output OUTPUT   Path to output file (txt, json)
     ...
   ```

5. **Optional: Install for Development**:
   To run tests or contribute, install additional dependencies:
   ```bash
   pip install pytest
   ```

## Configuration
**mr_h4shtag** is configured via command-line arguments, with no external configuration files required. For advanced customization:
- **Modify Regex Patterns**: Edit `hashtag_parser.py` to change the default hashtag regex (`r'#[\w]+'`) for specific use cases (e.g., supporting emojis in hashtags).
- **Adjust Logging**: Update `utils.py` to change the logging level (default: `INFO`). Enable verbose mode with `-v` for detailed logs.
- **Environment Variables**: Future releases may support environment variables for API keys or custom settings.

Example: Enable verbose logging:
```bash
python src/main.py -f examples/sample.txt -v
```

## Usage
**mr_h4shtag** is invoked via the command line and supports inputs from files, direct text, or STDIN. Outputs can be directed to the terminal or saved as files.

### Command-Line Interface
The CLI supports the following options:

| Option                | Type   | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `-f, --file <path>`   | String | Path to input file (`.txt`, `.json`, `.csv`).                               |
| `-t, --text <text>`   | String | Direct text input containing hashtags.                                      |
| `-o, --output <path>` | String | Path to output file (`.txt`, `.json`).                                      |
| `--min-length <int>`  | Integer| Minimum hashtag length (characters, excluding `#`).                         |
| `--max-length <int>`  | Integer| Maximum hashtag length (characters, excluding `#`).                         |
| `--top-n <int>`       | Integer| Display the top N most frequent hashtags.                                   |
| `--case-sensitive`    | Flag   | Enable case-sensitive hashtag matching (default: case-insensitive).         |
| `--pattern <regex>`   | String | Filter hashtags matching a regex pattern (e.g., `^#data.*`).                |
| `-v, --verbose`       | Flag   | Enable verbose logging for debugging.                                       |
| `-h, --help`          | Flag   | Display help message and exit.                                              |

### Examples
The following examples demonstrate common use cases, using files from the `examples/` directory.

1. **Extract Hashtags from a Text File**:
   ```bash
   python src/main.py -f examples/sample.txt
   ```
   **Input** (`examples/sample.txt`):
   ```
   I love #coding and #python!
   #python is awesome. #coding #tech
   Trying out #datascience with #python3
   ```
   **Output** (terminal):
   ```
   Summary:
     Total hashtags: 7
     Unique hashtags: 5
     Frequency distribution:
       #python: 2
       #coding: 2
       #tech: 1
       #datascience: 1
       #python3: 1
   ```

2. **Process Direct Text Input**:
   ```bash
   python src/main.py -t "I love #coding and #python! #coding is fun."
   ```
   **Output**:
   ```
   Summary:
     Total hashtags: 3
     Unique hashtags: 2
     Frequency distribution:
       #coding: 2
       #python: 1
   ```

3. **Save Output to JSON**:
   ```bash
   python src/main.py -f examples/sample.txt -o results.json
   ```
   **Output** (`results.json`):
   ```json
   {
     "timestamp": "2025-04-28T12:00:00Z",
     "total": 7,
     "unique": 5,
     "hashtags": [
       {"tag": "#python", "count": 2},
       {"tag": "#coding", "count": 2},
       {"tag": "#tech", "count": 1},
       {"tag": "#datascience", "count": 1},
       {"tag": "#python3", "count": 1}
     ]
   }
   ```

4. **Filter Hashtags by Length and Top-N**:
   ```bash
   python src/main.py -f examples/sample.txt --min-length 5 --top-n 3
   ```
   **Output**:
   ```
   Summary (hashtags with length >= 5):
     Total hashtags: 4
     Unique hashtags: 3
     Top 3 hashtags:
       #python: 2
       #coding: 2
       #datascience: 1
   ```

5. **Case-Sensitive Matching**:
   ```bash
   python src/main.py -t "#Python #python #PYTHON" --case-sensitive
   ```
   **Output**:
   ```
   Summary:
     Total hashtags: 3
     Unique hashtags: 3
     Frequency distribution:
       #Python: 1
       #python: 1
       #PYTHON: 1
   ```

6. **Pipe Input from STDIN**:
   ```bash
   cat examples/sample.txt | python src/main.py
   ```
   **Output**: Same as Example 1.

7. **Custom Regex Filtering**:
   ```bash
   python src/main.py -f examples/sample.txt --pattern "^#data.*"
   ```
   **Output**:
   ```
   Summary (hashtags matching '^#data.*'):
     Total hashtags: 1
     Unique hashtags: 1
     Frequency distribution:
       #datascience: 1
   ```

8. **Process Large Dataset**:
   ```bash
   python src/main.py -f examples/large_dataset.txt --top-n 5 -o large_results.json
   ```
   Suitable for stress-testing with the provided `large_dataset.txt`.

## Input and Output Specifications

### Supported Input Formats
- **Text Files (`.txt`)**:
  - Plain text with embedded hashtags.
  - Processed line-by-line for memory efficiency.
  - Example (`examples/sample.txt`):
    ```
    I love #coding and #python!
    #python is awesome. #coding #tech
    ```
- **JSON Files (`.json`)**:
  - Supports arrays of strings or objects with a `text` field.
  - Example (`examples/sample.json`):
    ```json
    [
      {"text": "I love #coding and #python!"},
      {"text": "#python is awesome. #coding #tech"}
    ]
    ```
- **CSV Files (`.csv`)**:
  - Requires a `text` column containing hashtag data.
  - Example (`examples/sample.csv`):
    ```csv
    text
    "I love #coding and #python!"
    "#python is awesome. #coding #tech"
    ```
- **STDIN**:
  - Accepts piped input for integration with other tools.
  - Example:
    ```bash
    echo "I love #coding" | python src/main.py
    ```

### Supported Output Formats
- **Terminal**:
  - Human-readable summary with statistics and hashtag frequencies.
  - Configurable verbosity with `-v`.
- **Text File (`.txt`)**:
  - Mirrors terminal output in a plain text format.
  - Example:
    ```
    Total hashtags: 7
    Unique hashtags: 5
    #python: 2
    #coding: 2
    ...
    ```
- **JSON File (`.json`)**:
  - Structured data with metadata (timestamp, totals, hashtag details).
  - Example (see Example 3 above).

## Advanced Features
- **Custom Regex Patterns**: Use `--pattern` to filter hashtags (e.g., `#data.*` for data-related tags).
- **Unicode Support**: Handles non-ASCII hashtags (e.g., `#программирование`, `#データ`).
- **Streaming I/O**: Processes large files efficiently by reading line-by-line.
- **Logging**: Detailed logs for debugging, accessible via `-v`.
- **Error Recovery**: Gracefully handles malformed inputs with clear error messages.
- **Extensible Filters**: Add custom filtering logic in `hashtag_parser.py` (e.g., sentiment-based filtering).

## Performance Optimization
- **Time Complexity**: Linear (`O(n)`) for text processing, where `n` is the input size.
- **Memory Usage**: Stream-based I/O minimizes memory footprint, suitable for files up to 1 GB.
- **Optimization Tips**:
  - Use `--min-length` or `--pattern` to reduce parsing overhead.
  - Split very large files into smaller chunks for faster processing.
  - Enable verbose mode (`-v`) to identify bottlenecks.
- **Benchmarking**:
  The repository includes a sample large dataset (`examples/large_dataset.txt`) for performance testing:
  ```bash
  python src/main.py -f examples/large_dataset.txt -v
  ```

## Testing
The `tests/` directory contains unit and integration tests to ensure reliability:
```bash
pip install pytest
python -m pytest tests/
```
**Test Coverage**:
- Hashtag extraction (valid/invalid hashtags, Unicode, edge cases).
- Input parsing (`.txt`, `.json`, `.csv`, STDIN).
- Output formatting (terminal, `.txt`, `.json`).
- Error handling (malformed files, invalid arguments).
- Filtering logic (length, regex, case sensitivity).

To add tests:
1. Create a new file in `tests/` (e.g., `test_new_feature.py`).
2. Use `pytest` conventions for test discovery.
3. Run `pytest --cov=src` to check code coverage.

## Extending the Tool
**mr_h4shtag** is designed for extensibility. To add new features:
1. **New Input Format**:
   - Update `input_validator.py` to validate the new format.
   - Add parsing logic in `hashtag_parser.py`.
   - Example: Add XML support by parsing `<text>` tags.
2. **New Output Format**:
   - Extend `output_handler.py` with a new method (e.g., `write_yaml`).
   - Update `main.py` to accept the new format via `--output`.
3. **Custom Filters**:
   - Add filter methods in `hashtag_parser.py` (e.g., `filter_by_category`).
   - Expose filters via new CLI arguments in `main.py`.
4. **API Integration**:
   - Create a new module (e.g., `api_client.py`) for fetching data from APIs.
   - Use environment variables for API credentials.
5. **Documentation**:
   - Update `docs/api.md` with new function details.
   - Add usage examples in `examples/`.

Refer to `docs/api.md` for function-level documentation.

## Troubleshooting
Common issues and solutions:
- **"File not found"**:
  - Verify the file path is correct and accessible.
  - Use absolute paths (e.g., `/path/to/file.txt`).
- **"Invalid JSON/CSV"**:
  - Validate files using tools like `jq` (JSON) or `csvlint` (CSV).
  - Check for missing `text` columns in CSV files.
- **Slow Performance**:
  - Apply filters (`--min-length`, `--pattern`) to reduce processing.
  - Use `examples/large_dataset.txt` to test optimizations.
- **No Hashtags Found**:
  - Ensure input contains valid hashtags (e.g., `#tag`, not `tag` or `@tag`).
  - Disable `--case-sensitive` or check `--pattern` syntax.
- **Verbose Logs**:
  - Run with `-v` to capture detailed error messages:
    ```bash
    python src/main.py -f examples/sample.txt -v
    ```

For persistent issues, open an issue on GitHub with:
- Python version and OS.
- Command used and input file.
- Full error message or unexpected output.

## Contributing
We welcome contributions to **mr_h4shtag**! To contribute:
1. **Fork the Repository**:
   ```bash
   git clone https://github.com/sharpnova/mr_h4shtag.git
   cd mr_h4shtag
   ```
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Write Code**:
   - Adhere to PEP 8 style guidelines.
   - Add tests in `tests/` for new features.
   - Update `docs/` with relevant changes.
4. **Commit and Push**:
   ```bash
   git commit -m "Add your feature"
   git push origin feature/your-feature
   ```
5. **Open a Pull Request**:
   - Provide a detailed description of changes.
   - Reference related issues (e.g., `Fixes #123`).
   - Ensure tests pass locally (`pytest tests/`).

See `docs/contributing.md` for detailed guidelines, including code style and pull request templates.

## Support
For assistance:
- **Issues**: Browse or open issues at [GitHub Issues](https://github.com/sharpnova/mr_h4shtag/issues).
- **Discussions**: Join community discussions at [GitHub Discussions](https://github.com/sharpnova/mr_h4shtag/discussions).
- **Contact**: Reach out to the maintainer via GitHub for private inquiries.

When reporting issues, include:
- Python version (e.g., `python --version`).
- Operating system and version.
- Command used and input file (if applicable).
- Full error message or unexpected output.

## Roadmap
Future enhancements planned for **mr_h4shtag**:
- **Input Formats**: Support for XML, YAML, and database inputs (e.g., SQLite).
- **API Integration**: Real-time hashtag extraction from social media APIs (e.g., Twitter/X, Instagram).
- **NLP Features**: Sentiment analysis and topic modeling for hashtags.
- **Parallel Processing**: Multi-threading for faster processing of large datasets.
- **GUI Interface**: Web or desktop interface for non-technical users.
- **Localization**: Full support for non-Latin hashtags and multilingual documentation.
- **CI/CD**: Automated testing and release pipelines via GitHub Actions.

Track progress and suggest features in [GitHub Issues](https://github.com/sharpnova/mr_h4shtag/issues) or [GitHub Projects](https://github.com/sharpnova/mr_h4shtag/projects).

## License
**mr_h4shtag** is released under the [MIT License](LICENSE). You are free to use, modify, and distribute the software, provided you include the original copyright notice and license terms. See the `LICENSE` file for details.

## Acknowledgments
- **Contributors**: Thanks to all contributors who have submitted code, issues, or feedback.
- **Open-Source Community**: Inspired by tools like `grep`, `jq`, and Python's `argparse`.
- **Libraries**: Built on Python's standard libraries for robust text processing.

---

Thank you for using **mr_h4shtag**! This tool is designed to simplify hashtag analysis and integrate seamlessly into your workflows. We value your feedback and contributions to make **mr_h4shtag** even better. Star the repository on [GitHub](https://github.com/sharpnova/mr_h4shtag) to show your support! 🌟