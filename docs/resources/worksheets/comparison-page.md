---
title: "Build a comparison page a buyer can trust"
headline: "Build a comparison page a buyer can trust"
description: "Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters."
page_class: "page"
schema_type: "Article"
learning_resource: "true"
hide: ["navigation", "toc"]
date_published: "2026-09-24T00:00:00+00:00"
date_modified: "2026-09-24T00:00:00+00:00"
---

# Build a comparison page a buyer can trust

<div class="bw-learning">
<nav class="bw-learning-nav" aria-label="Learning resources"><a href="/resources/">Resources</a><a href="/resources/playbooks/">Eight playbooks</a><a href="/resources/audit/sample/">Fictional Audit</a><a href="/resources/demos/recordings/">Recorded demos</a><a href="/resources/provenance/sources/">Sources</a></nav><p>Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters.</p><p><a href="/resources/guides/comparison-page/">Read the guide</a> | <a download href="/assets/learning/worksheets/comparison-page.json">Download blank JSON</a></p><form data-title="Build a comparison page a buyer can trust" data-slug="comparison-page" autocomplete="off"><label for="f0">Products / editions / region / as-of date</label><textarea id="f0" name="Products / editions / region / as-of date" maxlength="2000"></textarea><label for="f1">Buyer evaluation need</label><textarea id="f1" name="Buyer evaluation need" maxlength="2000"></textarea><label for="f2">Comparison dimension</label><textarea id="f2" name="Comparison dimension" maxlength="2000"></textarea><label for="f3">Our supported claim and source</label><textarea id="f3" name="Our supported claim and source" maxlength="2000"></textarea><label for="f4">Other option supported claim and source</label><textarea id="f4" name="Other option supported claim and source" maxlength="2000"></textarea><label for="f5">Unknown or not-found information</label><textarea id="f5" name="Unknown or not-found information" maxlength="2000"></textarea><label for="f6">Limitations and prerequisites</label><textarea id="f6" name="Limitations and prerequisites" maxlength="2000"></textarea><label for="f7">Approved fact IDs / reviewer</label><textarea id="f7" name="Approved fact IDs / reviewer" maxlength="2000"></textarea><label for="f8">Draft selection guidance</label><textarea id="f8" name="Draft selection guidance" maxlength="2000"></textarea><label for="f9">Acceptance / next review date</label><textarea id="f9" name="Acceptance / next review date" maxlength="2000"></textarea><div class="actions"><button id="export" type="button">Export my worksheet</button><button type="reset" class="secondary">Reset</button><button id="print" type="button" class="secondary">Print / save as PDF</button></div><p id="message" role="status" aria-live="polite"></p></form>
</div>

<script>
const form=document.querySelector('.bw-learning form');const msg=document.getElementById('message');document.getElementById('export').addEventListener('click',()=>{const values=Object.fromEntries(new FormData(form));const has=Object.values(values).some(v=>v.trim());if(!has){msg.textContent='Add at least one worksheet entry before exporting.';return;}const payload={worksheet:form.dataset.title,version:'bw-content-2026-09-24-v1',classification:'user-entered; unreviewed',values};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=form.dataset.slug+'-worksheet.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);msg.textContent='Worksheet exported. Your entries remain in this page until reset or navigation.'});form.addEventListener('reset',()=>{msg.textContent='Worksheet cleared.'});document.getElementById('print').addEventListener('click',()=>window.print());
</script>
