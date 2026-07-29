#!/usr/bin/env python3
"""
Gerador do site Pixel Santo.

Le a base "S A N T O S" no Notion, baixa as fotos, e escreve o site
pronto em site/.

Uso:
    export NOTION_TOKEN='...'      # a chave da sua integracao do Notion
    python3 build.py

A chave nunca fica salva no codigo, ela vem sempre da variavel de ambiente.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------- configuracao

DATABASE_ID = "19b3bb9d-9908-80fb-bcf9-e4d021a15d36"
NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"

RAIZ = Path(__file__).parent
TEMPLATE = RAIZ / "template.html"
SAIDA = RAIZ / "site"
PASTA_IMG = SAIDA / "img"

LARGURA_FOTO = 800          # px, o suficiente para telas retina nos cards
QUALIDADE_FOTO = 72         # 0-100, compressao jpeg


def token():
    valor = os.environ.get("NOTION_TOKEN", "").strip()
    if not valor:
        sys.exit(
            "ERRO: falta a variavel NOTION_TOKEN.\n"
            "Rode:  export NOTION_TOKEN='sua_chave_do_notion'"
        )
    return valor


# ------------------------------------------------------------------ notion api

def chamar(caminho, metodo="GET", corpo=None):
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(
        f"{API}{caminho}",
        data=dados,
        method=metodo,
        headers={
            "Authorization": f"Bearer {token()}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "replace")[:400]
        if e.code == 401:
            sys.exit("ERRO 401: a chave do Notion e invalida ou expirou.")
        if e.code == 404:
            sys.exit(
                "ERRO 404: o Notion nao encontrou a base.\n"
                "Confira se voce compartilhou a pagina com a integracao "
                "(botao ... > Conexoes > sua integracao)."
            )
        sys.exit(f"ERRO {e.code} do Notion: {detalhe}")


def listar_paginas():
    """Todas as linhas da base, seguindo a paginacao do Notion."""
    paginas, cursor = [], None
    while True:
        corpo = {"page_size": 100}
        if cursor:
            corpo["start_cursor"] = cursor
        r = chamar(f"/databases/{DATABASE_ID}/query", "POST", corpo)
        paginas.extend(r.get("results", []))
        if not r.get("has_more"):
            return paginas
        cursor = r.get("next_cursor")


def blocos(page_id):
    todos, cursor = [], None
    while True:
        q = "?page_size=100" + (f"&start_cursor={cursor}" if cursor else "")
        r = chamar(f"/blocks/{page_id}/children{q}")
        todos.extend(r.get("results", []))
        if not r.get("has_more"):
            return todos
        cursor = r.get("next_cursor")


# -------------------------------------------------------------- leitura de campos

def texto_de(rich):
    return "".join(p.get("plain_text", "") for p in (rich or [])).strip()


def campo(props, nome, tipo):
    p = props.get(nome)
    if not p:
        return None
    if tipo == "title":
        return texto_de(p.get("title"))
    if tipo == "rich_text":
        return texto_de(p.get("rich_text"))
    if tipo == "number":
        return p.get("number")
    if tipo == "select":
        s = p.get("select")
        return s.get("name") if s else None
    if tipo == "files":
        for arq in p.get("files") or []:
            if arq.get("type") == "external":
                return arq["external"].get("url")
            if arq.get("type") == "file":
                return arq["file"].get("url")
    return None


TIPOS_TEXTO = {
    "paragraph", "heading_1", "heading_2", "heading_3",
    "quote", "bulleted_list_item", "numbered_list_item",
}


def biografia(page_id):
    """Junta os paragrafos da pagina, ignorando imagens e blocos vazios."""
    paragrafos = []
    for b in blocos(page_id):
        tipo = b.get("type")
        if tipo not in TIPOS_TEXTO:
            continue
        t = texto_de(b.get(tipo, {}).get("rich_text"))
        if t:
            paragrafos.append(t)
    return paragrafos


# ------------------------------------------------------------------------ fotos

def slug(nome):
    base = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "santo"


def existe(programa):
    return shutil.which(programa) is not None


def comprimir(origem, destino):
    """Redimensiona e comprime. Usa sips no Mac, ImageMagick no Linux."""
    if existe("sips"):
        cmd = ["sips", "-Z", str(LARGURA_FOTO),
               "-s", "format", "jpeg",
               "-s", "formatOptions", str(QUALIDADE_FOTO),
               str(origem), "--out", str(destino)]
    elif existe("magick"):
        cmd = ["magick", str(origem), "-resize", f"{LARGURA_FOTO}x{LARGURA_FOTO}>",
               "-quality", str(QUALIDADE_FOTO), str(destino)]
    elif existe("convert"):
        cmd = ["convert", str(origem), "-resize", f"{LARGURA_FOTO}x{LARGURA_FOTO}>",
               "-quality", str(QUALIDADE_FOTO), str(destino)]
    else:
        # sem ferramenta de imagem, usa o arquivo original sem comprimir
        shutil.copyfile(origem, destino)
        return True

    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0 and destino.exists()


def baixar_foto(url, destino):
    """Baixa e comprime a foto. Devolve True se deu certo."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PixelSanto/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            bruto = r.read()
    except Exception as e:
        print(f"    aviso: nao consegui baixar a foto ({e})")
        return False

    temp = destino.with_suffix(".original")
    temp.write_bytes(bruto)
    try:
        if not comprimir(temp, destino):
            print("    aviso: nao consegui converter a foto")
            return False
    finally:
        temp.unlink(missing_ok=True)
    return True


