#!/usr/bin/env python3
"""Lean tools for the JEPA-inspired Site World Model.

Commands:
  python scripts/site_world_model_tools.py validate examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py summarize examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py graphml examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py checklist examples/anonymized_site_001/site_world_model_bundle.json
  python scripts/site_world_model_tools.py report examples/anonymized_site_001/site_world_model_bundle.json
"""
from __future__ import annotations
import json, sys, html
from pathlib import Path

VALID_CONFIDENCE={"high","medium","low","unknown"}
VALID_VERIFICATION={"not_required","pending","verified","contradicted","revised"}
REQUIRED_SECTIONS=["project","observations","predictions","risks","verification_tasks","interventions","design_scenarios"]
BAD_REPORT_PHRASES=["guaranteed","perfect","will definitely","no risk"]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_items(data):
    for section in ["observations","predictions","risks","verification_tasks","interventions"]:
        for item in data.get(section,[]):
            yield section,item


def validate(path: Path) -> int:
    data=load(path); errors=[]
    for section in REQUIRED_SECTIONS:
        if section not in data: errors.append(f"missing section: {section}")
    ids={item.get("id") for _,item in all_items(data) if item.get("id")}
    for section,item in all_items(data):
        for field in ["id","claim_type","summary","source","confidence","verification_status"]:
            if field not in item: errors.append(f"{section}:{item.get('id','<missing>')} missing {field}")
        if item.get("confidence") not in VALID_CONFIDENCE: errors.append(f"{item.get('id')} invalid confidence")
        if item.get("verification_status") not in VALID_VERIFICATION: errors.append(f"{item.get('id')} invalid verification_status")
    for pred in data.get("predictions",[]):
        for ref in pred.get("based_on",[])+pred.get("evidence_ids",[]):
            if ref not in ids: errors.append(f"prediction {pred['id']} references missing {ref}")
        if pred.get("verification_required") and not pred.get("verification_tasks"):
            errors.append(f"prediction {pred['id']} requires verification but has no tasks")
    task_ids={t["id"] for t in data.get("verification_tasks",[]) if "id" in t}
    for intervention in data.get("interventions",[]):
        if not intervention.get("supported_by"): errors.append(f"intervention {intervention.get('id')} lacks support")
        joined=" ".join(intervention.get("risks",[])).lower()
        risky=any(w in joined for w in ["foundation","utility","infiltration","digging","water"])
        if risky and not set(intervention.get("required_verification",[])).intersection(task_ids):
            errors.append(f"high-risk intervention {intervention.get('id')} lacks verification")
    for scenario in data.get("design_scenarios",[]):
        for field in ["id","name","summary","benefits","risks","unknowns","verification_needed","confidence"]:
            if field not in scenario: errors.append(f"scenario {scenario.get('id','<missing>')} missing {field}")
    if errors:
        print("FAIL")
        for e in errors: print("-",e)
        return 1
    print("PASS: Site World Model bundle validates."); return 0


def summarize(path: Path) -> int:
    data=load(path)
    for section in ["observations","predictions","risks","verification_tasks","interventions","design_scenarios"]:
        print(f"{section}: {len(data.get(section,[]))}")
    print("pending high-priority checks:")
    for t in data.get("verification_tasks",[]):
        if t.get("priority")=="high" and t.get("status")=="pending": print(f"- {t['id']}: {t['summary']}")
    return 0


def write_graphml(path: Path) -> int:
    data=load(path); out=path.with_name("site_model.generated.graphml")
    lines=['<?xml version="1.0" encoding="UTF-8"?>','<graphml xmlns="http://graphml.graphdrawing.org/xmlns">']
    for key in ["label","type","claim_type","confidence","source","verification_status"]:
        lines.append(f'  <key id="{key}" for="all" attr.name="{key}" attr.type="string"/>')
    lines.append('  <graph id="site_world_model_generated" edgedefault="directed">')
    section_type={"observations":"Observation","predictions":"Prediction","risks":"Risk","verification_tasks":"VerificationTask","interventions":"Intervention"}
    ids=set()
    for section,items in data.items():
        if section not in section_type: continue
        for item in items:
            ids.add(item["id"]); lines.append(f'    <node id="{item["id"]}">')
            vals={"label":item["summary"][:100],"type":section_type[section],"claim_type":item.get("claim_type",""),"confidence":item.get("confidence",""),"source":item.get("source",""),"verification_status":item.get("verification_status","")}
            for k,v in vals.items(): lines.append(f'      <data key="{k}">{html.escape(str(v))}</data>')
            lines.append('    </node>')
    n=1
    for _,item in all_items(data):
        for ref in item.get("evidence_ids",[])+item.get("based_on",[])+item.get("required_verification",[])+item.get("verification_tasks",[]):
            if ref in ids:
                lines.append(f'    <edge id="edge_{n:03d}" source="{item["id"]}" target="{ref}"/>'); n+=1
    lines += ['  </graph>','</graphml>']; out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Wrote {out}"); return 0


def checklist(path: Path) -> int:
    data=load(path); out=path.with_name("field_visit_checklist.generated.md")
    lines=["# Generated Field Verification Checklist",""]
    order={"high":0,"medium":1,"low":2}
    for t in sorted(data.get("verification_tasks",[]),key=lambda x:order.get(x.get("priority","low"),9)):
        lines.append(f"- [ ] **{t.get('priority','').upper()}** — {t['summary']}")
        lines.append(f"  - Method: {t.get('method','')}")
    out.write_text("\n".join(lines)+"\n",encoding="utf-8"); print(f"Wrote {out}"); return 0


def report(path: Path) -> int:
    data=load(path); out=path.with_name("client_report.generated.md")
    project=data.get("project",{}).get("project_name","Anonymized site")
    lines=["# Generated Preliminary Client Report","",f"**Project:** {project}","","This is preliminary and evidence-calibrated. Candidate directions require verification before final recommendation.","","## Candidate patterns to verify"]
    for p in data.get("predictions",[]): lines.append(f"- {p['summary']} Confidence: {p['confidence']}.")
    lines.append("\n## Candidate interventions")
    for i in data.get("interventions",[]): lines.append(f"- {i['summary']} Required verification: {', '.join(i.get('required_verification',[]))}.")
    lines.append("\n## Next verification tasks")
    for t in data.get("verification_tasks",[]): lines.append(f"- {t['summary']}")
    text="\n".join(lines)+"\n"
    low=text.lower()
    for bad in BAD_REPORT_PHRASES:
        if bad in low: raise SystemExit(f"Unsafe report phrase detected: {bad}")
    out.write_text(text,encoding="utf-8"); print(f"Wrote {out}"); return 0


def main(argv):
    if len(argv)!=3: print(__doc__); return 2
    cmd,path=argv[1],Path(argv[2])
    return {"validate":validate,"summarize":summarize,"graphml":write_graphml,"checklist":checklist,"report":report}.get(cmd,lambda p:2)(path)

if __name__=="__main__": raise SystemExit(main(sys.argv))
