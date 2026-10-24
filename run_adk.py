"""Optional real LLM/ADK demo. Requires google-adk and explicit model credentials."""
from __future__ import annotations
import asyncio
import os


async def main() -> None:
    if not (os.getenv('GOOGLE_API_KEY') or os.getenv('GOOGLE_GENAI_USE_VERTEXAI') == 'TRUE'):
        raise SystemExit('Configure GOOGLE_API_KEY, or Vertex AI ADC and GOOGLE_GENAI_USE_VERTEXAI=TRUE. Do not commit credentials.')
    try:
        from google.adk.apps import App
        from google.adk.runners import InMemoryRunner
        from google.genai import types
        from incident_adk.agent import root_agent
    except ImportError as exc:
        raise SystemExit('Install optional dependency: pip install -e ".[adk]"') from exc
    app = App(name='synthetic_incident_workbench', root_agent=root_agent)
    runner = InMemoryRunner(app=app)
    session = await runner.session_service.create_session(app_name=app.name, user_id='demo-user')
    message = types.Content(role='user', parts=[types.Part.from_text(text=(
        'Investigate SYN-101. Check supporting evidence and prepare a cited draft escalation. '
        'Use only read-only synthetic tools.'
    ))])
    async for event in runner.run_async(user_id='demo-user', session_id=session.id, new_message=message):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, 'text', None):
                    print(part.text)


if __name__ == '__main__':
    asyncio.run(main())
