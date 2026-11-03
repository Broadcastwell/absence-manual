"""Current production stays exact; the unwired active candidate stays strict."""
from pathlib import Path
import hashlib,importlib.util,os,unittest
from unittest.mock import patch
import yaml
ROOT=Path(__file__).resolve().parents[1]


class DormantIdentityTests(unittest.TestCase):
    def test_configuration_is_exact_dormant_or_exact_reviewed_coherent20_18_activation(self):
        # The code-only historical phase remains a supported exact configuration.
        # The active phase requires this finite Root-reviewed release, never a
        # catch/fallback to raw rendering or an arbitrary approved input folder.
        import json
        from pathlib import PurePosixPath, PureWindowsPath
        config=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
        dormant=['tools/hooks.py','tools/performance_assets.py','tools/library_field_freeze_hook.py']
        active=['tools/library_publication_hooks_candidate.py','tools/performance_assets.py','tools/library_field_freeze_hook.py']
        self.assertNotIn('from_environment',(ROOT/'tools/hooks.py').read_text())
        self.assertFalse((ROOT/'tools/library_publication_release.json').exists())
        self.assertFalse((ROOT/'tools/library_publication_inputs').exists())
        if config['hooks']==dormant:
            self.assertNotIn('tools/library_publication_hooks_candidate.py',config['hooks'])
            return
        self.assertEqual(active,config['hooks'])
        namespace=ROOT/'tools/library-publication'
        root=ROOT.resolve()
        def safe_local(value):
            self.assertIsInstance(value,str)
            posix=PurePosixPath(value);windows=PureWindowsPath(value)
            self.assertTrue(value and '\\' not in value and not posix.is_absolute()
                            and not windows.is_absolute() and not windows.drive)
            self.assertNotIn('..',posix.parts)
            self.assertEqual(posix.as_posix(),value)
            path=namespace.joinpath(*posix.parts)
            self.assertTrue(path.resolve().is_relative_to(namespace.resolve()))
            self.assertTrue(namespace.resolve().is_relative_to(root))
            for location in [path,*path.parents]:
                self.assertFalse(location.is_symlink(),str(location))
                self.assertFalse(getattr(location,'is_junction',lambda:False)(),str(location))
                if location==ROOT:break
            return path
        release=safe_local('release.json');raw=release.read_bytes()
        self.assertEqual('6a6bf041d88eba42d94b62a3b8c25eb41d4b01365f4d0f21d8302a5dc881191f',hashlib.sha256(raw).hexdigest())
        plan=json.loads(raw)
        self.assertEqual(1,plan['schema_version']);self.assertIs(plan['approved'],True)
        self.assertEqual(13241535906,plan['prior_artifact_id'])
        artifact_sha='a28ad4251756e7da2440b4756d54baf9f350e66ef7264171593d894b2e10a99a'
        self.assertEqual(artifact_sha,plan['prior_artifact_sha256'])
        inputs=plan['inputs'];self.assertEqual(326,inputs['published_count'])
        self.assertEqual(artifact_sha,inputs['actual_prior_production_binding']['artifact_sha256'])
        bound={}
        for name,row in inputs['files'].items():
            path=safe_local(row['path'])
            if name=='prior_artifact':
                # This is deliberately not a committed ZIP. The owning CI
                # downloader and stage require its actual ID/digest/bytes.
                self.assertEqual('PRIOR_ARTIFACT_DOWNLOAD_REQUIRED.zip',row['path'])
                self.assertEqual(artifact_sha,row['sha256'])
                continue
            self.assertTrue(path.is_file(),str(path))
            self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest(),name)
            if path.suffix=='.json':bound[name]=json.loads(path.read_text(encoding='utf-8'))
        for row in inputs['receipt_files']:
            path=safe_local(row['path']);self.assertTrue(path.is_file(),str(path))
            self.assertEqual(row['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
        downloaded=ROOT/'reviewed-prior-publication.zip'
        if downloaded.exists():
            self.assertFalse(downloaded.is_symlink())
            self.assertEqual(artifact_sha,hashlib.sha256(downloaded.read_bytes()).hexdigest())
        expected={
            'answers/agents/does-an-ai-handoff-mean-a-software-purchase-was-completed.md',
            'answers/agents/how-does-an-ai-connector-differ-from-browsing-a-website.md',
            'answers/buying/how-does-omniscient-digital-compare-as-a-geo-agency.md',
            'answers/buying/what-evidence-should-an-ai-factual-accuracy-alert-include.md',
            'answers/changes/what-should-we-check-when-an-ai-answer-gets-a-fact-wrong.md',
            'answers/chatgpt/which-dental-software-does-chatgpt-recommend.md',
            'answers/chatgpt/which-field-service-software-does-chatgpt-recommend.md',
            'answers/chatgpt/which-insurance-agency-software-does-chatgpt-recommend.md',
            'answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md',
            'answers/chatgpt/which-transportation-software-does-chatgpt-recommend.md',
            'answers/fixes/how-should-i-turn-a-measured-buyer-question-into-an-answer-page.md',
            'answers/fixes/how-should-i-use-robots-txt-to-control-ai-crawler-access.md',
            'answers/geo-basics/can-an-ai-answer-cite-a-company-without-naming-it.md',
            'answers/geo-basics/how-does-chatgpt-relate-to-seo.md',
            'answers/geo-basics/which-review-sites-for-geo-should-a-buyer-compare.md',
            'answers/google-ai/how-do-google-ai-overviews-affect-website-visibility.md',
            'answers/google-ai/what-is-a-google-ai-overview.md',
            'answers/google-ai/what-is-google-ai-mode.md',
            'answers/measurement/how-do-suede-profound-and-athenahq-differ-in-sampling-ai-answers-and-m.md',
            'answers/measurement/what-evidence-can-connect-ai-visibility-with-pipeline.md'}
        revisions=bound['active_revisions']
        self.assertIs(revisions['approved'],True)
        self.assertEqual(expected,set(revisions['pages']))
        self.assertTrue(all(r['payload']['meta']['library_cluster']==p.split('/')[1] for p,r in revisions['pages'].items()))
        self.assertEqual('c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c',inputs['files']['field_freeze_registry']['sha256'])
        frozen={row['source_path'] for row in bound['field_freeze_registry']['rows']}
        self.assertEqual(45,len(frozen));self.assertTrue(expected.isdisjoint(frozen))
        self.assertEqual(frozen,set(inputs['frozen_effective_pins']))
        expected_merges={
            'answers/buying/looking-for-ai-software-for-field-service-providers-in-the-united-king.md': 'answers/chatgpt/which-field-service-software-does-chatgpt-recommend.md',
            'answers/buying/what-should-i-ask-a-geo-provider-about-mcp-or-api-access.md': 'answers/agents/how-does-an-ai-connector-differ-from-browsing-a-website.md',
            'answers/buying/which-aeo-tools-suit-home-service-companies-and-contractors.md': 'answers/chatgpt/which-field-service-software-does-chatgpt-recommend.md',
            'answers/fixes/how-can-a-local-auto-glass-business-appear-in-google-ai-and-chatgpt-an.md': 'answers/geo-basics/can-an-ai-answer-cite-a-company-without-naming-it.md',
            'answers/fixes/how-should-a-local-business-respond-when-chatgpt-cites-ranking-list-pa.md': 'answers/geo-basics/which-review-sites-for-geo-should-a-buyer-compare.md',
            'answers/fixes/what-do-ai-crawlers-do-and-how-can-site-owners-control-access.md': 'answers/fixes/how-should-i-use-robots-txt-to-control-ai-crawler-access.md',
            'answers/fixes/which-ai-tools-can-support-programmatic-seo.md': 'answers/fixes/how-should-i-turn-a-measured-buyer-question-into-an-answer-page.md',
            'answers/geo-basics/chatgpt-brand-visibility-cost.md': 'answers/measurement/how-do-suede-profound-and-athenahq-differ-in-sampling-ai-answers-and-m.md',
            'answers/geo-basics/how-do-getmint-and-otterly-compare-for-transactional-geo-in-the-united.md': 'answers/agents/does-an-ai-handoff-mean-a-software-purchase-was-completed.md',
            'answers/geo-basics/where-can-i-find-an-ai-search-visibility-expert-near-me.md': 'answers/buying/how-does-omniscient-digital-compare-as-a-geo-agency.md',
            'answers/geo-basics/which-ai-is-best-for-seo.md': 'answers/geo-basics/how-does-chatgpt-relate-to-seo.md',
            'answers/geo-basics/which-ai-tools-for-analyzing-online-visibility-are-available-in-the-uk.md': 'answers/measurement/how-do-suede-profound-and-athenahq-differ-in-sampling-ai-answers-and-m.md',
            'answers/google-ai/are-google-ai-overviews-available-in-france.md': 'answers/google-ai/what-is-a-google-ai-overview.md',
            'answers/google-ai/can-ads-appear-in-google-ai-overviews.md': 'answers/google-ai/what-is-a-google-ai-overview.md',
            'answers/measurement/how-accurate-are-geo-tools-across-different-industries.md': 'answers/buying/what-evidence-should-an-ai-factual-accuracy-alert-include.md',
            'answers/measurement/how-can-i-defend-branded-search-results-against-lookalike-sites-that-c.md': 'answers/changes/what-should-we-check-when-an-ai-answer-gets-a-fact-wrong.md',
            'answers/measurement/how-do-ads-in-google-ai-overviews-affect-organic-traffic.md': 'answers/google-ai/how-do-google-ai-overviews-affect-website-visibility.md',
            'answers/measurement/how-would-you-optimize-an-e-commerce-product-page-for-google-and-ai-se.md': 'answers/fixes/how-should-i-turn-a-measured-buyer-question-into-an-answer-page.md'}
        self.assertIs(bound['merges']['approved'],True)
        self.assertEqual(expected_merges,{p:r['target_path'] for p,r in bound['merges']['merges'].items()})
        self.assertTrue(frozen.isdisjoint(expected_merges))
        self.assertTrue(frozen.isdisjoint(expected_merges.values()))
        self.assertTrue(set(expected_merges.values()).issubset(expected))
        self.assertEqual(expected | set(expected_merges),set(bound['authorized_changes']['pages']))
        for source,target in expected_merges.items():
            self.assertEqual('MERGED_CANONICAL_STUB',bound['authorized_changes']['pages'][source]['status'])
            self.assertEqual(target,bound['authorized_changes']['pages'][source]['target_path'])
            self.assertEqual(bound['merges']['merges'][source]['decision_receipt_sha256'],bound['authorized_changes']['pages'][source]['decision_receipt_sha256'])

    def test_unwired_active_candidate_rejects_missing_pinned_inputs(self):
        path=ROOT/'tools/library_publication_hooks_candidate.py'
        spec=importlib.util.spec_from_file_location('_strict_unwired_candidate',path);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Independently pinned prepared library inputs'):
                candidate.on_pre_build({'docs_dir':str(ROOT/'docs'),'site_dir':str(ROOT/'site')})


if __name__=='__main__':unittest.main()
