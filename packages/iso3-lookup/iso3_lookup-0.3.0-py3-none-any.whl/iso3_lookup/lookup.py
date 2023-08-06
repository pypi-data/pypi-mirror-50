from iso3_lookup.data import all


def conf_exists(l, var, value):
    if len(l) > 0:
        return l[0][var]
    raise ValueError(value + " does not exist in lookup data.")


def get_iso3(country):
    return conf_exists(
        [v for v in all if v["name"].lower() == country.lower()], "alpha-3", country
    )


def get_country(iso3):
    return conf_exists(
        [v for v in all if v["alpha-3"].lower() == iso3.lower()], "name", iso3
    )
