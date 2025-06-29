# python-bsdl-parser

This is a Lark-based parser for IEEE 1149.1 Boundary-Scan Description
Language (BSDL) files.

## Requirements

* Python 3.13+
* Lark 1.2.2+

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install Lark directly:

```bash
pip install lark
```

## Usage

The parser provides a command-line interface with various options:

### Basic Usage

```bash
python src/main.py [BSDL_FILE] [OPTIONS]
```

### Command Line Arguments

- `filename`: BSDL file to parse (required)
- `--output`: Output file (default: "output.json")
- `--format`: Output format ("json" or "str", default: "json")
- `--type`: Type to parse (optional)
- `--method`: Special parsing method (optional)
- `--seperate`: Separate output (default: False)

### Examples

#### 1. Basic parsing to JSON file:
```bash
python src/main.py test/PG2L100H_FBG676.bsm --output result.json
```

#### 2. Get logic port description:
```bash
python src/main.py test/PG2L100H_FBG676.bsm --method GetLogicPortDesp --output ports.json
```

#### 3. Get boundary scan register description:
```bash
python src/main.py test/PG2L100H_FBG676.bsm --method GetBoundaryScanRegDesp --output boundary.json
```

#### 4. Get pin mapping:
```bash
python src/main.py test/PG2L100H_FBG676.bsm --method GetPinMap --output pinmap.json
```

#### 5. Output to console (string format):
```bash
python src/main.py test/PG2L100H_FBG676.bsm --format str
```

### Available Methods

- `GetLogicPortDesp`: Extract logic port descriptions
- `GetBoundaryScanRegDesp`: Extract boundary scan register descriptions  
- `GetPinMap`: Extract pin mapping information

### Output Formats

- `json`: Save results to a JSON file
- `str`: Print results to console
