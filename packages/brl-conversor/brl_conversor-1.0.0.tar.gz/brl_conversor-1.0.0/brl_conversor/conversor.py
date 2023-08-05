import requests
import locale


class Conversor:
    """Conversor class helper:

    Responsible for connecting to awesome API 
    and download currency data from the chosen country code.
    Converts the currency of the country to Brazilian Real (BRL).
    Useful for Brazilian applications.

    Attributes:
        codein (str): BRL code to conversion.
        currencies (tuple): Tuple of allowed currencies.
        URL(str): Default URL for AwesomeAPI.
        data(dict): Dict that loads JSON data from AwesomeApi.
    """

    codein = "BRL" #: Default brazilian currency code
    currencies = ('USD', 'EUR', 'BTC') #: Allowed currencies
    URL = 'https://economia.awesomeapi.com.br/all/' #: AwesomeAPI

    def __init__(self, code):
        """Description of the __init__ method:

        The __init__ method is given a code as a parameter,
        and if it is not in the allowed currencies, it defaults to the US dollar.

        Args:
            code (str): Country currency code
        """
        locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8') #: Brazilian usage
        self.data = {} #: JSON data from API
        if code in self.currencies:
            self.code = code
        else:
            self.code = self.currencies[0]

    def __request_data(self):
        data = requests.get(self.URL + self.code)
        if data.status_code == 200:
            self.data = data.json()

    def converter(self, count):
        """
        Args:
            count(float): The amount of money you want to convert from a given currency to BRL.

        Returns:
            The total money, if the connection was a success, 
            0 if the connection is not successful.
        """

        self.__request_data()
        if self.data:
            str_value = self.data[self.code]['low']
            float_value = locale.atof(str_value)
            return count * float_value
        else:
            return 0

    def __str__(self):
        """String representing the current conversion"""
        return f"{code}-{codein}"