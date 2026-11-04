import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,copy,json,tempfile,unittest,shutil
O=Path(__file__).resolve().parents[1];sys.path.insert(0,str(O/'tools'));sys.path.insert(0,str(Path(__file__).resolve().parent))
import owner_surface_support as harness

class ExactSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prior_modules=dict(sys.modules);cls.prior_path=list(sys.path)
        cls.env,parser=harness.load_comparators();cls.cases,_=harness.actual_cases(parser);cls.by={c['path']:c for c in cls.cases}
    def answer(self):return copy.deepcopy(next(c for c in self.cases if c['path'].startswith('answers/buying/')))
    def legal(self):return copy.deepcopy(self.by['answers/chatgpt/which-legal-practice-software-does-chatgpt-recommend.md'])
    def research(self):return copy.deepcopy(self.by['research/glossary/citation-decay/index.md'])
    def check(self,c):return self.env['validate_content_surface'](c['path'],c['before_record'],c['after_record'],c['context'],c['before'],c['after'])
    def change(self,c,a,b):
        self.assertIn(a,c['after']);c['after']=c['after'].replace(a,b,1);return c
    def test_actual_seven_and_final_navigation_caller(self):
        proofs={}
        for c in self.cases:
            self.env['validate_render_context'](c['path'],c['after_record'],c['context'],c['after'])
            proofs[self.env['public_url'](c['path'])+'index.html']=self.check(c)
        self.assertTrue(harness.final_navigation_loop(self.env,self.cases,proofs))
    def test_toc_title_tamper(self):
        c=self.change(self.legal(),b'      Watch the legal-software summary\n',b'      Invented summary\n')
        with self.assertRaises(ValueError):self.check(c)
    def test_toc_foreign_href(self):
        c=self.change(self.legal(),b'href="#watch-the-legal-software-summary"',b'href="https://example.com/"')
        with self.assertRaises(ValueError):self.check(c)
    def test_wrong_footer_date(self):
        c=self.change(self.answer(),b'<time datetime="2026-11-04">4 November 2026</time>',b'<time datetime="2026-11-05">5 November 2026</time>')
        with self.assertRaises(ValueError):self.check(c)
    def test_footer_time_extra_attribute(self):
        c=self.change(self.answer(),b'<time datetime="2026-11-04">',b'<time datetime="2026-11-04" data-extra="x">')
        with self.assertRaises(ValueError):self.check(c)
    def test_research_footer_date(self):
        c=self.change(self.research(),b'<time datetime="2026-11-04">2026-11-04</time>',b'<time datetime="2026-11-03">2026-11-03</time>')
        with self.assertRaises(ValueError):self.check(c)
    def test_footer_commercial_fact(self):
        c=self.change(self.answer(),b'Answer Repair, $490',b'Answer Repair, $1')
        with self.assertRaises(ValueError):self.check(c)
    def test_footer_unrelated_link(self):
        c=self.change(self.answer(),b'href="https://broadcastwell.com/privacy"',b'href="https://example.com/privacy"')
        with self.assertRaises(ValueError):self.check(c)
    def test_skip_wrong_heading(self):
        c=self.change(self.legal(),b'href="#which-legal-practice-software-does-chatgpt-recommend" class="md-skip"',b'href="#wrong-heading" class="md-skip"')
        with self.assertRaises(ValueError):self.check(c)
    def test_legacy_resource_title_is_exact_template_not_arbitrary_whitespace(self):
        c=copy.deepcopy(self.by['resources/audit/sample.md'])
        c['before']=c['before'].replace(b'<title>Synthetic Category Audit , Northstar Lab |',b'<title>Synthetic Category Audit ,  Northstar Lab |',1)
        with self.assertRaises(ValueError):self.check(c)
    def test_research_wrong_fallback_headline(self):
        c=self.change(self.research(),b'"headline": "What is citation decay?"',b'"headline": "Other"')
        with self.assertRaises(ValueError):self.check(c)
    def test_unrelated_script(self):
        c=self.change(self.answer(),b'window.setTimeout(function ()',b'window.setInterval(function ()')
        with self.assertRaises(ValueError):self.check(c)
    def test_changed_complete_source_fails_render(self):
        c=self.answer();c['after_record']['body']+='\nA foreign scientific claim.\n'
        with self.assertRaises(ValueError):self.check(c)
    def test_final_caller_rejects_tampered_nav_even_with_new_HTML_hash(self):
        c=self.legal();p=self.check(c);c=self.change(c,b'aria-label="Broadcastwell"',b'aria-label="Forged"')
        # Primary-global header is outside strict primary. Use actual primary href.
        c['after']=c['after'].replace(b'href="../../../selection-not-ranking/"',b'href="../../../foreign/"',1)
        if b'../../../foreign/' not in c['after']:
            c['after']=c['after'].replace(b'id="__nav_1"',b'id="__nav_forged"',1)
        self.assertNotEqual(c['after'],self.by[c['path']]['after'])
        p['source_navigation']['after_html_sha256']=harness.sha(c['after'])
        with self.assertRaises(ValueError):harness.final_navigation_loop(self.env,[c],{self.env['public_url'](c['path'])+'index.html':p})
    def test_final_caller_rejects_foreign_source(self):
        c=self.legal();p=self.check(c);p['source_navigation']['after_full_source']+='\nforeign\n'
        with self.assertRaises(ValueError):harness.final_navigation_loop(self.env,[c],{self.env['public_url'](c['path'])+'index.html':p})
    def test_final_caller_rejects_stale_HTML_hash(self):
        c=self.legal();p=self.check(c);p['source_navigation']['after_html_sha256']='0'*64
        with self.assertRaises(ValueError):harness.final_navigation_loop(self.env,[c],{self.env['public_url'](c['path'])+'index.html':p})
    def test_template_drift_rejected(self):
        import library_owner_repair_surface as s
        work=O/'test-work';work.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=work) as d:
            r=Path(d)
            for f in ['mkdocs.yml','overrides/main.html','overrides/partials/site-footer.html']:
                q=r/f;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((harness.R/f).read_bytes())
            f=r/'overrides/partials/site-footer.html';f.write_bytes(f.read_bytes()+b'foreign')
            c=self.answer()
            with self.assertRaises(ValueError):s.project_source_template_slots(c['path'],c['after_record'],c['after'],template_root=r)
    def test_navigation_only_function_AST_unchanged(self):
        def node(p):return next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='validate_navigation_only')
        import hashlib
        self.assertEqual(hashlib.sha256(ast.dump(node(harness.PROPOSED/'library_owner_repair.py')).encode()).hexdigest(),'c42d1a500d84a6b82d51b9e5b8fe742f41ac09940a2f32344598a3308558b92c')
    def test_support_preserves_preexisting_modules_and_path(self):
        self.assertEqual(self.prior_path,sys.path)
        self.assertTrue(all(sys.modules.get(k) is v for k,v in self.prior_modules.items()))
    def test_material_override_shadow_rejected(self):
        import library_owner_repair_surface as s
        import material
        work=O/'test-work';work.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=work) as d:
            r=Path(d)
            for f in ['mkdocs.yml','overrides/main.html','overrides/partials/site-footer.html']:
                q=r/f;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((harness.R/f).read_bytes())
            q=r/'overrides/partials/toc.html'
            q.write_bytes((Path(material.__file__).parent/'templates/partials/toc.html').read_bytes()+b'foreign shadow')
            c=self.answer()
            with self.assertRaisesRegex(ValueError,'Override shadows'):
                s.project_source_template_slots(c['path'],c['after_record'],c['after'],template_root=r)

if __name__=='__main__':unittest.main(verbosity=2)
