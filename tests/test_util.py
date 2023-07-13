import os
from datetime import datetime

import pytest
import util


@pytest.fixture
def target_format():
    return "%Y-%m-%dT%H:%M:%S.%fZ"


@pytest.fixture
def sample_tweet():
    return {
        "data": {
            "author_id": "292637648",
            "created_at": "2022-11-01T22:48:03.000Z",
            "edit_history_tweet_ids": [
                "1587577235896238082"
            ],
            "id": "1587577235896238082",
            "text": "Pitoniso pero dejó por fuera la guerra Rusia-Ucrania, el alza de tasas por la reserva federal la consecuente del Banco de la REpública, la migración de golondrinas y saboteadores el encarecimiento derivado de las importaciones. ES decir ni pito ni niso https://t.co/MSEX0GWEkZ",
            "author_id_hydrate": {
                "id": "292637648",
                "name": "Guillermo Segovia M.",
                "username": "segoviamora"
            }
        }
    }


@pytest.fixture
def sample_json():
    return util.load_tweets(os.getcwd() + "/test_files/test6.json")


def test_filter_by_user(sample_json, sample_tweet):
    # Sólo existe 1 tweet dentro del json de prueba que pertenece al usuario @MaicolE44184284

    data = [sample_tweet]

    result = util.filter_by_user(sample_json, "segoviamora")

    assert result[0]['data']['author_id_hydrate']['username'] == data[0]['data']['author_id_hydrate']['username']
    assert len(result) == 1


def test_filter_by_start_date(sample_json, target_format):
    # Sólo existe 1 tweet dentro del json de prueba posterior a la fecha "2022-11-01T22:48:16.000Z"

    result = util.filter_by_start_date(sample_json, "20221101 224816")

    assert datetime.strptime(result[0]['data']['created_at'], target_format) >= datetime.strptime(
        "2022-11-01T22:48:16.000Z", target_format)
    assert len(result) == 1


def test_filter_by_end_date(sample_json, target_format):
    # Sólo existe 1 tweet dentro del json de prueba anterior a la fecha "2022-11-01T22:48:03.000Z"

    result = util.filter_by_end_date(sample_json, "20221101 224804")

    assert datetime.strptime(result[0]['data']['created_at'], target_format) < datetime.strptime(
        "2022-11-01T22:48:04.000Z", target_format)
    assert len(result) == 1


def test_empty_tweet_list():
    sample_list = []

    result = util.filter_by_user(sample_list, "galedesma")

    assert result == []


def test_max_results(sample_json):
    result = util.filter_by_max_results(sample_json, 1)

    assert len(result) == 1


def test_extract_text(sample_json):
    # Se filtra la lista para obtener sólo la clave "text" de cada tweet.
    result = util.extract_key(sample_json, 'text')

    expected = [{
        "text":
            "Pitoniso pero dej\u00f3 por fuera la guerra Rusia-Ucrania, el alza de tasas por la reserva federal la consecuente del Banco de la REp\u00fablica, la migraci\u00f3n de golondrinas y saboteadores el encarecimiento derivado de las importaciones. ES decir ni pito ni niso https://t.co/MSEX0GWEkZ"
    }, {
        'text':
            'RT @MundoEConflicto: 🇺🇸 | Presidente Joe Biden: "La inflación es un problema a nivel mundial debido a la guerra en Irak... perdón la guerra…'
    }, {
        "text":
            "@ANIABELLO_R la FED, la crisis de abatecmiento, guerra de ucrania y a duque con el aumento del deficit..etc, etc..."
    }, {
        "text":
            "RT @Mannyp24864392: @CarlosAJimnez4 Dudo que pueda haber un ataque nuclear en Kiev, le ha ido mejor a Rusia con la guerra t\u00e1ctica y desgast\u2026"
    }, {
        'text':
            'RT @MundoEConflicto: 🇺🇸 | Presidente Joe Biden: "La inflación es un problema a nivel mundial debido a la guerra en Irak... perdón la guerra…'
    }, {
        "text":
            "@Afroditaa1984 Y seguira titere todo por tu culps arrastraste s tu pais a una guerra perdida, horrible e infernal , solo por tus ambiciones de psicopata y drogadicto , demonio inmundo"
    }, {
        'text':
            'RT @EmmaRincon: 🚨 | Biden: "La inflación es un problema mundial en este momento debido a la guerra en Irak... Disculpe la guerra en Ucrania…'
    }, {
        'text':
            'RT @EmmaRincon: 🚨 | Biden: "La inflación es un problema mundial en este momento debido a la guerra en Irak... Disculpe la guerra en Ucrania…'
    }, {
        "text":
            "RT @latinus_us: \u201cLa paz no se alcanza derrotando a alguien y se debe construir con compromiso\u201d, dice el papa Francisco al pedir que cese la\u2026"
    }, {
        "text":
            "demonio pederasta. https://t.co/W8DwDP1Lq5"
    }]

    assert result == expected