# ---------------------------------------------------------------------- montagem

def montar():
    print("Buscando a base no Notion...")
    paginas = listar_paginas()
    print(f"  {len(paginas)} registros encontrados\n")

    PASTA_IMG.mkdir(parents=True, exist_ok=True)

    santos, sem_foto, sem_bio, sem_local = [], [], [], []

    for i, pagina in enumerate(paginas, 1):
        props = pagina.get("properties", {})
        nome = campo(props, "Nome", "title")
        if not nome:
            continue

        print(f"[{i}/{len(paginas)}] {nome}")

        registro = {
            "nome": nome,
            "nasc": campo(props, "Nascimento", "number"),
            "fale": campo(props, "Falecimento", "number"),
            "nacionalidade": campo(props, "Nacionalidade", "rich_text") or "",
            "profissao": campo(props, "Profissão", "rich_text") or "",
            "status": campo(props, "Status", "select") or "Servo de Deus",
            # campos opcionais, so aparecem se voce criar as colunas no Notion
            "localNasc": campo(props, "Local de nascimento", "rich_text") or "",
            "localRepouso": campo(props, "Local de sepultamento", "rich_text") or "",
        }

        registro["bio"] = biografia(pagina["id"])
        if not registro["bio"]:
            sem_bio.append(nome)

        if not registro["localNasc"] and not registro["localRepouso"]:
            sem_local.append(nome)

        url_foto = campo(props, "Foto", "files")
        if url_foto:
            arquivo = PASTA_IMG / f"{slug(nome)}.jpg"
            if baixar_foto(url_foto, arquivo):
                registro["foto"] = f"img/{arquivo.name}"
            else:
                sem_foto.append(nome)
        else:
            sem_foto.append(nome)

        santos.append(registro)

    santos.sort(key=lambda s: s["nome"])
    escrever_html(santos)
    relatorio(santos, sem_foto, sem_bio, sem_local)


def escrever_html(santos):
    html = TEMPLATE.read_text(encoding="utf-8")

    com_foto = sum(1 for s in santos if s.get("foto"))
    nota = (
        f"<strong>Sobre o catálogo.</strong> {len(santos)} santos, beatos, veneráveis e "
        f"servos de Deus catalogados, {com_foto} com foto. Os locais de nascimento e "
        f"sepultamento aparecem no mapa quando estão preenchidos no catálogo."
    )

    html = html.replace("/*__SAINTS_DATA__*/[]",
                        json.dumps(santos, ensure_ascii=False, indent=1))
    html = html.replace("<!--__FOOTER_NOTE__-->", nota)

    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "index.html").write_text(html, encoding="utf-8")

    tamanho = (SAIDA / "index.html").stat().st_size / 1024
    print(f"\nSite escrito em site/index.html ({tamanho:.0f} KB)")


def relatorio(santos, sem_foto, sem_bio, sem_local):
    print(f"\n{'='*56}\nRESUMO\n{'='*56}")
    print(f"  santos no site .......... {len(santos)}")
    print(f"  com foto ................ {len(santos) - len(sem_foto)}")
    print(f"  sem foto ................ {len(sem_foto)}")
    print(f"  sem biografia ........... {len(sem_bio)}")
    print(f"  sem local para o mapa ... {len(sem_local)}")

    def listar(titulo, nomes):
        if not nomes:
            return
        print(f"\n{titulo} ({len(nomes)}):")
        for n in nomes:
            print(f"  . {n}")

    listar("FALTA FOTO no Notion", sem_foto)
    listar("FALTA BIOGRAFIA no Notion", sem_bio)
    listar("FALTA LOCAL para o mapa", sem_local)
    print()


if __name__ == "__main__":
    montar()
