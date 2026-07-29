# Pixel Santo

Guia passo a passo. Você não precisa saber programar nem usar terminal.

Tudo o que você vai fazer é **clicar duas vezes em arquivos** e **copiar e colar
uma chave**.

---

# Passo 1. Pegar a chave do Notion

Isso é feito uma vez só na vida. Essa chave é o que deixa o site ler seu Notion.

**1.1** Abra este endereço no navegador:
https://www.notion.so/my-integrations

**1.2** Clique no botão escuro **New integration**.

**1.3** Preencha:
- Em *Name*, escreva: `Pixel Santo`
- Em *Associated workspace*, escolha seu workspace
- Clique em **Save**

**1.4** Na tela que abrir, procure o campo **Internal Integration Secret**.
Clique em **Show** e depois em **Copy**.

Você acabou de copiar a chave. Ela é um texto comprido que começa com `ntn_`.

> ⚠️ Essa chave dá acesso ao seu Notion. Não mande ela por e-mail, não cole em
> conversa com ninguém, nem aqui comigo. Você vai colar ela só numa janelinha do
> seu próprio Mac, no Passo 2.

**1.5** Agora falta liberar a página para essa integração. Sem isso não funciona.

- Abra a página **Pixel Santo** no Notion
- No canto superior direito, clique nos três pontinhos `•••`
- Procure **Conexões** (ou *Connections*)
- Clique em **Pixel Santo** para conectar
- Se aparecer uma confirmação, confirme

---

# Passo 2. Gerar o site

**2.1** Abra a pasta `pixel-santo`. Ela está na sua pasta de usuário.
Para chegar nela: abra o **Finder**, aperte as teclas `Command + Shift + H`
(isso abre sua pasta pessoal), e entre na pasta **pixel-santo**.

**2.2** Dentro dela, dê **dois cliques** no arquivo:

### 📄 `Gerar site.command`

**2.3** Vai abrir uma **janela preta com letras**. Isso é normal, não é erro.
Essa janela é o computador trabalhando. Não feche ela.

> Se o Mac disser que *"não pode abrir porque é de um desenvolvedor não
> identificado"*: clique com o **botão direito** no arquivo, escolha **Abrir**,
> e depois **Abrir** de novo na confirmação. Só precisa fazer isso na primeira vez.

**2.4** Vai aparecer uma janelinha pedindo a chave. **Cole a chave** que você
copiou no Passo 1.4 e clique em **Continuar**.

A chave fica guardada no Chaveiro do seu Mac. **Nas próximas vezes ele não vai
mais perguntar.**

**2.5** Agora espere. Ele vai baixar as fotos uma por uma, então pode levar
alguns minutos. Na janela preta vão aparecer os nomes dos santos sendo
processados.

**2.6** Quando terminar, aparece uma mensagem dizendo **Pronto** e a pasta
`site` abre sozinha na tela.

Na janela preta, no final, tem um resumo assim:

```
  santos no site .......... 84
  com foto ................ 39
  sem foto ................ 45
  sem biografia ........... 2
  sem local para o mapa ... 84
```

E embaixo, a lista de quais santos estão faltando o quê. **Esse é seu checklist
do que preencher no Notion.**

---

# Passo 3. Ver o site no seu computador

Antes de publicar, veja se ficou bom.

Dentro da pasta `site` que abriu, dê **dois cliques** no arquivo
**`index.html`**. Ele abre no seu navegador, funcionando de verdade, com as
fotos e os mapas.

Nessa etapa o site está só no seu computador. Ninguém mais vê ainda.

---

# Passo 4. Publicar na internet

**4.1** Abra este endereço no navegador:
https://app.netlify.com/drop

**4.2** Coloque as duas janelas lado a lado: o **Finder** com a pasta `site`
aberta, e o **navegador** na página do Netlify.

**4.3** Clique na pasta `site` e **arraste ela** com o mouse até o meio da
página do Netlify, onde está escrito para soltar arquivos. Aí solte.

> **Arrastar** é: apertar o botão do mouse em cima da pasta, manter apertado,
> mover o mouse até o outro lugar, e só então soltar o botão.
>
> Importante: arraste **a pasta `site` inteira**, não os arquivos de dentro dela.

**4.4** Ele vai subir os arquivos e mostrar um endereço tipo
`nome-aleatorio-123.netlify.app`. **Seu site está no ar.** Esse endereço já
funciona para qualquer pessoa.

**4.5** Para guardar esse site, o Netlify vai pedir para você criar uma conta.
É gratuito, dá para entrar com Google.

**4.6** Para trocar o endereço esquisito por algo bonito: em
**Site configuration > Change site name**, coloque `pixel-santo`. O endereço
vira `pixel-santo.netlify.app`.

---

# Como atualizar depois

Sempre que você mexer no Notion (adicionar foto, corrigir biografia, incluir
santo novo):

1. Dois cliques em **`Gerar site.command`** (não vai pedir a chave de novo)
2. Arraste a pasta `site` para o Netlify de novo, no seu site já criado, em
   **Deploys**

É isso. Duas ações.

---

# Se algo der errado

| O que aparece | O que fazer |
|---|---|
| `ERRO 401` | A chave está errada. Dois cliques em `Esquecer a chave.command` e faça o Passo 2 de novo. |
| `ERRO 404` | Falta conectar a integração na página do Notion. Volte no Passo 1.5. |
| `sem foto` na lista | Normal. Falta a foto daquele santo no campo **Foto** do Notion. |
| `sem local para o mapa` | Falta criar as colunas de local. Veja abaixo. |
| Mac não deixa abrir o arquivo | Botão direito no arquivo, **Abrir**, **Abrir**. |

---

# Sobre os mapas

Os mapas só aparecem quando o local está preenchido no Notion. Para isso
precisam existir duas colunas de texto na base, com **exatamente** estes nomes:

- `Local de nascimento`
- `Local de sepultamento`

Preencha com cidade e país, por exemplo `Assis, Itália`. Não precisa de endereço
nem de coordenada.

Onde estiver vazio, o site simplesmente não mostra mapa naquele santo. Não
quebra nada.

---

# O que é cada arquivo desta pasta

| Arquivo | Para que serve |
|---|---|
| `Gerar site.command` | **Você usa este.** Gera o site a partir do Notion. |
| `Esquecer a chave.command` | Use só se precisar trocar a chave do Notion. |
| `site/` | O site pronto. É esta pasta que vai para o Netlify. |
| `build.py` | O programa que faz o trabalho. Não precisa mexer. |
| `template.html` | O design do site. Não precisa mexer. |
| `LEIA-ME.md` | Este guia. |
