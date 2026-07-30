"""Monta a tabela de revisao: o que a Wikidata achou, cruzado com o que a Amanda ja tem."""
import json, re

santos = {s["nome"]: s for s in json.load(open("dados/santos.json", encoding="utf-8"))}
wd = {r["nome"]: r for r in json.load(open("dados/wikidata.json", encoding="utf-8"))}

linhas, sem_id, sem_local = [], [], []
for nome, s in santos.items():
    r = wd.get(nome, {})
    if r.get("conf") != "ok":
        sem_id.append(nome); continue
    nascL, sepL = r.get("nascLocal",""), r.get("sepLocal","")
    if not nascL and not sepL:
        sem_local.append(nome)
    linhas.append({
        "nome": nome,
        "rotuloWikidata": r.get("rotulo"),
        "qid": r.get("qid"),
        "nascLocal": nascL,
        "sepLocal": sepL,
        "precisaFoto": not s["temFoto"],
        "imagemWikidata": r.get("imagem",""),
    })

json.dump(linhas, open("dados/revisao.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"identificados ........: {len(linhas)}")
print(f"nao identificados ....: {len(sem_id)}")
if sem_id: print("   " + "; ".join(sem_id))
print(f"com nascimento .......: {sum(1 for l in linhas if l['nascLocal'])}")
print(f"com sepultamento .....: {sum(1 for l in linhas if l['sepLocal'])}")
print(f"precisam foto ........: {sum(1 for l in linhas if l['precisaFoto'])}")
print(f"   destes, com imagem : {sum(1 for l in linhas if l['precisaFoto'] and l['imagemWikidata'])}")
