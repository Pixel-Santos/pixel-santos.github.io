# Pixel Santo

Site do catálogo de santos modernos, gerado a partir da sua base do Notion.

Você edita tudo no Notion. O site se atualiza a partir de lá.

---

## Como funciona

```
    Notion (sua base "S A N T O S")
              │
              ▼
        build.py  ← lê o Notion, baixa as fotos
              │
              ▼
     site/  (index.html + img/)
              │
              ▼
     Netlify  →  seu site no ar
```

O arquivo `template.html` é o design. O `build.py` preenche o design com os
dados do Notion. Você nunca precisa mexer nesses dois para trocar conteúdo,
só no Notion.

---

## Parte 1. Dar acesso do Notion ao site

Isso é feito uma vez só.

1. Abra https://www.notion.so/my-integrations e clique em **New integration**.
2. Dê o nome `Pixel Santo`, escolha seu workspace e salve.
3. Copie a chave que aparece (começa com `ntn_` ou `secret_`).
   **Guarde num lugar seguro, tipo seu gerenciador de senhas. Essa chave dá
   acesso ao seu Notion, então não mande por e-mail nem cole em conversa.**
4. Abra a página **Pixel Santo** no Notion, clique nos `...` do canto superior
   direito, vá em **Conexões** (ou *Connections*) e adicione a integração
   `Pixel Santo`. Sem esse passo o site recebe erro 404.

---

## Parte 2. Gerar o site no seu computador

No Terminal:

```bash
cd ~/pixel-santo
export NOTION_TOKEN='cole_sua_chave_aqui'
python3 build.py
```

O `export` vale só para aquela janela do Terminal. Se fechar e abrir de novo,
precisa repetir.

Ao terminar ele mostra um resumo assim:

```
  santos no site .......... 84
  com foto ................ 39
  sem foto ................ 45
  sem biografia ........... 2
  sem local para o mapa ... 84
```

E lista os nomes que estão faltando alguma coisa. Use essa lista como
checklist do que preencher no Notion.

---

## Parte 3. Colocar no ar

A primeira vez, do jeito mais simples e sem instalar nada:

1. Entre em https://app.netlify.com/drop
2. Arraste a pasta `site` (que o build.py criou) para dentro da página.
3. Pronto, o site está no ar num endereço tipo `algo-aleatorio.netlify.app`.
4. Em **Site configuration > Change site name** você troca por
   `pixel-santo.netlify.app`.

Para atualizar depois: rode o `build.py` de novo e arraste a pasta `site`
novamente. Substitui o que estava lá.

### Domínio próprio (opcional)

Se quiser `pixelsanto.com.br`, compre em registro.br (por volta de R$ 40 por
ano) e em **Domain management** no Netlify siga o passo a passo dele para
apontar. O Netlify já dá o certificado de segurança de graça.

---

## Parte 4. Atualização automática (opcional, depois)

Enquanto você roda o `build.py` na mão, o site não é automático. Para ele se
atualizar sozinho a partir do Notion, o caminho é subir esta pasta para o
GitHub e usar o arquivo `.github/workflows/atualizar.yml` que já está pronto
aqui. Ele roda o `build.py` todos os dias de manhã e também tem um botão de
"rodar agora".

Nesse caminho a chave do Notion vai em **Settings > Secrets and variables >
Actions > New repository secret**, com o nome `NOTION_TOKEN`. Você mesma cola
ela lá, no site do GitHub. Ela fica escondida, não aparece no código.

---

## Colunas do Notion que o site usa

| Coluna no Notion        | Onde aparece no site                        |
|-------------------------|---------------------------------------------|
| Nome                    | título do cartão                            |
| Nascimento              | ano no cartão                               |
| Falecimento             | ano no cartão                               |
| Nacionalidade           | cartão, com a bandeira do país              |
| Profissão               | cartão                                      |
| Status                  | estágio de canonização (as bolinhas)        |
| Foto                    | imagem do cartão                            |
| corpo da página         | biografia, ao clicar no santo               |
| Local de nascimento     | mapa (coluna ainda não existe, ver abaixo)  |
| Local de sepultamento   | mapa (coluna ainda não existe, ver abaixo)  |

### Sobre os mapas

Os mapas só aparecem quando o local está preenchido. Para isso é preciso criar
duas colunas de texto na base do Notion, com estes nomes exatos:

- `Local de nascimento`
- `Local de sepultamento`

Preencha com cidade e país, por exemplo `Assis, Itália`. Não precisa de
endereço nem coordenada. Onde estiver vazio, o site simplesmente não mostra
mapa, sem quebrar nada.
