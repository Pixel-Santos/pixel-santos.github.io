import json, urllib.parse, urllib.request, time

UA = {"User-Agent": "PixelSanto/1.0 (catalogo de santos)", "Accept": "application/sparql-results+json"}

def sparql(q):
    u = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)
    for t in range(6):
        try:
            r = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(r, timeout=90) as f:
                return json.loads(f.read().decode())["results"]["bindings"]
        except Exception as e:
            print(f"    falhou ({e}), aguardando 70s", flush=True)
            time.sleep(70)
    return None

wd = json.load(open("dados/wikidata.json", encoding="utf-8"))
pend = [r["qid"] for r in wd if r.get("qid") and not r["nascLocal"] and not r["sepLocal"]]
print(f"pendentes: {len(pend)}", flush=True)

achou = {}
for k in range(0, len(pend), 25):
    lote = pend[k:k+25]
    valores = " ".join(f"wd:{q}" for q in lote)
    q = f"""
SELECT ?p ?nascLabel ?nascPaisLabel ?sepLabel ?sepPaisLabel WHERE {{
  VALUES ?p {{ {valores} }}
  OPTIONAL {{ ?p wdt:P19 ?nasc. OPTIONAL {{ ?nasc wdt:P17 ?nascPais. }} }}
  OPTIONAL {{ ?p wdt:P119 ?sep.  OPTIONAL {{ ?sep  wdt:P17 ?sepPais.  }} }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pt,en". }}
}}"""
    print(f"  lote {k//25+1} ({len(lote)} pessoas)", flush=True)
    res = sparql(q)
    if res:
        for b in res:
            pid = b["p"]["value"].rsplit("/", 1)[-1]
            def par(a, c):
                v = b.get(a, {}).get("value", "")
                if not v: return ""
                pais = b.get(c, {}).get("value", "")
                return f"{v}, {pais}" if pais and pais != v else v
            cur = achou.setdefault(pid, {"nasc": "", "sep": ""})
            cur["nasc"] = cur["nasc"] or par("nascLabel", "nascPaisLabel")
            cur["sep"]  = cur["sep"]  or par("sepLabel", "sepPaisLabel")
        print(f"    ok, {len(res)} linhas", flush=True)
    if k + 25 < len(pend):
        time.sleep(70)

for r in wd:
    a = achou.get(r.get("qid") or "", {})
    if a.get("nasc") and not r["nascLocal"]: r["nascLocal"] = a["nasc"]
    if a.get("sep")  and not r["sepLocal"]:  r["sepLocal"]  = a["sep"]

json.dump(wd, open("dados/wikidata.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nPRONTO. nascimento={sum(1 for r in wd if r['nascLocal'])} "
      f"sepultamento={sum(1 for r in wd if r['sepLocal'])}", flush=True)
