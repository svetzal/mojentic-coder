# Mojentic Coder

Mojentic Coder is an agentic software engineering tool that puts the developer in charge of the vision and direction of the project, while the agents take care of the toil in putting it together.

## Features

### Agent Management (In Progress)

- The user can create a series of agents that can be coordinated to solve problems and write code
- Currently the user can chat with any of the agents individually
  - Next step is to allow the user to define formation for the agents, we're going to start with an asynchronous eventing style
- Also started work on a goal/task management system, next step will be to create a series of tools for the agents to interact with the goals / tasks, with the panel reflecting changes in real time as the agents update them asynchronously

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