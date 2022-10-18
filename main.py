import flask
import typing
import pandas as pd
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import json
from numpy import int64

from conf import *

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", help="File with bank data", required=True)
args = vars(parser.parse_args())
filename = args['file']

app = flask.Flask("Sber Test Server")

class BanksInfo:
    def __init__(self, filename: str):
        self.table = pd.read_csv(filename)

    def get_info_json_by_bin(self, number: int64):
        return self.table[self.table['bin'] == number].reset_index().to_json(orient='records')


def ensure_and_get_bin(number: str) -> typing.Optional[int64]:
    if not 16 <= len(number) <= 20 or not number.isdigit():
        return None
    return int64(number[:6])


def make_json_response(json_str: str, status: int):
    return flask.Response(json.dumps(json_str), status=status, mimetype='application/json')


@app.route('/cards/<number>', methods=['GET'])
def process_cards_request(number: str):
    bin = ensure_and_get_bin(number)
    if bin is None:
        return make_json_response({"data": "Wrong number format"}, 500)

    info = cards_info.get_info_json_by_bin(bin)
    info_json = json.loads(info)
    if len(info_json) == 0:
        return flask.Response(json.dumps({}), status=200, mimetype='application/json')
    result = info_json[0]
    del result['index']
    del result['bin']
    return flask.Response(json.dumps(result), status=200, mimetype='application/json')


if __name__ == '__main__':
    cards_info = BanksInfo(filename)
    app.run(HOST, PORT)
