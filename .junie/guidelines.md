# Mojentic Coder Development Guidelines

You must update this guidelines file (`.junie/guidelines.md`) when you learn new things about the user's expectations, especially if the user tells you to remember something.

## Project Overview

Mojentic Coder is an agentic software engineering assistant that helps developers create better software. It is a Qt GUI application that coordinates a number of user-defined autonomous agents to plan, perform, and critique engineering tasks at the request of the developer.

The GUI is to consist of a left panel, a right panel, and a middle panel.

The left panel is a list of the agents that are working autonomously on behalf of the developer.

The right panel is split in two, the top is a live view of the goals and tasks that the agents are working on, and the bottom view is a live view of the trace of the agents' actions.

The middle panel is split in two, the top is the list of messages that the agents are sending to each other and to the developer. The bottom is a messagebox where the developer can send messages to the working agents.

## Tech Stack

- Python 3.13+
- Key Dependencies:
  - pydantic: Strongly typed data
  - structlog: Logging
  - pytest: Testing
  - mojentic: LLM interaction and agentic framework
  - pyside6: Qt6 library for Python for creating rich GUI applications

## Project Structure
```
docs/                  # Documentation files (MkDocs)
src/
├── mojentic_coder/    # Main package
│   ├── models/        # Data models using pydantic
│   ├── panels/        # UI panels (Qt widgets)
│   ├── services/      # Business logic and services
│   ├── tests/         # Test files
│   ├── config.py      # Application configuration
│   └── main.py        # Main application entry point
```

## Development Setup
1. Install Python 3.13 or higher
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Install pre-commit hooks (recommended):
   ```bash
   # Create a pre-commit hook that runs pytest
   cat > .git/hooks/pre-commit << 'EOL'
   #!/bin/sh

   # Run pytest
   echo "Running pytest..."
   python -m pytest

   # Store the exit code
   exit_code=$?

   # Exit with pytest's exit code
   exit $exit_code
   EOL

   # Make the hook executable
   chmod +x .git/hooks/pre-commit
   ```

## Testing Guidelines
- Tests are co-located with implementation files (test file must be in the same folder as the implementation)
- We write tests as specifications, therefore you can find all the tests in the *_spec.py files
- Run tests: `pytest`
- Linting: `flake8 src`
- Code style:
  - Max line length: 127
  - Max complexity: 10
  - Follow numpy docstring style

### Testing Best Practices
- Use pytest for testing, with mocker if you require mocking
- Do not use unittest or MagicMock directly, use it through the mocker wrapper
- Use @fixture markers for pytest fixtures
- Break up fixtures into smaller fixtures if they are too large
- Do not write Given/When/Then or Act/Arrange/Assert comments
- Do not write docstring comments on your should_ methods
- Separate test phases with a single blank line
- Do not write conditional statements in tests
- Each test must fail for only one clear reason

## Code Style Requirements
- Follow the existing project structure
- Write tests for new functionality
- Document using numpy-style docstrings
- Keep code complexity low
- Use type hints for all functions and methods
- Co-locate tests with implementation
- Favor declarative code styles over imperative code styles
- Use pydantic (not @dataclass) for data objects with strong types
- Favor list and dictionary comprehensions over for loops

## Qt/PySide6 Conventions

### UI Architecture
- The application follows a panel-based architecture where each major UI component is a separate panel class
- Panels are implemented as QWidget subclasses with a clear single responsibility
- The main window (QMainWindow) coordinates the panels and handles top-level UI elements like menus
- Use a service-based approach for business logic, with panels interacting with services through interfaces

### UI Implementation
- Build UI programmatically using layouts (QVBoxLayout, QHBoxLayout, QFormLayout) rather than using Qt Designer
- Use consistent margins and spacing in layouts for visual coherence
- Implement complex list items as custom widgets with their own layouts
- Follow a consistent naming convention for UI elements (e.g., `self.agent_list`, `self.create_agent_button`)

### Signal-Slot Communication
- Define signals at the class level using the Signal class
- Use descriptive signal names that indicate what event occurred (e.g., `agent_selected`, `agent_created`)
- Connect signals to slots using the `connect` method
- Use the `@Slot` decorator for slot methods to ensure proper type checking

### Form Handling
- Validate form inputs in code before performing actions
- Use appropriate input widgets for different data types (QLineEdit for text, QComboBox for selections, etc.)
- Provide clear feedback for validation errors
- Reset form fields when showing dialogs

