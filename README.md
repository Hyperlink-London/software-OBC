# Hyperlink-OBC

## Overview

Hyperlink OBC (On-Board Computer) is a Python-based application designed to control the Hyperlink pod and manage communication with the Hyperlink API. The system implements a state machine architecture for pod control and provides robust communication interfaces.

## Project Structure

```
hyperlink-OBC/
├── src/                    # Source code
│   ├── comms/             # Communication modules
│   ├── datamodels/        # Data models and schemas
│   ├── fsm/              # Finite State Machine implementation
│   ├── main.py           # Application entry point
│   ├── obc-tests.py      # Testing code for the OBC
│   ├── constants.py      # System constants
│   └── logger.py         # Logging configuration
├── logs/                  # Application logs
├── requirements.txt       # Python dependencies
├── .env.sample           # Example environment variables
└── .env                  # Environment variables (not in git)
```

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Hyperlink-London/software-OBC.git
cd hyperlink-OBC
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.sample .env
# Edit .env with your configuration
```

## Running the Application

### Local Development

```bash
python src/main.py
```

## Features

- State machine-based pod control system
- Asynchronous communication with Hyperlink API
- Serial communication interface
- Comprehensive logging system
- Environment-based configuration

## Dependencies

Key dependencies include:
- `aiohttp`: Asynchronous HTTP client/server
- `pyserial`: Serial communication
- `transitions`: State machine implementation
- `websockets`: WebSocket client/server
- `python-dotenv`: Environment variable management