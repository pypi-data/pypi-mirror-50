# hgfinance

**hgfinance** é uma API de finanças da HG brasil, este pacote em Python tem por objetivo facilitar o acesso de requisições a esta API. Por meio de uma chave pessoal e única que deve ser fornecida opcionalmente pelo usuário do pacote.

## Sobre o acesso

O acesso a API é totalmente definido pela chave de API, que você pode adquirir gratuitamente, ou comprar um plano no site da HG brasil.
Quaisquer dúvidas sobre a API, visite o site [HG brasil](https://hgbrasil.com/).

## Uso

Para começar a utilizar o pacote você deve instalá-lo via pip:
`pip install hgfinance`

Exemplo de conexão:

````
from hgfinance import HgFinanceConnection

conn = HgFinanceConnection()

conn.set_key_api('SUA-CHAVE')

quotations = conn.quotations_only_requisition() # cotações de moeda
````

**Atenção**: Para acessar dados históricos da API, é necessário comprar um plano de membro no site da HG brasil. 
