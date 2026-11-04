"""Current production stays exact; the unwired active candidate stays strict."""
from pathlib import Path
import hashlib,importlib.util,os,unittest
from unittest.mock import patch
import yaml
ROOT=Path(__file__).resolve().parents[1]


class DormantIdentityTests(unittest.TestCase):
    def test_configuration_is_exact_dormant_or_exact_reviewed_small_stage2_activation(self):
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
        owner=['tools/library_research_hooks_candidate.py','tools/performance_assets.py','tools/library_research_freeze_styles_hook.py','tools/library_field_freeze_hook.py']
        if config['hooks']==owner:
            self._assert_exact_reviewed_owner_inputs()
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
        self.assertEqual('87ed18b5fb345535927804bdf60ac9aea4fbfbab4d2e99c3e189f1b87a4ed869',hashlib.sha256(raw).hexdigest())
        plan=json.loads(raw)
        self.assertEqual(1,plan['schema_version']);self.assertIs(plan['approved'],True)
        self.assertEqual(13269636938,plan['prior_artifact_id'])
        artifact_sha='05ff987007321fcd80bdbd0ba27b020f8628422849e26d36e92f54e9c12f6668'
        self.assertEqual(artifact_sha,plan['prior_artifact_sha256'])
        inputs=plan['inputs'];self.assertEqual(308,inputs['published_count'])
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
            'answers/fixes/how-should-i-use-robots-txt-to-control-ai-crawler-access.md',
            'answers/geo-basics/can-an-ai-answer-cite-a-company-without-naming-it.md',
            'answers/industries/why-is-my-dental-software-missing-from-ai-answers.md'}
        revisions=bound['active_revisions']
        self.assertIs(revisions['approved'],True)
        self.assertEqual(expected,set(revisions['pages']))
        self.assertTrue(all(r['payload']['meta']['library_cluster']==p.split('/')[1] for p,r in revisions['pages'].items()))
        self.assertEqual('c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c',inputs['files']['field_freeze_registry']['sha256'])
        frozen={row['source_path'] for row in bound['field_freeze_registry']['rows']}
        self.assertEqual(45,len(frozen));self.assertTrue(expected.isdisjoint(frozen))
        self.assertEqual(frozen,set(inputs['frozen_effective_pins']))
        expected_merges={
            'answers/industries/is-dentally-a-good-fit-for-uk-dentists-running-a-cloud-based-practice.md': 'answers/industries/why-is-my-dental-software-missing-from-ai-answers.md'}
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

    def _assert_exact_reviewed_owner_inputs(self):
        # This only admits the reviewed source-observation configuration to CI.
        # Final artifact/PDF/publication permission remains the Owner verifier's job.
        import json,re
        from pathlib import PurePosixPath,PureWindowsPath
        namespace=ROOT/'tools/library-owner-repair'
        policy='OWNER_RISK_VERIFY_REPAIR_2026_11_03_V1'
        artifact_sha='04b35fe2e233e95266c359094c6c242bfc58c4c1a7657d22da09dd827ba71d01'
        cat_sha='d7ac7a36caab1eb4277c010fd6527127101b75cc5f819faec9bd2778df525bfa'
        sha=lambda raw:hashlib.sha256(raw).hexdigest()
        def parsed(raw):
            def unique(pairs):
                result={}
                for key,value in pairs:
                    self.assertNotIn(key,result);result[key]=value
                return result
            return json.loads(raw,object_pairs_hook=unique)
        def safe(value):
            self.assertIsInstance(value,str)
            posix=PurePosixPath(value);windows=PureWindowsPath(value)
            self.assertTrue(value and '\\' not in value and not posix.is_absolute()
                            and not windows.is_absolute() and not windows.drive)
            self.assertNotIn('..',posix.parts);self.assertEqual(posix.as_posix(),value)
            self.assertFalse(any(c in value for c in ['\x00','?','#','%']))
            path=namespace.joinpath(*posix.parts)
            self.assertTrue(namespace.resolve().is_relative_to(ROOT.resolve()))
            self.assertTrue(path.resolve().is_relative_to(namespace.resolve()))
            for item in [path,*path.parents]:
                self.assertFalse(item.is_symlink(),str(item))
                self.assertFalse(getattr(item,'is_junction',lambda:False)(),str(item))
                if item==ROOT:break
            return path
        approval=parsed(safe('ROOT_BLUEPRINT_APPROVAL.json').read_bytes())
        self.assertEqual(1,approval['schema_version']);self.assertIs(approval['approved'],True)
        self.assertEqual('root',approval['reviewer'])
        self.assertEqual('root-reviewed-portable-owner-blueprint',approval['review_kind'])
        self.assertEqual({'id':13277324668,'sha256':artifact_sha},approval['prior_artifact'])
        read_sha=approval['actual_Root_read_record_sha256']
        self.assertRegex(read_sha,r'\A[0-9a-f]{64}\Z')
        self.assertEqual('tools/library-owner-repair/release.json',approval['blueprint']['path'])
        release_raw=safe('release.json').read_bytes()
        # The actual Root proof supplies the blueprint digest. Artifact review
        # may legitimately update it; no first-observation digest is hardcoded.
        self.assertEqual(approval['blueprint']['sha256'],sha(release_raw))
        release=parsed(release_raw)
        self.assertEqual(1,release['schema_version']);self.assertEqual(policy,release['policy'])
        self.assertEqual('root-exact-owner-repair-inputs',release['review_kind'])
        self.assertIs(release['approved'],True)
        declared=release['files'];self.assertIsInstance(declared,dict);self.assertTrue(declared)
        for name,pin in declared.items():
            self.assertRegex(pin,r'\A[0-9a-f]{64}\Z')
            self.assertEqual(pin,sha(safe(name).read_bytes()),name)
        self.assertEqual(read_sha,declared['ROOT_SOURCE_OBSERVATION_REVIEW.json'])
        read=parsed(safe('ROOT_SOURCE_OBSERVATION_REVIEW.json').read_bytes())
        self.assertIs(read['Root_source_observation_inputs_reviewed'],True)
        self.assertEqual((49,43,24,0,19),(read['source_changes'],read['nonPDF_sources'],read['answer_effective_revisions'],read['raw_answer_source_changes'],read['inherited_retirements']))
        self.assertIs(read['frozen45_excluded'],True);self.assertIs(read['Root_actual48_before_read_adjudication'],True)
        self.assertEqual('35ca9252c34c5c285bb35204a50dc0d8baa9657c54ec2daafae5451c3386d193',read['current307_producer_review_sha256'])
        self.assertEqual('f6b829f2b422aecde88d744181488f881b50c33d351b256e0a3b5db2cb18aa9f',read['Root_actual43_private_adoption_sha256'])
        def bound(row,parent=PurePosixPath('.')):
            self.assertIsInstance(row,dict);self.assertEqual({'path','sha256'},set(row))
            safe(row['path'])  # Reject absolute/traversal before combining bases.
            name=(parent/PurePosixPath(row['path'])).as_posix()
            self.assertEqual(row['sha256'],declared[name])
            data=safe(name).read_bytes();self.assertEqual(row['sha256'],sha(data))
            return parsed(data) if name.endswith('.json') else data
        def refs(value):
            # Only portable configuration references are walked. Historical
            # pointer metadata inside raw peer JSON is never followed.
            if isinstance(value,dict):
                if set(value)=={'path','sha256'}:bound(value)
                else:
                    for child in value.values():refs(child)
            elif isinstance(value,list):
                for child in value:refs(child)
        self.assertEqual({'path':'base/prior-artifact.zip','sha256':artifact_sha},release['prior_artifact'])
        config=bound(release['owner_inputs']);self.assertEqual(1,config['schema_version']);self.assertEqual(policy,config['policy'])
        refs(config)
        source_plan=bound(config['owner_source_plan'])
        self.assertEqual(config['owner_source_plan']['sha256'],config['owner_source_plan_sha256'])
        self.assertEqual(1,source_plan['schema_version']);self.assertEqual(policy,source_plan['kind'])
        self.assertEqual('root-exact-owner-repair-source-plan',source_plan['review_kind'])
        self.assertIs(source_plan['approved'],True);self.assertIs(source_plan['Root_actual_source_review_complete'],True)
        self.assertIs(source_plan['Source_rule4_relevance_inventory_complete'],True)
        self.assertEqual(cat_sha,source_plan['required28_catalog_sha256'])
        catalog_raw=(ROOT/'tools/library_owner_repair_required28.json').read_bytes()
        self.assertEqual(cat_sha,sha(catalog_raw))
        self.assertEqual('96fe2d21ffea3c7ea17547d2695ae5e90dade5f388af44375822821b469c4820',sha((ROOT/'tools/library_owner_repair_required28.py').read_bytes()))
        catalog=parsed(catalog_raw)
        samples={'docs/assets/samples/Kalvenor_Sample_Category_Audit.pdf','docs/assets/samples/Category_Audit_sample_Kalvenor_fictional.pdf',
                 'docs/assets/samples/FieldEdge_Category_Audit_v2.pdf','docs/assets/samples/Category_Audit_sample_FieldEdge_rehearsal.pdf',
                 'docs/assets/samples/WhiteLabel_Sample_Category_Audit_v2.pdf','docs/assets/samples/White_label_Category_Audit_sample.pdf'}
        nonPDF=set(catalog['required_owner_nonPDF_sources']);self.assertEqual(43,len(nonPDF))
        expected=nonPDF|samples;self.assertEqual(49,len(expected))
        changes=source_plan['source_changes'];self.assertEqual(expected,set(changes));self.assertEqual(expected,set(config['source_inputs']))
        self.assertEqual(307,source_plan['article_count']);self.assertEqual([],source_plan['retirements']);self.assertEqual([],source_plan['new_articles'])
        for path,row in config['source_inputs'].items():
            self.assertEqual(changes[path]['after_sha256'],row['after_source']['sha256'])
            if path in samples:self.assertEqual('sample_pdf',changes[path]['class'])
            else:self.assertNotEqual('sample_pdf',changes[path]['class'])
        authority=bound(config['authority_read_receipt'])
        self.assertEqual(('root','owner-brief-local-full-read',policy),(authority['reviewer'],authority['review_kind'],authority['policy']))
        self.assertEqual('e9e33b6921d4eb0b78550f556b314cab937509c6c120f74261d59c9073cf2e88',authority['authority_pdf_sha256'])
        self.assertEqual(5,authority['pages_actually_read']);self.assertIs(authority['actual_full_read_complete'],True);self.assertIs(authority['local_hash_verified'],True)
        self.assertEqual(config['authority_read_receipt']['sha256'],source_plan['authority_read_receipt_sha256'])
        before=bound(config['root_current_before_read_receipt'])
        self.assertEqual(('root','root-current-owner-repair-before-read',policy),(before['reviewer'],before['review_kind'],before['policy']));self.assertIs(before['approved'],True)
        self.assertEqual(config['root_current_before_read_receipt']['sha256'],source_plan['root_current_before_read_receipt_sha256'])
        self.assertEqual({p for p in expected if p.startswith('docs/')},set(before['sources']));self.assertEqual(48,len(before['sources']))
        for path,row in before['sources'].items():
            self.assertIs(row['actually_read'],True);self.assertIs(row['javascript_off_or_raw_source_read'],True)
            self.assertRegex(row['recorded_utc'],r'\A\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)\Z')
            self.assertRegex(row['public_before_sha256'],r'\A[0-9a-f]{64}\Z')
        base=bound(config['base_inputs']);base_dir=PurePosixPath(config['base_inputs']['path']).parent
        self.assertEqual(307,base['published_count']);self.assertEqual(config['base_inputs']['sha256'],source_plan['base_inputs_sha256'])
        binding={'commit_sha':'90f4a5dab5b8ad9883526d75426e45019f8f3547','deployment_id':'41742865044','artifact_sha256':artifact_sha,'served_receipt_sha256':'a5704131c98ef9a203319798bb58c7a0cb3fdebb6650be839c1e0fa89ff91c61'}
        for actual in [base['actual_prior_production_binding'],source_plan['baseline_production_binding'],before['production_binding']]:self.assertEqual(binding,actual)
        loaded={}
        for name,row in base['files'].items():
            if name=='prior_artifact':
                self.assertEqual({'path':'prior-artifact.zip','sha256':artifact_sha},row)
                continue
            loaded[name]=bound(row,base_dir)
        for row in base['receipt_files']:bound(row,base_dir)
        download=safe('base/prior-artifact.zip')
        if download.exists():self.assertEqual(artifact_sha,sha(download.read_bytes()))
        context=bound(config['post_s5_context'])
        self.assertIs(context['approved'],True);self.assertEqual('root',context['reviewer'])
        self.assertEqual('root-exact-post-small-S5-owner-context',context['review_kind'])
        self.assertEqual((307,326,19),(context['article_count'],context['raw_article_count'],context['inherited_stub_count']))
        self.assertEqual(binding,context['production_binding'])
        from library_owner_repair import digest as owner_digest
        self.assertEqual(source_plan['post_s5_context_sha256'],owner_digest(context))
        producer=loaded['production_receipt']
        self.assertEqual('8fff391f1079dec39c58930d7e06a14fb354d57f09828fd9590e0a74665396ce',base['files']['production_receipt']['sha256'])
        self.assertEqual(base['files']['production_receipt']['sha256'],context['production_receipt_sha256'])
        self.assertEqual('prior-production-effective-payload',producer['review_kind'])
        for key in ['approved','actual_served_readback','source_render_equality_passed','hub_source_render_equality_passed']:self.assertIs(producer[key],True)
        self.assertEqual(binding,producer['production_binding'])
        prior=loaded['prior_state'];self.assertEqual(binding,prior['production_binding'])
        self.assertEqual(326,len(prior['raw_source_pins']));self.assertEqual(19,len(prior['merged_sources']))
        self.assertEqual(307,len(loaded['prior_payload']['pages']));self.assertEqual(326,len(loaded['current_leaf_manifest']['pages']))
        self.assertEqual({},loaded['merges']['merges'])
        self.assertEqual('c346b0f6a7997449f4eccbaf662b53f7ae25ba21a57341f786dc7d673db1798c',base['files']['field_freeze_registry']['sha256'])
        frozen={r['source_path'] for r in loaded['field_freeze_registry']['rows']};self.assertEqual(45,len(frozen))
        self.assertEqual(frozen,set(base['frozen_effective_pins']))
        answer_changes={p[5:] for p in expected if p.startswith('docs/answers/')}
        self.assertEqual(24,len(answer_changes));self.assertTrue(answer_changes.isdisjoint(frozen))
        active=loaded['active_revisions'];self.assertIs(active['approved'],True);self.assertEqual(answer_changes,set(active['pages']))
        for path,row in active['pages'].items():self.assertEqual(changes['docs/'+path]['after_sha256'],row['after_effective_canonical_sha256'])


    def test_unwired_active_candidate_rejects_missing_pinned_inputs(self):
        path=ROOT/'tools/library_publication_hooks_candidate.py'
        spec=importlib.util.spec_from_file_location('_strict_unwired_candidate',path);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Independently pinned prepared library inputs'):
                candidate.on_pre_build({'docs_dir':str(ROOT/'docs'),'site_dir':str(ROOT/'site')})


if __name__=='__main__':unittest.main()
