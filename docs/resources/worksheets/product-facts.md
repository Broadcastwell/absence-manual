---
title: "Keep product facts consistent without inventing certainty"
headline: "Keep product facts consistent without inventing certainty"
description: "Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters."
page_class: "page"
schema_type: "Article"
learning_resource: "true"
hide: ["navigation", "toc"]
date_published: "2026-09-24T00:00:00+00:00"
date_modified: "2026-09-24T00:00:00+00:00"
---

# Keep product facts consistent without inventing certainty

<div class="bw-learning">
<nav class="bw-learning-nav" aria-label="Learning resources"><a href="/resources/">Resources</a><a href="/resources/playbooks/">Eight playbooks</a><a href="/resources/audit/sample/">Fictional Audit</a><a href="/resources/demos/recordings/">Recorded demos</a><a href="/resources/provenance/sources/">Sources</a></nav><p>Editable worksheet. Use permitted public or synthetic material. Entries stay in this page; export to keep a copy. Each field is limited to 2,000 characters.</p><p><a href="/resources/guides/product-facts/">Read the guide</a> | <a download href="/assets/learning/worksheets/product-facts.json">Download blank JSON</a></p><form data-title="Keep product facts consistent without inventing certainty" data-slug="product-facts" autocomplete="off"><label for="f0">Fact ID and version</label><textarea id="f0" name="Fact ID and version" maxlength="2000"></textarea><label for="f1">Approved wording or candidate wording</label><textarea id="f1" name="Approved wording or candidate wording" maxlength="2000"></textarea><label for="f2">Product / edition / region</label><textarea id="f2" name="Product / edition / region" maxlength="2000"></textarea><label for="f3">Exact source and source passage</label><textarea id="f3" name="Exact source and source passage" maxlength="2000"></textarea><label for="f4">Source review date</label><textarea id="f4" name="Source review date" maxlength="2000"></textarea><label for="f5">Accountable owner / reviewer</label><textarea id="f5" name="Accountable owner / reviewer" maxlength="2000"></textarea><label for="f6">Permitted uses</label><textarea id="f6" name="Permitted uses" maxlength="2000"></textarea><label for="f7">Dependent assets</label><textarea id="f7" name="Dependent assets" maxlength="2000"></textarea><label for="f8">State: supported, conflicting, stale, not found or pending</label><textarea id="f8" name="State: supported, conflicting, stale, not found or pending" maxlength="2000"></textarea><label for="f9">Resolution / superseded version</label><textarea id="f9" name="Resolution / superseded version" maxlength="2000"></textarea><label for="f10">Next review trigger</label><textarea id="f10" name="Next review trigger" maxlength="2000"></textarea><div class="actions"><button id="export" type="button">Export my worksheet</button><button type="reset" class="secondary">Reset</button><button id="print" type="button" class="secondary">Print / save as PDF</button></div><p id="message" role="status" aria-live="polite"></p></form>
</div>

<script>
const form=document.querySelector('.bw-learning form');const msg=document.getElementById('message');document.getElementById('export').addEventListener('click',()=>{const values=Object.fromEntries(new FormData(form));const has=Object.values(values).some(v=>v.trim());if(!has){msg.textContent='Add at least one worksheet entry before exporting.';return;}const payload={worksheet:form.dataset.title,version:'bw-content-2026-09-24-v1',classification:'user-entered; unreviewed',values};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=form.dataset.slug+'-worksheet.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);msg.textContent='Worksheet exported. Your entries remain in this page until reset or navigation.'});form.addEventListener('reset',()=>{msg.textContent='Worksheet cleared.'});document.getElementById('print').addEventListener('click',()=>window.print());
</script>
