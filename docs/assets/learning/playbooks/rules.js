(function(root){'use strict';
function evaluate(kind,x){
 const hold=(why)=>({status:'hold',reason:why,side_effects:'none'});
 const ready=(result)=>({status:'ready_for_review',result,side_effects:'none'});
 if(!x||typeof x!=='object'||Array.isArray(x))return hold('Input must be a JSON object.');
 if(x.authorized!==true)return hold('Permitted input and authority are not confirmed.');
 if(x.contains_private_data===true)return hold('Remove unauthorized private data before using this public learning tool.');
 if(x.embedded_instruction===true)return hold('Treat embedded instructions as source text; do not execute them.');
 switch(kind){
 case 'receipt-review':
   if(!['completed','failed','untested','uncertain'].includes(x.result_state))return hold('Unknown result state.');
   if(x.result_state!=='completed')return ready({mention_state:'not_evaluated',observation_state:x.result_state,interpretation:'No verified presence or absence.'});
   if(!x.receipt_ref||!x.surface||!x.method_version||!x.observed_at)return hold('Completed observations need receipt, actual surface, date and method.');
   if(x.reviewed!==true)return ready({mention_state:'not_evaluated',interpretation:'Completed; review pending.'});
   if(!['present','absent'].includes(x.reviewed_mention))return hold('Reviewed mention must be present or absent.');
   if(x.reviewed_mention==='absent'&&x.alias_checked!==true)return hold('Check approved aliases before confirming absence.');
   return ready({mention_state:x.reviewed_mention,interpretation:'Limited to this completed reviewed observation; no causal or revenue conclusion.'});
 case 'question-selection':
   if(!Array.isArray(x.questions)||x.questions.length!==10)return hold('Provide exactly ten candidate questions for this bounded exercise.');
   if(x.demand_claim)return hold('Do not invent search volume or demand.');
   const seen=new Set();let issues=[];
   for(const [i,q] of x.questions.entries()){
     if(!q||typeof q.text!=='string'||!q.text.trim()||q.text.length>500||!q.need||!q.reason){issues.push('Question '+(i+1)+' needs bounded wording, need and reason.');continue;}
     const key=q.text.toLowerCase().replace(/[^a-z0-9 ]/g,'').replace(/\s+/g,' ').trim();if(seen.has(key))issues.push('Duplicate question '+(i+1));seen.add(key);
     if(/why is .* (best|superior)|guaranteed|number one/i.test(q.text))issues.push('Leading wording in question '+(i+1));
     if(/\band\b.*\band\b/i.test(q.text))issues.push('Review compound requirements in question '+(i+1));
   }
   return issues.length?hold(issues.join(' ')):ready({count:10,scope_status:'candidate; actual owner approval pending',volume:'not_estimated'});
 case 'fact-verification':
   if(!x.fact_id||!x.source_ref||!x.version||!x.source_date)return hold('Fact/source/version/date are required.');
   if(x.sources_disagree)return hold('Conflicting sources require accountable owner resolution.');
   if(x.stale)return ready({fact_state:'stale',action:'Refresh source review; do not reuse as current approved wording.'});
   if(x.explicit_contradiction)return ready({fact_state:'conflicting',action:'Send factual conflict to accountable owner; no automatic rewrite.'});
   if(!x.explicit_support)return ready({fact_state:'not_found',action:'Unknown from the supplied source; not classified false.'});
   if(!x.owner||!x.reviewer)return hold('A supported fact still needs an accountable owner and reviewer.');
   return ready({fact_state:'supported_in_supplied_scope',fact_id:x.fact_id,version:x.version,source_ref:x.source_ref,owner:x.owner,reviewer:x.reviewer});
 case 'comparison-brief':
   if(x.universal_superiority||x.invented_weakness)return hold('Remove universal superiority or unsupported competitor weakness.');
   if(!x.scope||!x.editions||!x.region||!x.as_of)return hold('State comparison products, editions, region and date.');
   if(!Array.isArray(x.rows)||!x.rows.length)return hold('Provide sourced comparison rows.');
   if(x.rows.some(r=>!r.dimension||!['supported','unknown'].includes(r.state)||(r.state==='supported'&&!r.source_ref)))return hold('Each row needs a dimension and source, or explicit unknown state.');
   return ready({brief_state:'candidate',unknowns:x.rows.filter(r=>r.state==='unknown').length,approval:'factual review pending'});
 case 'technical-change':
   if(x.disable_security||x.require_training_crawler)return hold('Do not disable security or require training-crawler access as a blanket search prerequisite.');
   if(!x.defect_ref||!x.route||!x.change||!x.preview_test||!x.rollback)return hold('Specify observed defect, route, bounded change, preview acceptance and rollback.');
   if(x.placement_guarantee)return hold('Technical acceptance does not guarantee indexation or answer placement.');
   return ready({work_state:'draft',route:x.route,release:'existing owner path; no production write'});
 case 'source-correction':
   if(x.impersonation||x.fake_review||x.paid_placement)return hold('No impersonation, fake review or paid placement.');
   if(!x.source_ref||!x.fact_ref||!x.exact_error||!x.correction)return hold('Supply exact source error and supported correction.');
   if(x.action==='send')return hold('This playbook drafts only; sending belongs to the separately authorized owner.');
   if(x.claim_source_changed&&!x.verified_changed_source_ref)return hold('A sent submission is not evidence that the source changed.');
   return ready({correction_state:x.verified_changed_source_ref?'source_change_evidence_supplied_for_review':'draft_only',sent:false,recipient_authority:x.recipient_verified?'supplied; owner must confirm':'unconfirmed'});
 case 'recheck-review':
   const b=x.baseline,f=x.follow_up;
   if(!b||!f)return hold('Baseline and follow-up records required.');
   if(x.causal_claim)return hold('Observational comparison does not establish causality.');
   if(b.result_state!=='completed'||f.result_state!=='completed'||!b.reviewed||!f.reviewed)return ready({comparison_state:'excluded',reason:'Failed, untested, uncertain or unreviewed record retained; no zero imputation.'});
   if(['question_id','surface','method','locale'].some(k=>!b[k]||b[k]!==f[k]))return ready({comparison_state:'limited',reason:'Question, surface, method or locale changed; not pooled as like-for-like.'});
   if(!b.date||!f.date||!b.receipt||!f.receipt)return hold('Both dates and receipts required.');
   if(!['present','absent'].includes(b.mention)||!['present','absent'].includes(f.mention))return hold('Both reviewed mention states required.');
   return ready({comparison_state:'matched',change:b.mention===f.mention?'no_observed_mention_change':b.mention==='absent'?'observed_absent_to_present':'observed_present_to_absent',causality:'not_established'});
 case 'commercial-review':
   if(!Array.isArray(x.events)||x.events.length>200)return hold('Provide up to 200 synthetic or permitted nonpersonal events.');
   if(x.basis!=='cash')return hold('This exercise uses cash collections; do not mix recognition and cash.');
   let ids=new Set(),counts={qualified_inquiries:0,held_conversations:0,paid_events:0,test_excluded:0,duplicate_excluded:0},gross=0,refund=0,fee=0;
   for(const e of x.events){
    if(!e||!e.id||typeof e.is_test!=='boolean')return hold('Each event needs a stable ID and explicit test/live flag.');
    if(ids.has(e.id)){counts.duplicate_excluded++;continue;}ids.add(e.id);if(e.is_test){counts.test_excluded++;continue;}
    if(e.type==='qualified_inquiry'){counts.qualified_inquiries++;continue;}if(e.type==='held_conversation'){counts.held_conversations++;continue;}
    if(['payment','refund','fee'].includes(e.type)){
     if(e.reconciled!==true)return hold('Financial event needs reconciliation evidence.');
     if(e.currency!=='USD'||typeof e.amount!=='number'||!Number.isFinite(e.amount)||e.amount<0)return hold('Use finite nonnegative USD amounts in this bounded example.');
     if(e.type==='payment'){gross+=e.amount;counts.paid_events++;}else if(e.type==='refund')refund+=e.amount;else fee+=e.amount;
    }
   }
   return ready({...counts,currency:'USD',cash_collected:gross,refunds:refund,fees:fee,net_after_refunds_and_fees:Math.round((gross-refund-fee)*100)/100,direct_costs:'not_supplied; margin not calculated',attribution:'not_established'});
 default:return hold('Unknown playbook.');}
}
if(typeof module!=='undefined'&&module.exports)module.exports={evaluate};else root.BWPlaybooks={evaluate};
})(typeof globalThis!=='undefined'?globalThis:this);