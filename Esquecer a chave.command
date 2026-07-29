#!/bin/bash
#
# Clique duas vezes aqui se precisar trocar a chave do Notion.
# Isso apaga a chave guardada no Chaveiro do Mac. Nada mais e apagado.
#

SERVICO="pixel-santo-notion"

security delete-generic-password -a "$USER" -s "$SERVICO" >/dev/null 2>&1

echo ""
echo "════════════════════════════════════════════════"
echo "  Chave esquecida"
echo "════════════════════════════════════════════════"
echo ""
echo "Na proxima vez que voce clicar em 'Gerar site.command',"
echo "ele vai pedir a chave do Notion de novo."
echo ""
read -r -p "Aperte Enter para fechar esta janela. " _
