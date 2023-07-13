import json
import os
import sys
from datetime import datetime

from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError, HydrateType, OAuthType

import menu_options
import util
import validation

salir = False

QUERY = 'guerra ucrania OR guerra rusia'
EXPANSIONS = 'author_id'
TWEET_FIELDS = 'author_id,created_at,id,text'
USER_FIELDS = 'name,username'


def get_info_dir():  # @todo debe modificar la query QUERY de forma que busque por ese parametro
    "Se obtiene el directorio de la carpeta /trabajo-practico-fizzbuzz_v2 en tu PC"  # Setear el path segun la pc del usuario que ejecuta
    dir = os.getcwd()
    dir_persistencia = os.path.join(dir, "info_recuperada")
    return dir_persistencia


def get_date_time():  # @todo debe modificar la query QUERY de forma que busque por ese parametro
    now = datetime.now()
    format = now.strftime('\nFecha y Hora de Inicio: %d-%m-%Y %H:%M:%S \n')
    print(format)


def pedir_numero_entero_opcion_menu():
    correcto = False
    num = None
    while (not correcto):
        try:
            num = int(input("Elegir opcion: "))
            if num == 0:
                sys.exit('Ingreso 0, saliendo del programa....')
            else:
                correcto = True
        except ValueError:
            print('Introduce 0 para salir, o elija una opcion valida')
    return num


def stream_tweets(query, expansions, tweet_fields, user_fields, tweets_qtty):
    cant_tweets_recolectados = 0

    try:
        get_date_time()
        nombre_archivo = input("Ingrese un nombre para guardar los tweets recuperados: ")
        path = get_info_dir() + f"\\ {nombre_archivo}.json"
        o = TwitterOAuth.read_file()
        api = TwitterAPI(o.consumer_key, o.consumer_secret, auth_type=OAuthType.OAUTH2, api_version='2')

        # DELETE STREAM RULES
        r = api.request("tweets/search/stream/rules", method_override="GET")
        rules = r.json()
        if "data" in rules:
            ids = list(map(lambda rule: rule["id"], rules["data"]))
            api.request("tweets/search/stream/rules", {"delete": {"ids": ids}})

        # ADD STREAM RULES

        r = api.request('tweets/search/stream/rules', {'add': [{'value': QUERY}]})
        print(f'[{r.status_code}] RULE ADDED: {json.dumps(r.json(), indent=2)}\n')
        if r.status_code != 201: exit()

        # GET STREAM RULES

        r = api.request('tweets/search/stream/rules', method_override='GET')
        print(f'[{r.status_code}] RULES: {json.dumps(r.json(), indent=2)}\n')
        if r.status_code != 200: exit()

        # START STREAM

        r = api.request('tweets/search/stream', {
            'expansions': EXPANSIONS,
            'tweet.fields': TWEET_FIELDS,
            'user.fields': USER_FIELDS,
        },
                        hydrate_type=HydrateType.APPEND)

        print(f'[{r.status_code}] START...')
        if r.status_code != 200: exit()
        for item in r:
            cant_tweets_recolectados = cant_tweets_recolectados + 1
            with open(path, "a", encoding="utf-8") as file:
                file.write(json.dumps(item) + "\n")
            archivo_bytes = os.path.getsize(path)
            print("Cantidad de Bytes recuperados en Disco: " + str(archivo_bytes))
            print("\nCantidad de Tweets guardados: " + str(cant_tweets_recolectados))
            if tweets_qtty <= 0:  # -- No se establece limite de tweets
                continue
            elif cant_tweets_recolectados >= tweets_qtty:
                print('Se completo la obtencion de ' + str(tweets_qtty) + " tweets")
                break

    except KeyboardInterrupt:
        print('\nDone!')
        return r
    except TwitterRequestError as e:
        print(f'\n{e.status_code}')
        for msg in iter(e):
            print(msg)

    except TwitterConnectionError as e:
        print(e)

    except Exception as e:
        print(e)


while not salir:

    print("\n****Menu Principal FizzBuzz****")
    print("\n")
    print("1- Recolectar Tweets sobre " + str(QUERY))
    print("2- Buscar Tweets en disco")
    print("3- Consultas booleanas de Tweets por Frases o Palabras ")
    print("4- Estadisticas ")
    print("0- Terminar programa ")
    print("\n")
    opcion = pedir_numero_entero_opcion_menu()

    if opcion == 1:
        try:
            cant_a_recuperar = int(input(
                "\nElija cantidad de tweets a recuperar, cero o neg para recuperar hasta que el usuario finalice: "))
        except ValueError:
            print('Opcion invalida')
        else:
            r = stream_tweets(QUERY, EXPANSIONS, TWEET_FIELDS, USER_FIELDS,
                              cant_a_recuperar)  # @todo QUERY debe ser modificado segun la opcion ingresada
    elif opcion == 2:

        tweets_a_filtrar = []

        while True:
            try:
                filename = f'{os.getcwd()}/info_recuperada/{input("Ingrese nombre del archivo: ")}.json'
                tweets_a_filtrar = util.load_tweets(filename)
            except FileNotFoundError:
                print("Intente nuevamente")
                continue
            break

        search_by_user = input("¿Realizar búsqueda por usuario? (S/N): ")
        while validation.is_input_valid(search_by_user) is False:
            search_by_user = input("Ingrese S o N: ")

        search_by_start_date = input("¿Realizar búsqueda por fecha inicial? (S/N): ")
        while validation.is_input_valid(search_by_start_date) is False:
            search_by_start_date = input("Ingrese S o N: ")

        search_by_end_date = input("¿Realizar búsqueda por fecha final? (S/N): ")
        while validation.is_input_valid(search_by_end_date) is False:
            search_by_end_date = input("Ingrese S o N: ")

        search_max_results = input("¿Cambiar cantidad máxima de resultados? (S/N): ")
        while validation.is_input_valid(search_max_results) is False:
            search_max_results = input("Ingrese S o N: ")

        tweets_filtrados = menu_options.filter_tweets(tweets_a_filtrar,
                                                      search_by_user=util.convert_input(search_by_user),
                                                      search_by_start_date=util.convert_input(search_by_start_date),
                                                      search_by_end_date=util.convert_input(search_by_end_date),
                                                      search_max_results=util.convert_input(search_max_results))

        texto_extraido = util.extract_key(tweets_filtrados, 'text')

        print(f'\nCantidad de tweets obtenidos: {str(len(texto_extraido))}\n')
        print(f'{json.dumps(texto_extraido, indent=2)}')

    elif opcion == 3:
        while not salir:
            print("\nMenu Consultas Booleanas")
            print("\n")
            print("1- Operador AND")
            print("2- Operador OR ")
            print("3- Operador NOT ")
            print("0- Terminar programa ")
            print("\n")
        opcion = pedir_numero_entero_opcion_menu()

    elif opcion == 4:  # Entregable opcional de estadisticas
        while not salir:
            print("\nMenu Estadisticas")
            print("\n")
            print("1- Las 10 palabras mas usadas en todos los twitts recuperados")
            print("2- Las 10 palabras mas usadas por el usuario ingresado")
            print("3- Ranking de las n palabras mas usadas ")
            print("0- Terminar programa ")
            print("\n")
        opcion = pedir_numero_entero_opcion_menu()

    elif opcion == 0:
        salir = True
    else:
        print("Introduce una opcion valida")

if __name__ == '__main__':
    pedir_numero_entero_opcion_menu()
