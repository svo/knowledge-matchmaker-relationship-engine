# Knowledge Matchmaker Relationship Engine

[![Build Builder](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/builder.yml/badge.svg)](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/builder.yml)
[![Build Development](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/development.yml/badge.svg)](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/development.yml)
[![Build Service](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/service.yml/badge.svg)](https://github.com/svo/knowledge-matchmaker-relationship-engine/actions/workflows/service.yml)

A production-ready Python service template implementing Hexagonal Architecture and Domain-Driven Design principles. This project provides a solid foundation for building maintainable, testable, and scalable microservices with FastAPI.

## Prerequisites

* `vagrant`: 2.4.3
* `ansible`: 2.18.3
* `colima`: 0.8.1
* `docker`: 28.0.2

## Quick Start

```bash
colima start --cpu 2 --memory 2 --vm-type=vz --mount-type=virtiofs --dns 8.8.8.8
vagrant up
vagrant provision
vagrant ssh
```

## Usage

### Run Application

```bash
./bin/run-local -c
```

### Run Tests

```bash
tox
```

Watch mode for development:

```bash
tox -e watch
```

### Format Code

```bash
tox -e format
```

### Lint Infrastructure

Shell scripts:
```bash
shellcheck -x ./*.sh bin/*
```

Ansible playbooks:
```bash
ansible-lint -p infrastructure/ansible/playbook-*.yml
```

## Architecture

This project follows **Hexagonal Architecture** (Ports and Adapters) combined with **Domain-Driven Design** principles:

- **Domain Layer**: Pure business logic and entities
- **Application Layer**: Use case orchestration
- **Infrastructure Layer**: Technical adapters (databases, APIs, message queues)
- **Interface Layer**: API controllers and external interfaces
- **Shared Layer**: Cross-cutting concerns (configuration, resilience patterns)

For comprehensive architectural rules, coding standards, testing requirements, and development guidelines, see [`.claude/CLAUDE.md`](.claude/CLAUDE.md).

## Key Features

- 100% test coverage requirement
- Dependency injection using Lagom
- Structured logging with correlation IDs
- Consumer-Driven Contract Testing (CDCT)
- Security scanning and static analysis
- Docker containerization
- Infrastructure as Code (Ansible, Terraform, Packer)

## Claude Code Skills

This project includes custom [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills to help with common development tasks. Use these slash commands in Claude Code:

| Command | Purpose |
|---------|---------|
| `/hexagonal-architecture-scaffolder` | Scaffold a new feature across all architecture layers |
| `/test-generator` | Generate tests following the one-assertion-per-test rule |
| `/self-documenting-refactor` | Refactor code to eliminate comments |
| `/property-based-testing` | Apply property-based testing patterns |
| `/sequential-thinking` | Break down complex problems into sequential reasoning steps |

These skills can also be triggered by natural language (e.g., "create a new feature", "generate tests for"). See [`.claude/skills/README.md`](.claude/skills/README.md) for full details.

## Contributing

When contributing to this project:

1. Review [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for detailed coding standards
2. Ensure all tests pass: `tox`
3. Format code before committing: `tox -e format`
4. Maintain 100% test coverage
5. Follow the one-assertion-per-test rule
6. Respect layer boundaries (see architectural documentation)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

The MIT License allows you to freely use, modify, and distribute this project in your own projects, including commercial applications, with minimal restrictions.
