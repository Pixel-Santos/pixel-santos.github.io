# Estado da extração do Notion

Objetivo: gerar `site/index.html` com os 84 santos, a partir de `template.html`.

- `santos.json` é a fonte de verdade em construção. Cada santo tem
  nome, nasc, fale, nacionalidade, profissao, status, slug, pageId,
  temFoto, bio (lista de parágrafos), foto (url original), localNasc, localRepouso.
- `faltam.txt` lista `pageId<TAB>nome` de quem ainda não tem bio.
- Para cada pageId faltante, usar a ferramenta Notion `fetch` e extrair
  do bloco `<content>` os parágrafos (separados por `<br>`), ignorando as
  linhas `![](...)` de imagem. A url real da foto está na propriedade
  `Foto`, dentro do JSON url-encoded, na chave `source`.
- As bios são texto da Amanda. Copiar verbatim, sem reescrever.
- Ao final: baixar as fotos para `site/img/<slug>.jpg`, comprimir com sips,
  e injetar os dados em `/*__SAINTS_DATA__*/[]` do template.
