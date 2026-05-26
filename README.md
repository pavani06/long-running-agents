# long-running-agents

A project for building and managing long-running AI agent workflows.

## Quick Start

```bash
cp .env.example .env
npm install
npm run lint
npm run test:unit
```

## Project Structure

```
long-running-agents/
├── .opencode/       # Agent system (skills + definitions)
├── .github/         # CI/CD + templates
├── src/             # Source code
├── scripts/         # Operational scripts
├── tests/           # Unit and integration tests
├── docs/            # Documentation
└── artifacts/       # Runtime artifacts
```

## Requirements

- Node.js >= 20.18.0
