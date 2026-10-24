"""ADK wiring contract test using test doubles; does NOT claim SDK/cloud runtime validation."""
import importlib
import sys
import types
import unittest
from unittest.mock import patch


class AgentAdapterTests(unittest.TestCase):
    def test_agent_registration_contract(self):
        calls=[]
        class FakeLlmAgent:
            def __init__(self,**kw):self.fields=kw;calls.append(kw)
        google=types.ModuleType('google');google.__path__=[]
        adk=types.ModuleType('google.adk');adk.__path__=[]
        agents=types.ModuleType('google.adk.agents');agents.LlmAgent=FakeLlmAgent
        stubs={'google':google,'google.adk':adk,'google.adk.agents':agents}
        with patch.dict(sys.modules,stubs):
            try:
                module=importlib.import_module('incident_adk.agent')
                self.assertIsInstance(module.root_agent,FakeLlmAgent)
                self.assertEqual(len(calls[0]['tools']),5)
                self.assertTrue(all(callable(t) for t in calls[0]['tools']))
                self.assertIn('untrusted',calls[0]['instruction'])
            finally:
                for mod in ['incident_adk.agent','incident_adk']:
                    sys.modules.pop(mod,None)


if __name__=='__main__':unittest.main()
