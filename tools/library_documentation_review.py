"""One dated publication row; never an integration or compliance measurement."""
import hashlib
import json
from pathlib import Path
import re

DOC_REVIEW_SOURCE = 'https://broadcastwell.com/best-ai-visibility-tools-with-mcp'
DOC_REVIEW_METHOD_URL = DOC_REVIEW_SOURCE
DOC_REVIEW_METHOD_LABEL = 'Our dated MCP and API documentation review.'
DOC_REVIEW_RECEIPT_PATH = 'assets/library/otterly-plan-access-review-2026-09-17.json'
DOC_REVIEW_RECEIPT_URL = 'https://docs.broadcastwell.com/' + DOC_REVIEW_RECEIPT_PATH
DOC_REVIEW_RECORD_ID = 'otterlyai-2026-09-17'
DOC_REVIEW_FIELD_DATE = '2026-09-17'
DOC_REVIEW_SNAPSHOT_SHA256 = '3eb24eced80a5d0fe1b4f66d257d2d0817dd608c3a8b23d1db85ef37899eb1f3'
DOC_REVIEW_FACT_KEY = 'figure:5af00bfce83dbf587027a865e03f1ed5056ee4ae8f37a9c3b58c11b983d0c89f'
DOC_REVIEW_EXPECTED_RECEIPT = {
    'schema_version':'1.0',
    'source_url':DOC_REVIEW_SOURCE,
    'publication_date':'2026-09-18',
    'source_snapshot':{'read_utc':'2026-10-28T18:38:51.788710+00:00','html_sha256':DOC_REVIEW_SNAPSHOT_SHA256},
    'method':{'kind':'dated-publication-review','unit':'named MCP-access plan labels in one published provider record','count_rule':'Count Standard, Premium and Enterprise once each; Lite is explicitly excluded.','runtime_integration_test':False,'security_or_compliance_audit':False,'publisher_scored':False},
    'record':{'id':DOC_REVIEW_RECORD_ID,'provider':'OtterlyAI','field_date':DOC_REVIEW_FIELD_DATE,'MCP_connector':'Yes','MCP_plan_labels':['Standard','Premium','Enterprise'],'MCP_excluded_plan_labels':['Lite'],'official_API':'Yes','API_plan_labels':['Standard','Premium','Enterprise'],'API_excluded_plan_labels':['Lite'],'demo_without_account':'No','documentation_host':'docs.otterly.ai'},
    'lead_fact':{'source_url':DOC_REVIEW_SOURCE,'record':{'capture_date':DOC_REVIEW_FIELD_DATE,'subject':'OtterlyAI','metric':'MCP_access_named_plan_labels'},'count':3,'base':None,'unit':'plan-labels','label':'OtterlyAI MCP access: three named plan labels in the dated review'},
}

def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf8')

DOC_REVIEW_RECEIPT_SHA256 = hashlib.sha256(_canonical(DOC_REVIEW_EXPECTED_RECEIPT)).hexdigest()

def _unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError('duplicate documentation-review receipt key')
        result[key]=value
    return result

def _predicate_negated(prefix):
    # Scope belongs to this predicate, not to an unrelated earlier adjective.
    return bool(re.search(r"\b(?:(?:do|does|did|is|are|was|were|has|have)\s+not|cannot|can't|never|not)\s*$",prefix,re.I))

def _assurance_negated(prefix):
    return _predicate_negated(prefix) or bool(re.search(
        r'\bnot\s+(?:(?:yet|currently|fully)\s+)*(?:an?\s+)?(?:(?:SOC[- ]?2|Type\s+II|ISO[- ]?27001)\s+)*(?:audit\s+)?$',prefix,re.I))

def _execution_negated(prefix):
    return _predicate_negated(prefix) or bool(re.search(r'\bnot\s+an?\s*$',prefix,re.I))

