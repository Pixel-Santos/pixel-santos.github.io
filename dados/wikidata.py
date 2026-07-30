import json, re, urllib.parse, urllib.request, time

UA = "PixelSanto/1.0 (catalogo de santos)"

def get(url, tent=3):
    for t in range(tent):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode())
        except Exception:
            time.sleep(1 + t)
    return {}

def buscar(nome, lang="pt"):
    u = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
         f"&language={lang}&uselang={lang}&type=item&limit=6&search={urllib.parse.quote(nome)}")
    return [h["id"] for h in get(u).get("search", [])]

def ents(ids):
    out = {}
    ids = [i for i in dict.fromkeys(ids) if i]
    for k in range(0, len(ids), 45):
        lote = ids[k:k+45]
        u = ("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json"
             f"&props=claims|labels&languages=pt|en&ids={'|'.join(lote)}")
        out.update(get(u).get("entities", {}))
    return out

def qids(e, p):
    r = []
    for c in e.get("claims", {}).get(p, []):
        dv = c.get("mainsnak", {}).get("datavalue", {})
        if dv.get("type") == "wikibase-entityid":
            r.append(dv["value"]["id"])
    return r

def sval(e, p):
    for c in e.get("claims", {}).get(p, []):
        dv = c.get("mainsnak", {}).get("datavalue", {})
        if dv.get("type") == "string":
            return dv["value"]
    return None

def rot(e):
    for l in ("pt", "en"):
        if e.get("labels", {}).get(l): return e["labels"][l]["value"]
    return None

def ano(e, p):
    for c in e.get("claims", {}).get(p, []):
        dv = c.get("mainsnak", {}).get("datavalue", {})
        if dv.get("type") == "time":
            m = re.match(r"[+-](\d{4})", dv["value"]["time"])
            if m: return int(m.group(1))
    return None

santos = json.load(open("dados/santos.json", encoding="utf-8"))

print("fase 1: buscando nomes", flush=True)
cand = {}
for i, s in enumerate(santos, 1):
    limpo = re.sub(r"\s*\(.*?\)", "", s["nome"]).strip()
    ids = buscar(limpo)
    if not ids: ids = buscar(limpo, "en")
    cand[s["nome"]] = ids[:6]
    if i % 15 == 0: print(f"  {i}/84", flush=True)

print("fase 2: baixando entidades", flush=True)
todos = [x for v in cand.values() for x in v]
E = ents(todos)

print("fase 3: escolhendo por ano", flush=True)
esc = {}
for s in santos:
    for q in cand[s["nome"]]:
        e = E.get(q)
        if not e or "Q5" not in qids(e, "P31"): continue
        an, am = ano(e, "P569"), ano(e, "P570")
        if (an and abs(an - s["nasc"]) <= 2) or (am and abs(am - s["fale"]) <= 2):
            esc[s["nome"]] = q; break

print("fase 4: resolvendo lugares", flush=True)
lug = []
for q in esc.values():
    lug += qids(E[q], "P19") + qids(E[q], "P119")
L = ents(lug)
paises = []
for e in L.values():
    paises += qids(e, "P17")
P = ents(paises)

def nome_lugar(q):
    e = L.get(q)
    if not e or not rot(e): return ""
    pais = ""
    for cq in qids(e, "P17"):
        if P.get(cq) and rot(P[cq]): pais = rot(P[cq]); break
    return f"{rot(e)}, {pais}" if pais else rot(e)

res = []
for s in santos:
    q = esc.get(s["nome"])
    if not q:
        res.append({"nome": s["nome"], "conf": "nao identificado", "qid": None,
                    "rotulo": None, "nascLocal": "", "sepLocal": "", "imagem": ""})
        continue
    e = E[q]
    img = sval(e, "P18")
    res.append({
        "nome": s["nome"], "conf": "ok", "qid": q, "rotulo": rot(e),
        "nascLocal": next((nome_lugar(x) for x in qids(e, "P19") if nome_lugar(x)), ""),
        "sepLocal":  next((nome_lugar(x) for x in qids(e, "P119") if nome_lugar(x)), ""),
        "imagem": ("https://commons.wikimedia.org/wiki/Special:FilePath/"
                   + urllib.parse.quote(img.replace(" ", "_")) if img else ""),
    })

json.dump(res, open("dados/wikidata.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
ok = [r for r in res if r["conf"] == "ok"]
print(f"\nPRONTO. identificados {len(ok)}/84")
print(f"  com local de nascimento ....: {sum(1 for r in ok if r['nascLocal'])}")
print(f"  com local de sepultamento ..: {sum(1 for r in ok if r['sepLocal'])}")
print(f"  com imagem .................: {sum(1 for r in ok if r['imagem'])}")
