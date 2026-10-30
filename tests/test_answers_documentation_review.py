"""Fictional source-rule fixtures; none is a page or a product test."""
import copy,json
from pathlib import Path
import tempfile,unittest
from tools.library_answers import validate_source_evidence
from tools.library_documentation_review import (
    DOC_REVIEW_SOURCE,DOC_REVIEW_METHOD_LABEL,DOC_REVIEW_RECEIPT_PATH,
    DOC_REVIEW_RECEIPT_URL,DOC_REVIEW_RECORD_ID,DOC_REVIEW_FIELD_DATE,
    DOC_REVIEW_SNAPSHOT_SHA256,DOC_REVIEW_RECEIPT_SHA256,
    DOC_REVIEW_EXPECTED_RECEIPT,DOC_REVIEW_FACT_KEY,
)
from tools.library_quality import figure_key

class DocumentationReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.docs=Path(self.temp.name)
        self.asset=self.docs/DOC_REVIEW_RECEIPT_PATH;self.asset.parent.mkdir(parents=True)
        self.asset.write_text(json.dumps(DOC_REVIEW_EXPECTED_RECEIPT),encoding='utf8')
        self.meta={'evidence_kind':'published-documentation-review','is_based_on':DOC_REVIEW_SOURCE,'evidence_documentation_record':DOC_REVIEW_RECORD_ID,'evidence_documentation_field_date':DOC_REVIEW_FIELD_DATE,'evidence_documentation_snapshot_sha256':DOC_REVIEW_SNAPSHOT_SHA256,'evidence_documentation_receipt_sha256':DOC_REVIEW_RECEIPT_SHA256}
        self.body='''# Fictional source-rule fixture

Our 17 September 2026 publication record names three MCP-access plan labels for OtterlyAI. This fixture is not published.

## What we measured

**Measured publication record.** We counted named plans in [the dated public documentation review]('''+DOC_REVIEW_SOURCE+'''). The [pinned record receipt]('''+DOC_REVIEW_RECEIPT_URL+''') retains the source and field date.

| Field | Published value |
| --- | --- |
| MCP connector | Yes |
| MCP plans | Standard, Premium and Enterprise; not Lite |
| Official API | Yes |
| API plans | Standard, Premium and Enterprise; not Lite |
| Record date | 17 September 2026 |

The count is a published documentation record, not an executed integration or a security audit.

## What this means for you

This fictional fixture exercises only the source validator.

## Next step

The normal purchase block is tested by the unchanged answer rules.

['''+DOC_REVIEW_METHOD_LABEL+''']('''+DOC_REVIEW_SOURCE+''')
'''
    def errors(self,meta=None,body=None):
        return validate_source_evidence(meta or self.meta,body or self.body,self.docs)[0]
    def reject_body(self,text):
        body=self.body.replace('## What this means for you',text+'\n\n## What this means for you')
        self.assertTrue(self.errors(body=body),text)
    def test_exact_pinned_publication_passes(self):self.assertEqual(self.errors(),[])
    def test_two_distinct_scope_wordings_pass(self):
        text='We counted plan names in public documentation. No account was tested, and the count supplies no compliance assurance.'
        body=self.body.replace('The count is a published documentation record, not an executed integration or a security audit.',text)
        self.assertEqual(self.errors(body=body),[])
    def test_fact_identity_is_the_existing_semantic_proposal(self):self.assertEqual(figure_key(DOC_REVIEW_EXPECTED_RECEIPT['lead_fact']),DOC_REVIEW_FACT_KEY)
    def test_arbitrary_source_is_rejected(self):
        m=dict(self.meta,is_based_on='https://example.test/fictional-review');self.assertTrue(self.errors(meta=m))
    def test_unapproved_record_is_rejected(self):
        m=dict(self.meta,evidence_documentation_record='fictional-provider');self.assertTrue(self.errors(meta=m))
    def test_wrong_field_date_is_rejected(self):
        m=dict(self.meta,evidence_documentation_field_date='2026-10-29');self.assertTrue(self.errors(meta=m))
    def test_wrong_snapshot_is_rejected(self):
        m=dict(self.meta,evidence_documentation_snapshot_sha256='0'*64);self.assertTrue(self.errors(meta=m))
    def test_wrong_receipt_hash_is_rejected(self):
        m=dict(self.meta,evidence_documentation_receipt_sha256='0'*64);self.assertTrue(self.errors(meta=m))
    def test_changed_plan_in_asset_is_rejected(self):
        d=copy.deepcopy(DOC_REVIEW_EXPECTED_RECEIPT);d['record']['MCP_plan_labels'].append('Lite');self.asset.write_text(json.dumps(d),encoding='utf8');self.assertTrue(self.errors())
    def test_changed_count_in_asset_is_rejected(self):
        d=copy.deepcopy(DOC_REVIEW_EXPECTED_RECEIPT);d['lead_fact']['count']=4;self.asset.write_text(json.dumps(d),encoding='utf8');self.assertTrue(self.errors())
    def test_duplicate_receipt_key_is_rejected(self):
        self.asset.write_text('{"source_url":"x","source_url":"y"}',encoding='utf8');self.assertTrue(self.errors())
    def test_missing_receipt_is_rejected(self):self.asset.unlink();self.assertTrue(self.errors())
    def test_wrong_visible_plan_table_is_rejected(self):self.assertTrue(self.errors(body=self.body.replace('Standard, Premium and Enterprise; not Lite','Standard, Premium, Enterprise and Lite',1)))
    def test_wrong_visible_count_is_rejected(self):self.assertTrue(self.errors(body=self.body.replace('three MCP-access plan labels','four MCP-access plan labels')))
    def test_wrong_first_unit_is_rejected(self):self.assertTrue(self.errors(body=self.body.replace('three MCP-access plan labels','three MCP providers')))
    def test_missing_execution_and_assurance_limit_is_rejected(self):self.assertTrue(self.errors(body=self.body.replace('The count is a published documentation record, not an executed integration or a security audit.','The record is a published page.')))
    def test_execution_claim_is_rejected(self):self.reject_body('We executed the MCP connector in this review.')
    def test_passive_execution_is_rejected(self):self.reject_body('The MCP connector was tested successfully.')
    def test_unrelated_negation_cannot_hide_passive_execution(self):self.reject_body('The MCP connector is not anonymous and was tested successfully.')
    def test_truthful_direct_no_execution_passes(self):
        body=self.body.replace('## What this means for you','The MCP connector was not tested.\n\n## What this means for you')
        self.assertEqual(self.errors(body=body),[])
    def test_compliance_proof_is_rejected(self):self.reject_body('Our review proves GDPR compliance.')
    def test_unrelated_negation_cannot_hide_execution(self):self.reject_body('Our review is not anonymous and verified API execution.')
    def test_unrelated_negation_cannot_hide_compliance(self):self.reject_body('Our review is not anonymous and proves compliance.')
    def test_three_plans_do_not_become_certified(self):self.reject_body('The three plans are certified.')
    def test_qualified_plan_assurance_is_rejected(self):
        for label in ['SOC2 Type II','ISO27001']:
            with self.subTest(label=label):self.reject_body('The three plans are '+label+' certified.')
    def test_unrelated_negation_cannot_hide_qualified_assurance(self):
        for label in ['SOC2 Type II','ISO27001']:
            with self.subTest(label=label):self.reject_body('The three plans are not anonymous and are '+label+' certified.')
    def test_direct_qualified_plan_negation_passes(self):
        for label in ['SOC2 Type II','ISO27001']:
            with self.subTest(label=label):
                body=self.body.replace('## What this means for you','The three plans are not '+label+' certified.\n\n## What this means for you')
                self.assertEqual(self.errors(body=body),[])
    def test_lite_positive_access_is_rejected(self):self.reject_body('OtterlyAI MCP access is available on Lite.')
    def test_standard_sso_is_rejected(self):self.reject_body('OtterlyAI Standard includes SSO.')
    def test_audit_roadmap_cannot_be_completed(self):self.reject_body('OtterlyAI SOC2 Type II audit is complete.')
    def test_unrelated_negation_cannot_hide_completed_audit(self):self.reject_body('OtterlyAI is not anonymous and its SOC2 Type II audit is complete.')
    def test_truthful_direct_negative_claims_pass(self):
        text='Our review does not prove compliance. OtterlyAI is not SOC2 Type II compliant. OtterlyAI MCP access is not available on Lite. OtterlyAI Standard does not include SSO.'
        body=self.body.replace('## What this means for you',text+'\n\n## What this means for you')
        self.assertEqual(self.errors(body=body),[])
    def test_reported_other_provider_claim_is_not_blocked(self):
        body=self.body.replace('## What this means for you','Profound reports SOC2 Type II compliance and SAML or OIDC sign-in.\n\n## What this means for you')
        self.assertEqual(self.errors(body=body),[])
    def test_provider_price_claim_is_rejected(self):self.reject_body('OtterlyAI costs $123 a month.')
    def test_old_universal_method_is_rejected(self):self.assertTrue(self.errors(body=self.body+'\nEvery figure comes from the published method, v1.1.'))
    def test_missing_source_receipt_link_is_rejected(self):self.assertTrue(self.errors(body=self.body.replace(DOC_REVIEW_RECEIPT_URL,'https://example.test/fictional-receipt')))
    def test_doi_method_metadata_is_rejected(self):
        m=dict(self.meta,evidence_method_receipts=['https://doi.org/10.5281/zenodo.22907695']);self.assertTrue(self.errors(meta=m))
    def test_unrelated_audit_metadata_is_rejected(self):
        m=dict(self.meta,evidence_audit_records=['fictional-agency']);self.assertTrue(self.errors(meta=m))

if __name__=='__main__':unittest.main()
