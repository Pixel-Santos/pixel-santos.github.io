# Publicar o Pixel Santo no GitHub

Feito uma vez só. Depois disso o site se atualiza sozinho todo dia,
sem você precisar clicar em nada.

---

## Passo 1. Instalar o GitHub Desktop

Você não vai precisar de terminal em momento nenhum. O GitHub Desktop
é um programa com botões, igual qualquer outro.

**1.1** Abra https://desktop.github.com e clique em **Download**.

**1.2** Abra o arquivo baixado e arraste o GitHub Desktop para a pasta
Aplicativos, como faz com qualquer programa.

**1.3** Abra o GitHub Desktop. Ele vai pedir para você entrar na sua
conta do GitHub. Se ainda não tem conta, crie em https://github.com/signup
(é gratuita).

---

## Passo 2. Mandar o projeto para o GitHub

**2.1** No GitHub Desktop, no menu de cima, clique em **File** e depois
em **Add Local Repository**.

**2.2** Clique em **Choose** e escolha a pasta **pixel-santo**, que fica
dentro da sua pasta de usuário. Clique em **Add Repository**.

**2.3** Ele vai mostrar o projeto. No canto superior direito vai aparecer
um botão azul escrito **Publish repository**. Clique nele.

**2.4** Vai abrir uma janelinha. Aqui tem um detalhe importante.

- Em **Name**, deixe `pixel-santo`
- **Desmarque** a caixinha **Keep this code private**

Precisa ser público, porque o site gratuito do GitHub só funciona assim.
Fique tranquila, sua chave do Notion **não** está no projeto, ela mora só
no seu Mac. O que fica público é o site e o código, que é o que você quer
mostrar mesmo.

**2.5** Clique em **Publish Repository** e espere. São 7 MB de fotos,
leva um minutinho.

---

## Passo 3. Ligar o site

**3.1** No GitHub Desktop, no menu de cima, clique em **Repository** e
depois em **View on GitHub**. Vai abrir seu projeto no navegador.

**3.2** Na barra de cima da página, clique em **Settings**.

**3.3** Na coluna da esquerda, procure e clique em **Pages**.

**3.4** Onde está escrito **Source**, troque de `Deploy from a branch`
para **GitHub Actions**. Só isso, não precisa salvar nada.

**3.5** Volte para a aba **Actions**, lá em cima. Você vai ver o
"Publicar o site" rodando. Quando ficar com o sinal verde, seu site
está no ar.

O endereço vai ser algo como:
`https://SEUUSUARIO.github.io/pixel-santo`

---

## Passo 4. Deixar o site se atualizar sozinho

Esse passo faz o site buscar o Notion todo dia de manhã sozinho.
Se você pular, o site funciona igual, só não atualiza automático.

**4.1** No seu projeto no GitHub, clique em **Settings**.

**4.2** Na coluna da esquerda, clique em **Secrets and variables** e
depois em **Actions**.

**4.3** Clique no botão verde **New repository secret**.

**4.4** Em **Name**, escreva exatamente:

    NOTION_TOKEN

**4.5** Em **Secret**, cole a mesma chave do Notion que você usou no
`Gerar site.command`. Ela começa com `ntn_`.

**4.6** Clique em **Add secret**.

Pronto. Todo dia às 9h da manhã o site vai ler seu Notion e se atualizar.
Se quiser forçar na hora, vá na aba **Actions**, clique em
**Publicar o site** e depois em **Run workflow**.

---

## E no dia a dia, como fica

Você tem dois caminhos, e pode usar os dois.

**Só mexer no Notion.** Escreve lá e espera. No dia seguinte o site já
está atualizado sozinho. Não precisa abrir o computador nem clicar nada.

**Querer ver na hora.** Dois cliques em `Gerar site.command` como sempre,
e depois, no GitHub Desktop, clique em **Push origin** no topo. Em um
minuto o site no ar já está novo.

---

## Se algo der errado

| O que aparece | O que fazer |
|---|---|
| A aba Actions fica vermelha | Clique no erro e me mande o print. Quase sempre é a chave do Notion faltando ou escrita errada. |
| O site abre sem as fotos | Espere alguns minutos, o Pages demora para propagar na primeira vez. |
| "Publish repository" não aparece | Confirme que você está logada no GitHub Desktop, em File e Options. |
| Deu erro de permissão no push | No GitHub, vá em Settings, Actions, General, e em Workflow permissions marque Read and write permissions. |
