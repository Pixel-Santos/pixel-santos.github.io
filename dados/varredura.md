# Varredura final, 30/07/2026

Rodada sobre o site gerado as 12h11, ou seja, ja com as fotos, os locais
e os nomes novos.

## Numeros
- 84 santos, 84 com foto, 84 com biografia
- 84 com local de nascimento, 79 com local de sepultamento
- 32 biografias 100% conformes (4 paragrafos, sem travessao, sem dois pontos)

## Corrigido nesta varredura
- **Emil Kapaun**: sobrou um paragrafo antigo com a citacao longa de John
  McHugh, porque meu old_str da reescrita nao cobriu aquele bloco. Reescrevi
  a citacao dentro do 4o paragrafo e removi o bloco solto.
- **Josemaria Escriva**: "escondendo se", "disfarcando se" e "dedicou se"
  ganharam hifen. Nome no texto corrigido para Josemaria com acento.
- **Madre Teresa de Calcuta**: "tornou se" ganhou hifen.

## Falsos positivos do detector de pronome, nao mexer
"continuou se envolvendo", "quando se provou", "aspirando se tornar".
Sao proclise, o pronome vem antes do verbo e nao leva hifen.

## Ainda pendente, 52 biografias nunca reescritas
Delas, 17 tem travessao, 13 tem dois pontos e a maioria esta em 3 paragrafos.
Isso e o esperado, sao as que ficaram na fila da padronizacao.
Faltam ainda os pronomes sem hifen em Jacques Fesch e Papa Joao Paulo II,
que serao corrigidos quando essas duas forem reescritas.

## Licao aprendida em 30/07 sobre replace_all_matches
No Francisco Marto usei replace_all_matches para remover um bloco solto e
ele apagou tambem a frase identica que eu tinha acabado de inserir no
paragrafo anterior, sumindo com a morte dele. Nunca usar replace_all quando
o texto novo repete o texto antigo. Corrigido no mesmo minuto.

## Licao aprendida em 31/07, e esta e grave
Quando se manda VARIAS content_updates numa mesma chamada, o Notion pode
aplicar so as que casaram e ainda assim responder sucesso. Uma que nao casa
NAO derruba a chamada. Foi o que aconteceu no Frei Damiao, onde a segunda
substituicao falhou calada por causa de um erro meu na palavra veneravel, e
o texto ficou com uma frase duplicada.
REGRA: depois de qualquer chamada com mais de uma substituicao, conferir a
pagina com notion-fetch antes de marcar como pronta.

## Fotos que sumiam sem motivo aparente, 06/08
Seis santos ficaram sem foto no site mesmo tendo link valido no Notion:
Rosario Livatino, Marie-Clementine, Antonietta Meo, Papa Joao Paulo I,
Pier Giorgio Frassati e Gemma Galgani.

Nao era link quebrado. Testado na mao, o link do Livatino baixa 200 OK com
70 KB e o sips comprime sem erro. A causa era o build.py nao ter NENHUMA
repeticao de tentativa: uma falha momentanea de rede, ou o limite de taxa
do Wikimedia ao baixar 86 imagens em sequencia, derrubava a foto daquele
santo para sempre naquela geracao.

Corrigido com quatro tentativas e espera crescente, mais uma pausa de 0,4s
entre downloads. Como o efeito e aleatorio, os santos afetados mudam a cada
geracao, o que explica por que a lista de hoje e diferente da de 30/07.
