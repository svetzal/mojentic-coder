# Mojentic Coder

Agentic coding has become a fairly popular phenomenon in the software industry. The challenge is that it tends to be misapplied. The bottleneck in software development is not the developer's ability to type code, but rather in deciding what to build and when to build software that can satisfy the objective of its users and stakeholders.

Working with agents is like working with a team of brand new developers. They generally know how to code, but they each code in their own direction, which is seldom in alignment with the intent and vision of the developer in charge.

This UI is an attempt to build a multi-agent software engineering environment, which puts the developer in charge of the vision and direction of the project, while the agents take care of the toil in putting it together.

## Epic 1: Agent Management

- [ ] Upon launch, the tool opens a full-size window with three blank panels

- [ ] Agents can be defined in the left-hand panel
  - Agents have a Gateway (OpenAI or Ollama), a Model (the list of models is retrieved via the chosen gateway), and a system prompt that defines their character and behaviour

- [ ] When an Agent is created, a Chat Session is created with the agent, which is displayed in the middle panel.

- [ ] When an Agent is created, the user can type a message in the bottom of the middle panel, which is sent to the agent's Chat Session.
