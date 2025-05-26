
# Mojentic Coder Services Architecture

This directory contains the service layer for the Mojentic Coder application. The service layer separates the UI components from the mojentic framework, enabling asynchronous messaging and testability.

## Architecture Overview

The architecture follows these principles:

1. **Separation of Concerns**: UI components are separated from application logic.
2. **Dependency Inversion**: High-level modules (UI) depend on abstractions (interfaces), not concrete implementations.
3. **Dependency Direction**: Dependencies flow from UI → application services → mojentic framework.
4. **No Cyclic Dependencies**: Dependencies are unidirectional to avoid cycles.

## Components

### Interfaces

The `interfaces.py` file defines the service interfaces that establish a clear contract between the UI and the application logic:

- `AgentServiceInterface`: Defines methods for agent management.
- `MessageServiceInterface`: Defines methods for message handling.

### Implementations

- `agent_service.py`: Implements the `AgentServiceInterface`, handling agent creation and management.
- `message_service.py`: Implements the `MessageServiceInterface`, handling asynchronous message sending and chat history retrieval.

### Service Provider

The `service_provider.py` file provides a service locator that manages service instances and provides them to the UI components. This enables:

1. **Dependency Injection**: Services are provided to UI components rather than created by them.
2. **Testability**: Services can be replaced with mock implementations for testing.
3. **Singleton Management**: Ensures only one instance of each service exists.

## Asynchronous Messaging

The `MessageService` implements asynchronous messaging using threading:

1. When a message is sent, a new thread is created to handle the request.
2. The UI remains responsive while waiting for the response.
3. When the response is received, a callback is invoked to update the UI.

This allows sending messages to different agents without waiting for responses, as required by the application.

## Testability

The service layer is designed to be testable by:

1. **Defining Interfaces**: Services implement interfaces, allowing them to be mocked in tests.
2. **Dependency Injection**: Dependencies are injected, allowing them to be replaced with mocks.
3. **Separation from UI**: Services don't depend on UI components, making them easier to test.

See the `tests` directory for examples of how to test the services by mocking the mojentic framework.