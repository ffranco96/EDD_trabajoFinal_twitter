import json
from datetime import datetime


def load_tweets(filename: str) -> list:
    """
    Lee archivo y devuelve el contenido como una lista
    :param filename: ruta al archivo a leer
    :return: lista con tweets
    """
    try:
        data = []
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line))
        return data
    except FileNotFoundError:
        print("El archivo ingresado no existe!")
        raise


def filter_by_user(tweets: list, target_user: str) -> list:
    """
    Filtra lista de tweets por nombre de usuario
    :param tweets: lista de tweets
    :param target_user: usuario objetivo
    :return: lista de tweets filtrada por usuario
    """
    return [tweet for tweet in tweets if tweet['data']['author_id_hydrate']['username'] == target_user]


def filter_by_start_date(tweets: list, target_date: str) -> list:
    """
    Filtra lista de tweets por aquellos cuya fecha es igual o posterior a la fecha ingresada
    :param tweets: lista de tweets
    :param target_date: fecha inicial objetivo
    :return: lista de tweets filtrada por fecha inicial
    """
    return [tweet for tweet in tweets if
            datetime.strptime(tweet['data']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ") >= datetime.strptime(target_date,
                                                                                                         "%Y%m%d %H%M%S")]


def filter_by_end_date(tweets: list, target_date: str) -> list:
    """
    Filtra lista de tweets por aquellos cuya fecha es menor a la fecha ingresada
    :param tweets: lista de tweets
    :param target_date: fecha final objetivo
    :return: lista de tweets filtrada por fecha final
    """
    return [tweet for tweet in tweets if
            datetime.strptime(tweet['data']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.strptime(target_date,
                                                                                                        "%Y%m%d %H%M%S")]


def filter_by_max_results(tweets: list, target_max_results: int) -> list:
    """
    Devuelve los primeros n elementos de la lista dada por parámetro
    @param tweets: Lista de tweets
    @param target_max_results: cantidad máxima objetivo
    @return: Lista conteniendo los primeros n parámetros elementos de la lista inicial.
    """
    return tweets[:target_max_results]


def convert_input(input_str: str) -> bool:
    return input_str in ["S", "s"]


def extract_key(tweets: list, key_to_extract: str) -> list:
    """
    Devuelve lista conteniendo sólo los pares clave-valor especificado por parámetro, dentro del atributo "data" de la
    lista ingresada.
    @param tweets: Lista a filtrar. Se espera que cada tweet contenga la clave "data" en el nivel más alto.
    @param key_to_extract: Clave a extraer
    @return: Lista sólo conteniendo un par clave-valor por elemento de la lista original
    """
    new_tweet_list = []
    for tweet in tweets:
        new_tweet = {k: v for k, v in tweet["data"].items() if k.startswith(key_to_extract)}
        new_tweet_list.append(new_tweet)

    return new_tweet_list
