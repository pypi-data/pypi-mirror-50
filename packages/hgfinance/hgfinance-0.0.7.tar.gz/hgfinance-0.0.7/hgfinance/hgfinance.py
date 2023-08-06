import requests

DEFAULT_URL = 'https://api.hgbrasil.com/finance?key={}'
SYMBOL_URL = 'https://api.hgbrasil.com/finance/stock_price?key={}&symbol={}'
QUOTATIONS_URL = 'https://api.hgbrasil.com/finance/quotations?key={}'
TAXES_URL = 'https://api.hgbrasil.com/finance/taxes?key={}'
HISTORICAL_DATA_URL = 'https://api.hgbrasil.com/finance/historical?key={}&days_ago={}&mode={}'


class HgFinanceConnection:
    """classe HgFinanceConnection:

    Responsável por se conectar a API HG finance, e
    retornar dicionários de acordo com a chave e requisição solicitada.

    Attributes:
        __key_api(str): É a chave opcional de acesso dos dados da API.
    """

    def __init__(self, key_api=''):
        """Descrição do método __init__:

        O método __init__ recebe opcionalmente uma chave de API,
        para acessar determinados dados.

        Args:
            key_api (str): É a chave opcional da API. String vazia por padrão.
        """
        self.__key_api = key_api

    def set_key_api(self, new_key):
        """
        Args:
            new_key(str): Nova chave da conexão.
        """

        self.__key_api = new_key

    def __connection_has_error(self, json_response):
        """
        Verifica a existência da chave 'error' vinda da API,
        em caso positivo é levantada uma exceção com a mensagem da API.
        """
        if 'error' in json_response['results'].keys():
            raise Exception(json_response['results']['message'])

    def default_requisition(self):
        """
        Returns:
            O dicionário com os dados da requisição padrão.
        """
        request = requests.get(DEFAULT_URL.format(self.__key_api))
        return request.json()

    def symbol_requisition(self, symbol):
        """
        Args:
            symbol(str): Representa a empresa. Como petr4 para Petrobrás.
        Returns:
            O dicionário com os dados da requisição de símbolos.
            Apenas um símbolo pode ser requisitado por vez.
        """
        request = requests.get(SYMBOL_URL.format(self.__key_api, symbol))
        if 'error' in request.json()['results'][symbol.upper()].keys():
            raise Exception(request.json()['results'][symbol.upper()]['message'])
        return request.json()

    def quotations_only_requisition(self):
        """
        Returns:
            O dicionário com os dados da requisição das cotações.
        """

        request = requests.get(QUOTATIONS_URL.format(self.__key_api))
        return request.json()

    def taxes_only_requisition(self):
        """
        Returns:
            O dicionário com os dados da requisição das taxas.
        """
        if not self.__key_api:
            raise Exception('Chave de API requerida.')
        request = requests.get(TAXES_URL.format(self.__key_api))
        return request.json()

    def historical_data_requisition(self, days_ago=3, mode='all'):
        """
        Returns:
            O dicionário com os dados da requisição de dados históricos.
            Requer chave com plano pago.
        """
        request = requests.get(HISTORICAL_DATA_URL.format(
            self.__key_api, days_ago, mode))

        self.__connection_has_error(request.json())

        return request.json()
