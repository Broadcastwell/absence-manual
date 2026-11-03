import unittest
from tools.research_quality import check_closing_sections

LEGACY = "## Continue\n\n[Free check](https://audit.broadcastwell.com/)\n[Method](https://docs.broadcastwell.com/valid-measurement/)\n"
class ResearchClosingTests(unittest.TestCase):
    def errors(self, body, group='study'):
        errors=[]
        check_closing_sections(body, group, lambda ok,msg: None if ok else errors.append(msg))
        return errors
    def test_noncommercial_study_accepts_both_real_related_headings(self):
        for heading in ['Related reading','Related studies']:
            self.assertEqual([],self.errors('## '+heading+'\n[Method](https://docs.broadcastwell.com/valid-measurement/)'))
    def test_noncommercial_study_requires_real_related_heading(self):
        self.assertIn('noncommercial related reading missing',self.errors('## Sources\nNo related section.'))
        self.assertIn('noncommercial related reading missing',self.errors('```md\n## Related reading\n```'))
    def test_noncommercial_study_rejects_audit_urls_in_each_supported_form(self):
        for url in ['https://audit.broadcastwell.com/','https://audit.broadcastwell.com','https://audit.broadcastwell.com?x=1','HTTP://AUDIT.BROADCASTWELL.COM/','//audit.broadcastwell.com/']:
            self.assertIn('study body must not include a promotional audit link',self.errors('## Related studies\n[Check]('+url+')'))
    def test_noncommercial_study_allows_unrelated_source_host(self):
        self.assertEqual([],self.errors('## Related reading\n[Source](https://example.org/audit/)'))
    def test_legacy_study_migration_retains_exact_existing_two_link_rule(self):
        self.assertEqual([],self.errors(LEGACY))
        self.assertTrue(self.errors(LEGACY+'[Third](https://example.org/)'))
    def test_nonstudy_still_requires_continue_and_original_link_order(self):
        for group in ['insight','source','glossary','playbook','hub']:
            self.assertEqual([],self.errors(LEGACY,group))
            self.assertIn('Continue missing',self.errors('## Related studies\n[Method](https://docs.broadcastwell.com/valid-measurement/)',group))
            self.assertTrue(self.errors('## Continue\n[Method](https://docs.broadcastwell.com/valid-measurement/)\n[Check](https://audit.broadcastwell.com/)',group))
if __name__=='__main__':unittest.main()
