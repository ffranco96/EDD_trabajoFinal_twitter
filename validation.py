import re


def is_username_format_valid(username: str) -> bool:
    """
    Valida si username tiene formato valido para twitter
    @param username: username a validar
    @return: true si valida la expresión regular
    """
    return re.search(r'^(?=.{1,15}$)(^\w+$)', username) is not None


def is_date_format_valid(date: str) -> bool:
    """
    Valida si la fecha ingresada está en formato YYYYMMDD HHMMSS
    Con 15 caracteres exactos de longitud
    @param date: fecha a validar
    @return: true si valida la expresión regular
    """
    # TODO mejorar regEx para que la fecha tenga sentido, EJ: no tratar de formatear 40 de Febrero, etc.
    return re.search(r'^(?=.{15}$)\d{4}[0-1]?\d[0-3]?\d (?:2[0-3]|[01]?\d)[0-5]?\d[0-5]?\d', date) is not None


def is_max_results_valid(number: str) -> bool:
    return re.search(r'^\d*$', number) is not None


def is_input_valid(input_str: str) -> bool:
    return re.search(r'^[SsNn]*$', input_str) is not None