### Service Integration
- Obtain services from a central ServiceProvider
- Use dependency injection to provide services to panels
- Define clear interfaces for services to allow for testing and flexibility
- Handle service exceptions gracefully with appropriate user feedback

### Documentation
- Document all panel classes with a clear description of their purpose
- Document signals with their purpose and parameters
- Document methods with their purpose and parameters using numpy-style docstrings
- Include type hints for all method parameters and return values

## Mojentic Development

### LLM Tool Development

1. When writing a new LLM tool, model the implementation after `mojentic.llm.tools.date_resolver.ResolveDateTool`
2. For LLM-based tools, take the LLMBroker object as a parameter in the tool's initializer
3. Don't ask the LLM to generate JSON directly, use the `LLMBroker.generate_object()` method instead

## Documentation

- Built with MkDocs and Material theme
- API documentation uses mkdocstrings
- Supports mermaid.js diagrams in markdown files:
  ```mermaid
  graph LR
      A[Doc] --> B[Feature]
  ```
- Build docs locally: `mkdocs serve`
- Build for production: `mkdocs build`
- Markdown files
    - Use `#` for top-level headings
    - Put blank lines above and below bulleted lists, numbered lists, headings, quotations, and code blocks
- Always keep the navigation tree in `mkdocs.yml` up to date with changes to the available documents in the `docs` folder

### API Documentation

API documentation uses mkdocstrings, which inserts module, class, and method documentation using certain markers in the markdown documents.

eg.

```
::: mojentic.llm.MessageBuilder
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
```

Always use the same `show_root_heading`, `merge_init_into_class`, and `group_by_category` options. Adjust the module and class name after the `:::` as needed.

## Release Process

1. Update CHANGELOG.md:
   - All notable changes should be documented under the [Unreleased] section
   - Group changes into categories:
     - Added: New features
     - Changed: Changes in existing functionality
     - Deprecated: Soon-to-be removed features
     - Removed: Removed features
     - Fixed: Bug fixes
     - Security: Security vulnerability fixes
   - Each entry should be clear and understandable to end-users
   - Reference relevant issue/PR numbers where applicable

2. Creating a Release:
   - Ensure `pyproject.toml` has the next release version
   - Ensure all changes are documented in CHANGELOG.md
     - Move [Unreleased] changes to the new version section (e.g., [1.0.0])
   - Follow semantic versioning:
     - MAJOR version for incompatible API changes
     - MINOR version for backward-compatible new functionality
     - PATCH version for backward-compatible bug fixes

3. Best Practices:
   - Keep entries concise but descriptive
   - Write from the user's perspective
   - Include migration instructions for breaking changes
   - Document API changes thoroughly
   - Update documentation to reflect the changes

## Running Scripts

1. Example scripts are in `src/_examples/`
2. Basic usage:
   ```python
   from mojentic.llm import LLMBroker
   from mojentic.agents import BaseLLMAgent
   ```
3. See example files for common patterns:
   - simple_llm.py: Basic LLM usage
   - chat_session.py: Chat interactions
   - working_memory.py: Context management

## Release Process

