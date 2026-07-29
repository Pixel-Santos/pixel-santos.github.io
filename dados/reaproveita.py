import json, re

src = "/private/tmp/claude-501/-Users-amandagoncalves/108ca16d-0535-4077-a989-2b5177efceea/scratchpad/pixel-santo.html"
html = open(src, encoding="utf-8").read()

# isolate the SAINTS array
i = html.index("const SAINTS = [")
j = html.index("\n];", i)
block = html[i:j]

# split into per-saint objects
chunks = re.split(r"\n  \{\n", block)[1:]
found = {}
for c in chunks:
    m = re.search(r'nome:\s*"((?:[^"\\]|\\.)*)"', c)
    if not m:
        continue
    nome = m.group(1).encode().decode("unicode_escape")
    bm = re.search(r"bio:\s*\[(.*?)\n    \]", c, re.S)
    bio = []
    if bm:
        for pm in re.finditer(r'"((?:[^"\\]|\\.)*)"', bm.group(1)):
            bio.append(pm.group(1).replace('\\"', '"').replace("\\\\", "\\"))
    ln = re.search(r'localNasc:\s*"((?:[^"\\]|\\.)*)"', c)
    lr = re.search(r'localRepouso:\s*"((?:[^"\\]|\\.)*)"', c)
    found[nome] = {
        "bio": bio,
        "localNasc": ln.group(1) if ln else "",
        "localRepouso": lr.group(1) if lr else "",
    }

santos = json.load(open("santos.json", encoding="utf-8"))
hits = 0
for s in santos:
    f = found.get(s["nome"])
    if f and f["bio"]:
        s["bio"] = f["bio"]
        s["localNasc"] = f["localNasc"]
        s["localRepouso"] = f["localRepouso"]
        hits += 1

json.dump(santos, open("santos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("bios reaproveitadas:", hits)
print("nomes encontrados no prototipo:", sorted(found))
faltam = [s["nome"] for s in santos if not s["bio"]]
print("faltam bios:", len(faltam))
open("faltam.txt", "w", encoding="utf-8").write("\n".join(
    f'{s["pageId"]}\t{s["nome"]}' for s in santos if not s["bio"]))
