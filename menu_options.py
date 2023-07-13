import util
import validation


def filter_tweets(tweets: list,
                  search_by_user: bool = False,
                  search_by_start_date: bool = False,
                  search_by_end_date: bool = False,
                  search_max_results: bool = False) -> list:
    """
    Filtra la lista de tweets ingresada en función de los parámetros opcionales.
    @param tweets: Lista de tweets a filtrar
    @param search_by_user: Si es true, filtrará tweets por username ingresado por el usuario
    @param search_by_start_date: Si es true, filtrará tweets por fecha de inicio ingresada por el usuario
    @param search_by_end_date: Si es true, filtrará tweets por fecha tope ingresada por el usuario
    @param search_max_results: Si es true, filtra hasta una cantidad máxima de resultados a determinar por el usuario.
    Por defecto devuelve hasta 10 resultados. Si se ingresa 0 o menor, devuelve la cantidad máxima de resultados.
    @return: Lista filtrada.
    """
    max_results = 10

    if search_max_results:
        max_results = input("Ingrese la cantidad máxima de resultados a buscar (por defecto 10): ")
        while validation.is_max_results_valid(max_results) is False:
            max_results = input("Intente nuevamente.\nIngrese un número entero: ")

    if search_by_user:
        user = input("Ingrese nombre de usuario a buscar (sin @): ")
        while validation.is_username_format_valid(user) is False:
            user = input(
                "Intente nuevamente.\n"
                "El nombre de usuario debe ser de 1 a 15 caracteres, alfanumérico y puede tener \"_\" (guión bajo): ")
        tweets = util.filter_by_user(tweets, user)

    if search_by_start_date:
        start_date = input("Ingrese la fecha de inicio, formato YYYYMMDD HHMMSS: ")
        while validation.is_date_format_valid(start_date) is False:
            start_date = input(
                "Intente nuevamente.\n"
                "La fecha debe estar en formato YYYYMMDD HHMMSS con un \" \" (espacio) entre medio: ")
        tweets = util.filter_by_start_date(tweets, start_date)

    if search_by_end_date:
        end_date = input("Ingrese la fecha de fin, formato YYYYMMDD HHMMSS: ")
        while validation.is_date_format_valid(end_date) is False:
            end_date = input(
                "Intente nuevamente.\n"
                "La fecha debe estar en formato YYYYMMDD HHMMSS con un \" \" (espacio) entre medio: ")
        tweets = util.filter_by_end_date(tweets, end_date)

    if int(max_results) >= 0:
        tweets = util.filter_by_max_results(tweets, int(max_results))

    return tweets
