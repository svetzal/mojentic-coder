# Mojentic Coder

Mojentic Coder is an agentic software engineering tool that puts the developer in charge of the vision and direction of the project, while the agents take care of the toil in putting it together.

## Features

### Epic 1: Agent Management (In Progress)

- Upon launch, the tool opens a full-size window with three blank panels
- Agents can be defined in the left-hand panel
  - Agents have a Gateway (OpenAI or Ollama), a Model (the list of models is retrieved via the chosen gateway), and a system prompt that defines their character and behaviour
- When an Agent is created, a Chat Session is created with the agent, which is displayed in the middle panel
- When an Agent is created, the user can type a message in the bottom of the middle panel, which is sent to the agent's Chat Session

## Installation

### Requirements

- Python 3.13 or higher

### Install from source

```bash
git clone https://github.com/yourusername/mojentic-coder.git
cd mojentic-coder
pip install -e .
```

## Usage

After installation, you can run the application using:

```bash
mojentic-coder
```

Or directly with Python:

```bash
python -m mojentic_coder
```

## Development

### Setup development environment

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

## License

MIT