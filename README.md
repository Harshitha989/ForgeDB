
# ForgeDB

ForgeDB is a beginner-friendly relational database engine
implemented from scratch in Python.

## Features

- Create tables with INT and TEXT columns
- Insert, select, update, and delete records
- Basic WHERE filtering
- Persistent file-based storage
- Interactive SQL terminal

## Requirements

- Python 3.10 or later
- No third-party Python packages

## Run ForgeDB

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

- catalog: table schemas
- parser: SQL parsing
- executor: query execution
- storage: persistent records
- engine.py: connects the modules
- main.py: interactive terminal

## Current limitations

ForgeDB is an educational prototype. It does not yet support
joins, indexes, transactions, concurrent access, or full SQL.
Storage currently uses JSON files rather than custom binary pages.
