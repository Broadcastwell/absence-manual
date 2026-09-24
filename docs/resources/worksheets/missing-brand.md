---
title: "Your brand was missing. What does that actually tell you?"
headline: "Your brand was missing. What does that actually tell you?"
description: "Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters."
page_class: "page"
schema_type: "Article"
learning_resource: "true"
hide: ["navigation", "toc"]
date_published: "2026-09-24T00:00:00+00:00"
date_modified: "2026-09-24T00:00:00+00:00"
---

# Your brand was missing. What does that actually tell you?

<div class="bw-learning">
<nav class="bw-learning-nav" aria-label="Learning resources"><a href="/resources/">Resources</a><a href="/resources/playbooks/">Eight playbooks</a><a href="/resources/audit/sample/">Fictional Audit</a><a href="/resources/demos/recordings/">Recorded demos</a><a href="/resources/provenance/sources/">Sources</a></nav><p>Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters.</p><p><a href="/resources/guides/missing-brand/">Read the guide</a> | <a download href="/assets/learning/worksheets/missing-brand.json">Download blank JSON</a></p><form data-title="Your brand was missing. What does that actually tell you?" data-slug="missing-brand" autocomplete="off"><label for="f0">Receipt and reviewed absence</label><textarea id="f0" name="Receipt and reviewed absence" maxlength="2000"></textarea><label for="f1">Completion and extraction checks</label><textarea id="f1" name="Completion and extraction checks" maxlength="2000"></textarea><label for="f2">Aliases and former names checked</label><textarea id="f2" name="Aliases and former names checked" maxlength="2000"></textarea><label for="f3">Buyer / question fit</label><textarea id="f3" name="Buyer / question fit" maxlength="2000"></textarea><label for="f4">Independent page or fact evidence</label><textarea id="f4" name="Independent page or fact evidence" maxlength="2000"></textarea><label for="f5">Supported finding versus hypothesis</label><textarea id="f5" name="Supported finding versus hypothesis" maxlength="2000"></textarea><label for="f6">Proposed action or no-change decision</label><textarea id="f6" name="Proposed action or no-change decision" maxlength="2000"></textarea><label for="f7">Acceptance check</label><textarea id="f7" name="Acceptance check" maxlength="2000"></textarea><label for="f8">Evidence that would change the decision</label><textarea id="f8" name="Evidence that would change the decision" maxlength="2000"></textarea><div class="actions"><button id="export" type="button">Export my worksheet</button><button type="reset" class="secondary">Reset</button><button id="print" type="button" class="secondary">Print / save as PDF</button></div><p id="message" role="status" aria-live="polite"></p></form>
</div>

<script>
const form=document.querySelector('.bw-learning form');const msg=document.getElementById('message');document.getElementById('export').addEventListener('click',()=>{const values=Object.fromEntries(new FormData(form));const has=Object.values(values).some(v=>v.trim());if(!has){msg.textContent='Add at least one worksheet entry before exporting.';return;}const payload={worksheet:form.dataset.title,version:'bw-content-2026-09-24-v1',classification:'user-entered; unreviewed',values};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=form.dataset.slug+'-worksheet.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);msg.textContent='Worksheet exported. Your entries remain in this page until reset or navigation.'});form.addEventListener('reset',()=>{msg.textContent='Worksheet cleared.'});document.getElementById('print').addEventListener('click',()=>window.print());
</script>
