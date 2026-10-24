# Google ADK Agent Workbench

A **real Google Agent Development Kit (`LlmAgent`) integration** wired to five strictly **read-only tools** for synthetic GenAI incident investigation. Its deterministic domain layer can be tested offline without a model or Google Cloud account. Optional end-to-end LLM execution requires installing Google ADK and providing your own credentials.

## Architecture

```text
ADK LlmAgent (Gemini; optional live path)
  ├─ list_incidents       synthetic-only inventory
  ├─ inspect_incident     limited non-secret observations
  ├─ search_runbooks      local lexical retrieval
  ├─ assess_evidence      corroboration-required hypothesis
  └─ draft_escalation     cited DRAFT; never submits
        |
        +-- agent_workbench/tools.py (standard-library; offline tests)
```

Unlike a deterministic *agent simulation*, `incident_adk/agent.py` instantiates Google's `LlmAgent`, binds native function tools, and can run through ADK's `App` and `InMemoryRunner`. This is a reference implementation, not a production support product.

## Run offline (Python 3.11+; no dependencies)

```bash
python -m agent_workbench.cli --case SYN-101
python -m agent_workbench.cli --evaluate
python -m unittest discover -s tests -v
```

Includes five synthetic cases: missing OAuth scopes (403), tool burst quota saturation (429), disabled retrieval, insufficient latency evidence, and prompt-injection text embedded in a fake log. Reported test accuracy is over these **five intentionally simple synthetic cases only**.

## Run through Google ADK (optional, actual model calls)

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\\Scripts\\activate
pip install -e '.[adk]'
export GOOGLE_API_KEY='...'           # Windows: set GOOGLE_API_KEY=...
python run_adk.py
```

`run_adk.py` creates an `App`, `InMemoryRunner`, local demo session, and passes a synthetic user request to the agent. Alternatively, the `incident_adk` package defines the standard `root_agent` entry point for local ADK tools. The optional live path has **not** been exercised by CI and may make billable Gemini API calls. SDK integration should be revalidated locally after dependency upgrades.

## Safety and evaluation

- All case IDs, telemetry, access flags, and runbooks are fabricated. No employer, customer, or private incident data.
- No network or write tools are exposed to the agent. Model inference itself communicates with the configured provider only when you explicitly run the optional path.
- Log content is untrusted; the agent instructions prohibit following instructions found in logs. **Prompt injection is not provably prevented by instructions alone.**
- Escalation packets carry evidence references and `draft_only_no_submission`; no tickets are created.
- Tests assert tool behavior and **mocked ADK wiring**, not a deployed ADK system or real-model safety guarantees.

## Reference

Google ADK primary `LlmAgent` docs: https://github.com/google/adk-python/blob/main/docs/guides/agents/llm_agent/index.md
