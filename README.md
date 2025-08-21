# Nilor CLI

Interactive command-line interface for the Nilor AI stack. Chat with an AI agent that searches your knowledge base and provides relevant insights.

## Setup

### Prerequisites

1. Google Cloud Project with Vertex AI APIs enabled
2. gcloud CLI authenticated with appropriate permissions
3. uv for Python dependency management

### Quick Start

1. **Install dependencies**:
   ```bash
   cd src
   uv sync
   ```

2. **Authenticate with Google Cloud**:
   ```bash
   gcloud config set project robot-rnd-nilor-gcp
   gcloud auth login
   ```

3. **Run the CLI**:
   ```bash
   uv run python main.py
   ```

## Usage

Start chatting with the AI agent:

```
nilor> Search your knowledge base for digital sovereignty
nilor> What is a network state?
nilor> Tell me about creative blocks and motivation
nilor> quit
```

## Local Development

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run with debug output
uv run python main.py --debug
```

## Enhancements

1. TBD