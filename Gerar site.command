#!/bin/bash
#
# Clique duas vezes neste arquivo para gerar o site Pixel Santo.
# Ele pede a chave do Notion na primeira vez e guarda no Chaveiro do Mac,
# entao nas proximas vezes nao pergunta mais nada.
#

cd "$(dirname "$0")" || exit 1

SERVICO="pixel-santo-notion"
CONTA="$USER"

titulo() {
  echo ""
  echo "════════════════════════════════════════════════"
  echo "  $1"
  echo "════════════════════════════════════════════════"
  echo ""
}

avisar() {
  # mostra uma janelinha de aviso
  osascript -e "display dialog \"$1\" buttons {\"OK\"} default button 1 with title \"Pixel Santo\"" >/dev/null 2>&1
}

# ---------------------------------------------------------------- 1. a chave

# tenta ler a chave que ja foi guardada no Chaveiro do Mac
TOKEN=$(security find-generic-password -a "$CONTA" -s "$SERVICO" -w 2>/dev/null)

if [ -z "$TOKEN" ]; then
  titulo "Primeira vez, preciso da chave do Notion"
  echo "Vou abrir uma janelinha pedindo a chave."
  echo "Ela fica guardada com seguranca no Chaveiro do seu Mac."
  echo ""

  PERGUNTA="Cole aqui a chave da sua integração do Notion.\n\nEla começa com ntn_ ou secret_\n\nSerá guardada no Chaveiro do seu Mac, com segurança. Você só precisa fazer isso uma vez."

  RESPOSTA=$(osascript -e "display dialog \"$PERGUNTA\" default answer \"\" with hidden answer with title \"Pixel Santo\" buttons {\"Cancelar\", \"Continuar\"} default button \"Continuar\"" 2>/dev/null)

  if [ -z "$RESPOSTA" ]; then
    titulo "Cancelado"
    echo "Nenhuma chave informada. Pode fechar esta janela."
    echo ""
    read -r -p "Aperte Enter para fechar. " _
    exit 0
  fi

  TOKEN="${RESPOSTA#*text returned:}"

  if [ -z "$TOKEN" ]; then
    avisar "Não recebi a chave. Tente clicar no arquivo de novo."
    exit 1
  fi

  # confere se parece mesmo com uma chave do Notion, para pegar erro de copiar e colar
  case "$TOKEN" in
    ntn_*|secret_*) ;;
    *)
      avisar "Isso não parece uma chave do Notion.

A chave começa com ntn_ ou com secret_

Confira se você copiou a chave inteira, em notion.so/my-integrations, no campo Internal Integration Secret."
      titulo "Chave em formato inesperado"
      echo "Nada foi guardado. Clique no arquivo de novo para tentar outra vez."
      echo ""
      read -r -p "Aperte Enter para fechar. " _
      exit 1
      ;;
  esac

  # guarda no Chaveiro (-U atualiza se ja existir)
  security add-generic-password -a "$CONTA" -s "$SERVICO" -w "$TOKEN" -U 2>/dev/null
  echo "Chave guardada no Chaveiro. Nas proximas vezes nao vou mais perguntar."
fi

# ---------------------------------------------------------------- 2. gerar

titulo "Gerando o site a partir do Notion"
echo "Isso pode levar alguns minutos, porque ele baixa as fotos uma por uma."
echo "Pode deixar rodando."
echo ""

export NOTION_TOKEN="$TOKEN"

if python3 build.py; then
  unset NOTION_TOKEN
  titulo "Pronto"
  echo "O site foi gerado na pasta 'site'."
  echo "Vou abrir a pasta para voce agora."
  echo ""
  open site
  avisar "Site gerado.

A pasta 'site' abriu na tela. É essa pasta que você vai arrastar para o Netlify.

Olhe o resumo na janela preta para ver quais santos ainda estão sem foto, sem biografia ou sem local."
else
  unset NOTION_TOKEN
  titulo "Deu erro"
  echo "Leia a mensagem acima para entender o que aconteceu."
  echo ""
  echo "Se falou em erro 401, a chave esta errada ou expirou."
  echo "Se falou em erro 404, falta conectar a integracao na pagina do Notion"
  echo "  (abra a pagina Pixel Santo, clique nos ... do canto, Conexoes)."
  echo ""
  echo "Para trocar a chave guardada, rode o arquivo 'Esquecer a chave.command'"
  echo "e depois este de novo."
fi

echo ""
read -r -p "Aperte Enter para fechar esta janela. " _
