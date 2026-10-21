# REDMYTHOS CLAW 🦀

Open-source AI coding agent for Termux and Android — a lightweight, Gemini-powered alternative to Claude Code for mobile-first software workflows.

This repository has been hardened for safer local execution. The main changes include:

- workspace confinement for file and shell actions
- command allowlisting and removal of shell metacharacters
- public-only outbound URL validation to prevent SSRF-style abuse
- restricted tool auto-loading to approved modules only
- secure default workspace creation under `~/.redmythos/workspace`

## Security posture

The agent is now safer for prototype/local use, but it is still not a production-grade sandbox. For cloud or multi-user deployment, use:

- isolated execution containers or VMs
- authenticated tool execution API layers
- project-scoped workspaces with RBAC
- secret management via environment variables or a key manager
- audit logging and session tracing

## Cloud / Claude Code style architecture

A strong architecture for turning this prototype into a cloud-native coding agent looks like:

1. Client app or CLI
2. Backend orchestration service
3. Workspace manager per project
4. Sandbox runner (Docker/Kubernetes)
5. Tool registry and policy engine
6. Memory + state database
7. LLM orchestration and event streaming
8. PR/commit automation and CI integration

This approach keeps the local agent UX while moving risky execution into an isolated environment.

## Quick start

```bash
git clone https://github.com/pentrestion/redmythos-claw
cd redmythos-claw
bash install.sh
python3 main.py
```

## Notes

The project keeps a local workspace at `~/.redmythos/workspace` by default, and file or shell operations cannot escape that directory unless explicitly rewritten for a different policy.

## License

MIT

---

Built by Mir mahmood khan
