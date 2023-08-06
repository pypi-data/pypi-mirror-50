import requests
from fuzzywuzzy import fuzz


class Lookup:
    def __init__(self):
        self.data = self.get_data()

    @staticmethod
    def get_data(
        url="https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.json"
    ):
        return requests.get(url).json()

    @staticmethod
    def conf_exists(l, var, value):
        if len(l) > 0:
            return l[0][var]
        raise ValueError(value + " does not exist in lookup data.")

    @staticmethod
    def get_fuzz(v, country, var):
        v["ratio"] = fuzz.partial_ratio(v[var].lower(), country.lower())
        return v

    @staticmethod
    def get_max(data):
        return max([v["ratio"] for v in data])

    @staticmethod
    def filter_data(data, cutoff=50):
        return [v for v in data if v["ratio"] > cutoff]

    def max_data(self, data):
        return self.get_max(data), self.filter_data(data)