This project follows [Semantic Versioning](https://semver.org/) (SemVer) for version numbering. The version format is MAJOR.MINOR.PATCH, where:

1. MAJOR version increases for incompatible API changes
2. MINOR version increases for backward-compatible functionality additions
3. PATCH version increases for backward-compatible bug fixes

### Preparing a Release

When preparing a release, follow these steps:

1. **Update CHANGELOG.md**:
   - Move items from the "[Next]" section to a new version section
   - Add the new version number and release date: `## [x.y.z] - YYYY-MM-DD`
   - Ensure all changes are properly categorized under "Added", "Changed", "Deprecated", "Removed", "Fixed", or "Security"
   - Keep the empty "[Next]" section at the top for future changes

2. **Update Version Number**:
   - Update the version number in `pyproject.toml`
   - Ensure the version number follows semantic versioning principles based on the nature of changes:
     - **Major Release**: Breaking changes that require users to modify their code
     - **Minor Release**: New features that don't break backward compatibility
     - **Patch Release**: Bug fixes that don't add features or break compatibility

3. **Update Documentation**:
   - Review and update `README.md` to reflect any new features, changed behavior, or updated requirements
   - Update any other documentation files that reference features or behaviors that have changed
   - Ensure installation instructions and examples are up to date

4. **Final Verification**:
   - Run all tests to ensure they pass
   - Verify that the application works as expected with the updated version
   - Check that all documentation accurately reflects the current state of the project

### Release Types

#### Major Releases (x.0.0)

Major releases may include:

- Breaking API changes (eg tool plugin interfacing)
- Significant architectural changes
- Removal of deprecated features
- Changes that require users to modify their code or workflow

For major releases, consider:
- Providing migration guides
- Updating all documentation thoroughly
- Highlighting breaking changes prominently in the CHANGELOG

#### Minor Releases (0.x.0)

Minor releases may include:

- New features
- Non-breaking enhancements
- Deprecation notices (but not removal of deprecated features)
- Performance improvements

For minor releases:
- Document all new features
- Update README to highlight new capabilities
- Ensure backward compatibility

#### Patch Releases (0.0.x)

Patch releases should be limited to:

- Bug fixes
- Security updates
- Performance improvements that don't change behavior
- Documentation corrections

For patch releases:

- Clearly describe the issues fixed
- Avoid introducing new features
- Maintain strict backward compatibility

# mojentic: Using the Mojentic Library

Mojentic is an agentic framework that provides a simple and flexible way to assemble teams of agents to solve complex problems. It supports integration with various LLM providers (Ollama, OpenAI, Anthropic) and includes tools for task automation.

## Core Components

### LLMBroker

The central component for interacting with language models:

```python
from mojentic.llm import LLMBroker

# Create a broker with a specific model
llm_broker = LLMBroker(model="llama3.3-70b-32k")  # Uses Ollama by default

# For OpenAI models
from mojentic.llm.gateways.openai import OpenAIGateway
llm_broker = LLMBroker(model="gpt-4-turbo", gateway=OpenAIGateway())
```

Use the broker to generate responses:

```python
from mojentic.llm.gateways.models import LLMMessage, MessageRole

# Generate a text response
messages = [
    LLMMessage(role=MessageRole.System, content="You are a helpful assistant."),
    LLMMessage(role=MessageRole.User, content="What is the capital of France?")
]
response = llm_broker.generate(messages)

# Generate a structured response
from pydantic import BaseModel

class CapitalInfo(BaseModel):
    country: str
    capital: str
    population: int

structured_response = llm_broker.generate_object(messages, object_model=CapitalInfo)
print(structured_response.capital)  # "Paris"
```

You can also get a list of available models from any LLM gateway implementation:

```python
from mojentic.llm.gateways import OllamaGateway, OpenAIGateway
from mojentic.llm.gateways.anthropic import AnthropicGateway
import os

# List Ollama models
ollama = OllamaGateway()
ollama_models = ollama.get_available_models()
print("Available Ollama models:", ollama_models)

# List OpenAI models
openai = OpenAIGateway(os.environ["OPENAI_API_KEY"])
openai_models = openai.get_available_models()
print("Available OpenAI models:", openai_models)

# List Anthropic models
anthropic = AnthropicGateway(os.environ["ANTHROPIC_API_KEY"])
anthropic_models = anthropic.get_available_models()
print("Available Anthropic models:", anthropic_models)
```

### ChatSession

Manages stateful conversations with automatic context management:

```python
from mojentic.llm import ChatSession, LLMBroker

llm_broker = LLMBroker(model="llama3.3-70b-32k")
chat_session = ChatSession(
    llm_broker,
    system_prompt="You are a helpful assistant specialized in geography.",
    max_context=16384  # Automatically manages context window
)

response = chat_session.send("What is the capital of France?")
follow_up = chat_session.send("What is its population?")  # Maintains conversation context
```

### Tools

Extend LLM capabilities with specialized tools:

```python
from mojentic.llm import ChatSession, LLMBroker
from mojentic.llm.tools.date_resolver import ResolveDateTool

# Create a chat session with a tool
llm_broker = LLMBroker(model="llama3.3-70b-32k")
chat_session = ChatSession(llm_broker, tools=[ResolveDateTool()])

# The LLM can now resolve relative dates
response = chat_session.send("What date is next Monday?")
```

Create custom tools by extending LLMTool:

```python
from mojentic.llm.tools.llm_tool import LLMTool

class WeatherTool(LLMTool):
    def run(self, location: str):
        # Implement weather lookup logic
        return {"temperature": 22, "conditions": "sunny"}

    @property
    def descriptor(self):
        return {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or location name"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
```

### Agents

Create agents with different capabilities:

```python
from mojentic.agents import BaseLLMAgent
from mojentic.llm import LLMBroker

llm_broker = LLMBroker(model="llama3.3-70b-32k")
agent = BaseLLMAgent(
    llm_broker,
    behaviour="You are a helpful assistant specialized in geography."
)

response = agent.generate_response("What is the capital of France?")
```

Agents with memory:

```python
from mojentic.agents import BaseLLMAgentWithMemory
from mojentic.context.shared_working_memory import SharedWorkingMemory
from pydantic import BaseModel

class Response(BaseModel):
    answer: str

memory = SharedWorkingMemory()
agent = BaseLLMAgentWithMemory(
    llm_broker,
    memory=memory,
    behaviour="You are a helpful assistant.",
    instructions="Answer the user's question.",
    response_model=Response
)

# Agent will remember information across interactions
response = agent.generate_response("My name is Alice.")
response = agent.generate_response("What's my name?")  # Will know the name is Alice
```

### Tracer

Monitor and analyze interactions with LLMs and tools for debugging and observability:

```python
from mojentic.tracer import TracerSystem
from mojentic.tracer.tracer_events import (
    LLMCallTracerEvent, 
    LLMResponseTracerEvent, 
    ToolCallTracerEvent,
    AgentInteractionTracerEvent
)
from mojentic.llm import LLMBroker, ChatSession
from mojentic.llm.tools.date_resolver import ResolveDateTool

# Create a tracer system
tracer = TracerSystem()

# Integrate with LLMBroker
llm_broker = LLMBroker(model="llama3.3-70b-32k", tracer=tracer)

# Integrate with tools
date_tool = ResolveDateTool(llm_broker=llm_broker, tracer=tracer)

# Create a chat session with the broker and tool
chat_session = ChatSession(llm_broker, tools=[date_tool])

# Use the chat session normally
response = chat_session.send("What day is next Friday?")

# Retrieve and analyze traced events
all_events = tracer.get_events()
print(f"Total events recorded: {len(all_events)}")

# Filter events by type
llm_calls = tracer.get_events(event_type=LLMCallTracerEvent)
llm_responses = tracer.get_events(event_type=LLMResponseTracerEvent)
tool_calls = tracer.get_events(event_type=ToolCallTracerEvent)
agent_interactions = tracer.get_events(event_type=AgentInteractionTracerEvent)

# Get the last few events
last_events = tracer.get_last_n_tracer_events(3)

# Filter events by time range
start_time = 1625097600.0  # Unix timestamp
end_time = 1625184000.0    # Unix timestamp
time_filtered_events = tracer.get_events(start_time=start_time, end_time=end_time)

# Print event summaries
for event in last_events:
    print(event.printable_summary())

# Extract specific information from events
if tool_calls:
    tool_usage = {}
    for event in tool_calls:
        tool_name = event.tool_name
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

    print("Tool usage frequency:")
    for tool_name, count in tool_usage.items():
        print(f"  - {tool_name}: {count} calls")
```

#### Tracer Event Types

The tracer system captures different types of events:

1. **LLMCallTracerEvent**: Records when an LLM is called
   - `model`: The LLM model used
   - `messages`: The messages sent to the LLM
   - `temperature`: The temperature setting used
   - `tools`: The tools available to the LLM

2. **LLMResponseTracerEvent**: Records when an LLM responds
   - `model`: The LLM model used
   - `content`: The content of the response
   - `tool_calls`: Any tool calls made by the LLM
   - `call_duration_ms`: Duration of the call in milliseconds

3. **ToolCallTracerEvent**: Records tool usage
   - `tool_name`: Name of the tool called
   - `arguments`: Arguments provided to the tool
   - `result`: Result returned by the tool
   - `caller`: Component that called the tool

4. **AgentInteractionTracerEvent**: Records agent interactions
   - `from_agent`: Agent sending the event
   - `to_agent`: Agent receiving the event
   - `event_type`: Type of event being processed
   - `event_id`: Unique identifier for the event

Each event has a `printable_summary()` method that formats the event information for display.

## Best Practices

1. **Model Selection**: Choose appropriate models for your task:
   - Smaller models for simple tasks (faster, cheaper)
   - Larger models for complex reasoning

2. **Context Management**: Use ChatSession for long conversations to automatically manage context window limits

3. **Structured Output**: Use `generate_object()` instead of parsing JSON manually

4. **Tools**: Extend capabilities with tools rather than complex prompting

5. **Memory**: Use BaseLLMAgentWithMemory when information needs to persist across interactions

6. **Tracing**: Use the TracerSystem to monitor and debug interactions with LLMs and tools
