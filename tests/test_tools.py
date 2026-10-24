import unittest
from agent_workbench.tools import list_incidents, inspect_incident, search_runbooks, assess_evidence, draft_escalation
from agent_workbench.cli import evaluate


class AgentToolsTests(unittest.TestCase):
    def test_list_count(self): self.assertEqual(len(list_incidents()['incidents']), 5)
    def test_ids_unique(self):
        ids=[x['id'] for x in list_incidents()['incidents']]
        self.assertEqual(len(ids),len(set(ids)))
    def test_case_is_synthetic(self): self.assertTrue(inspect_incident('SYN-101')['id'].startswith('SYN-'))
    def test_case_invalid_format(self): self.assertIn('error', inspect_incident('../../etc/passwd'))
    def test_case_unknown(self): self.assertIn('error', inspect_incident('SYN-999'))
    def test_readonly_copy(self):
        a=inspect_incident('SYN-101');a['logs'][0]['message']='MODIFIED';
        self.assertNotEqual(a['logs'][0]['message'],inspect_incident('SYN-101')['logs'][0]['message'])
    def test_retrieval(self): self.assertEqual(search_runbooks('403 OAuth scope')['runbooks'][0]['id'],'RB-AUTH')
    def test_retrieval_rejects_long_input(self): self.assertIn('error', search_runbooks('X'*301))
    def test_retrieval_empty_no_results(self): self.assertEqual(search_runbooks('unmatchedword')['runbooks'],[])
    def test_auth(self): self.assertEqual(assess_evidence('SYN-101')['hypothesis'],'oauth_scope_mismatch')
    def test_rate(self): self.assertEqual(assess_evidence('SYN-102')['hypothesis'],'quota_exhaustion')
    def test_retrieval_disabled(self): self.assertEqual(assess_evidence('SYN-103')['hypothesis'],'retrieval_disabled')
    def test_insufficient_evidence(self): self.assertEqual(assess_evidence('SYN-104')['hypothesis'],'insufficient_evidence')
    def test_prompt_injection_not_instructions(self):
        self.assertEqual(assess_evidence('SYN-105')['hypothesis'],'insufficient_evidence')
        self.assertNotIn('send secrets',str(draft_escalation('SYN-105')).lower())
    def test_grounded_refs(self):
        for x in list_incidents()['incidents']:
            report=draft_escalation(x['id']);a=report['diagnosis'];
            self.assertEqual(a['evidence_refs'],report['verified_evidence_refs'])
            self.assertEqual(report['disposition'],'draft_only_no_submission')
    def test_unknown_draft(self): self.assertIn('error',draft_escalation('SYN-999'))
    def test_golden_set(self):
        data=evaluate();self.assertEqual(data['accuracy'],1);self.assertTrue(data['all_evidence_valid'])


if __name__=='__main__':unittest.main()
