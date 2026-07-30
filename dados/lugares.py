import json, urllib.parse, urllib.request, time

UA = {"User-Agent": "PixelSanto/1.0 (catalogo de santos)", "Accept": "application/sparql-results+json"}

def sparql(q):
    u = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(q)
    for t in range(4):
        try:
            r = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(r, timeout=60) as f:
                return json.loads(f.read().decode())["results"]["bindings"]
        except Exception as e:
            print(f"  tentativa {t+1} falhou: {e}", flush=True)
            time.sleep(3 + 3*t)
    return None

wd = json.load(open("dados/wikidata.json", encoding="utf-8"))
qids = [r["qid"] for r in wd if r.get("qid")]
print(f"consultando lugares de {len(qids)} pessoas", flush=True)

achou = {}
for k in range(0, len(qids), 30):
    lote = qids[k:k+30]
    valores = " ".join(f"wd:{q}" for q in lote)
    q = f"""
SELECT ?p ?nascLabel ?nascPaisLabel ?sepLabel ?sepPaisLabel WHERE {{
  VALUES ?p {{ {valores} }}
  OPTIONAL {{ ?p wdt:P19 ?nasc. OPTIONAL {{ ?nasc wdt:P17 ?nascPais. }} }}
  OPTIONAL {{ ?p wdt:P119 ?sep.  OPTIONAL {{ ?sep  wdt:P17 ?sepPais.  }} }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pt,en". }}
}}"""
    res = sparql(q)
    if res is None:
        print(f"  lote {k//30+1}: FALHOU", flush=True); continue
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
    print(f"  lote {k//30+1}: {len(res)} linhas", flush=True)
    time.sleep(1)

n_nasc = n_sep = 0
for r in wd:
    a = achou.get(r.get("qid") or "", {})
    r["nascLocal"] = a.get("nasc", "")
    r["sepLocal"] = a.get("sep", "")
    n_nasc += bool(r["nascLocal"]); n_sep += bool(r["sepLocal"])

json.dump(wd, open("dados/wikidata.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nPRONTO. nascimento={n_nasc} sepultamento={n_sep}", flush=True)