def _claim_errors(text):
    errors=[]
    units=re.split(r'[.!?](?:\s|$)|[;\n]',text)
    for unit in units:
        own=bool(re.search(r'\b(?:our|this|Broadcastwell(?:[\'’]s)?)\s+(?:(?:published|dated|documentation|MCP|API|plan[- ]access)\s+)*(?:review|record|check|count|finding|figure)\b|\b(?:we|our team)\b',unit,re.I))
        if own:
            for hit in re.finditer(r'\b(?:prove[sd]?|establish(?:es|ed)?|confirm(?:s|ed)?|verif(?:y|ies|ied)|certif(?:y|ies|ied)|demonstrat(?:e|es|ed)|test(?:s|ed)?|execut(?:e|es|ed)|ran)\b',unit,re.I):
                suffix=unit[hit.end():]
                if re.search(r'\b(?:compliance|compliant|certification|secure|security|integration|execution|performance|outcomes?|results?|GDPR|SOC.?2|ISO.?27001|MCP|API|connector)\b',suffix,re.I) and not _predicate_negated(unit[:hit.start()]):
                    errors.append('documentation-review cannot turn publication evidence into tested integration, security, compliance or outcome evidence')
                    break
        if re.search(r'\b(?:MCP|API|connector|integration)\b',unit,re.I):
            for hit in re.finditer(r'\b(?:tested|executed|connected)\b',unit,re.I):
                if not _execution_negated(unit[:hit.start()]):
                    errors.append('documentation-review cannot report an executed MCP/API connection')
                    break
        if re.search(r'\b(?:three|3)\s+(?:named\s+)?plans?\b',unit,re.I):
            for hit in re.finditer(r'\b(?:certified|compliant|secure)\b',unit,re.I):
                if not _assurance_negated(unit[:hit.start()]):
                    errors.append('documentation-review plan labels cannot become compliant or certified plans')
        if re.search(r'\bOtterlyAI\b',unit,re.I):
            if re.search(r'\b(?:MCP|API)\b',unit,re.I) and re.search(r'\bLite\b',unit,re.I):
                for hit in re.finditer(r'\b(?:includes?|supports?|provides?|available on|enabled on)\b',unit,re.I):
                    if 'Lite' in unit[hit.end():] and not _predicate_negated(unit[:hit.start()]):
                        errors.append('documentation-review cannot include Lite in the pinned MCP/API plan list')
                        break
            if re.search(r'\b(?:SOC.?2|Type\s+II)\b',unit,re.I):
                for hit in re.finditer(r'\b(?:complete[sd]?|certified|compliant|passed)\b',unit,re.I):
                    if not _assurance_negated(unit[:hit.start()]):
                        errors.append('documentation-review cannot describe OtterlyAI’s roadmap audit as completed')
                        break
            for hit in re.finditer(r'\b(?:Standard|Premium)\s+(?:includes?|supports?|provides?|has)\s+SSO\b|\bSSO\s+(?:is\s+)?(?:available|included)\s+(?:on|in|with)\s+(?:Standard|Premium)\b',unit,re.I):
                if not _predicate_negated(unit[:hit.start()]):
                    errors.append('documentation-review MCP/API access does not establish SSO on Standard or Premium')
    if re.search(r'\b(?:OtterlyAI|Profound)\b[^.!?]{0,45}\b(?:charges?|costs?|starts? at|is free|priced at)\b',text,re.I):
        errors.append('documentation-review cannot establish provider prices')
    return errors

def validate_documentation_review(meta,body,measured,docs,*,plain_text,markdown_links,paragraph_after_heading):
    errors=[]
    expected={'is_based_on':DOC_REVIEW_SOURCE,'evidence_documentation_record':DOC_REVIEW_RECORD_ID,'evidence_documentation_field_date':DOC_REVIEW_FIELD_DATE,'evidence_documentation_snapshot_sha256':DOC_REVIEW_SNAPSHOT_SHA256,'evidence_documentation_receipt_sha256':DOC_REVIEW_RECEIPT_SHA256}
    for key,value in expected.items():
        if meta.get(key)!=value:
            errors.append('documentation-review requires exact approved '+key)
    if meta.get('evidence_method_receipts') or any(k.startswith(('evidence_audit_','evidence_list_audit_')) for k in meta):
        errors.append('documentation-review cannot use a DOI-study or unrelated audit method')
    try:
        receipt=json.loads((Path(docs)/DOC_REVIEW_RECEIPT_PATH).read_text(encoding='utf-8-sig'),object_pairs_hook=_unique)
        if hashlib.sha256(_canonical(receipt)).hexdigest()!=DOC_REVIEW_RECEIPT_SHA256:
            errors.append('documentation-review public receipt differs from the one pinned row, date, scope or plan labels')
    except (OSError,ValueError,TypeError) as error:
        errors.append('documentation-review public receipt cannot be verified: '+str(error))
    first=plain_text(paragraph_after_heading(body));text=plain_text(measured)
    if not re.search(r'\b(?:3|three)\s+(?:named\s+)?(?:MCP(?:[- ]access)?\s+)?plan(?:s| labels)\b',first,re.I) or '17 September 2026' not in first or 'OtterlyAI' not in first or not re.search(r'\bMCP\b',first):
        errors.append('first documentation-review paragraph must carry the dated three-plan OtterlyAI MCP record')
    links=markdown_links(measured)
    if any(url not in links for url in (DOC_REVIEW_SOURCE,DOC_REVIEW_RECEIPT_URL)):
        errors.append('documentation-review must link its exact published record and public receipt in What we measured')
    required_rows=[
        '| MCP connector | Yes |',
        '| MCP plans | Standard, Premium and Enterprise; not Lite |',
        '| Official API | Yes |',
        '| API plans | Standard, Premium and Enterprise; not Lite |',
        '| Record date | 17 September 2026 |',
    ]
    if any(row not in measured for row in required_rows):
        errors.append('documentation-review visible table must preserve the exact five selected publication fields')
    if not re.search(r'\b(?:public|published)\b',text,re.I) or not re.search(r'\b(?:documentation|publication|record)\b',text,re.I):
        errors.append('documentation-review must identify publication/documentation as its evidence')
    no_execution=re.search(r'\b(?:not|no|never)\b.{0,65}\b(?:executed|runtime|authenticated|integration|account|test(?:ed|s)?)\b',text,re.I)
    no_assurance=re.search(r'\b(?:not|no|never)\b.{0,90}\b(?:compliance|certification|security audit|audited security)\b',text,re.I)
    if not no_execution or not no_assurance:
        errors.append('documentation-review needs one plain scope limit covering execution and security/compliance assurance')
    for old in ('Every figure comes from the published method, v1.1.','Our answer-study method, v1.1.','Our published agency-audit criteria.','Our published agency-list audit criteria.'):
        if old in body:
            errors.append('documentation-review cannot borrow a study or different audit footer')
    errors.extend(_claim_errors(plain_text(body.split('## Next step')[0])))
    return errors
