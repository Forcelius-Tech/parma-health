# Parma Health Toolkit

The Parma Health Toolkit is a modular, local-first Python library designed to act as a secure "sanitization gateway" for sensitive healthcare data. It ensures no Protected Health Information (PHI) leaves the secure source zone without proper anonymization.

## Features

- **Ingestion Layer:** Connectors to read data from CSV, JSON, and other sources without altering the original data.
- **Core Engine:** Anonymization engine supporting masking, generalization, and pseudonymization rules.
- **Validation Layer:** Generates compliance artifacts and transformation logs.
- **Output Layer:** Writes sanitized data to the destination.

## Installation

```bash
pip install parma-health
```

## Usage

```bash
parma-health --help
```

## Development

```bash
git clone https://github.com/org/parma-health-toolkit.git
cd parma-health-toolkit
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```
