from Lib.Config.config import Config
from Lib.Oauth.oauth import Oauth
from Lib.Protocol.rpc_client import RpcClient
from Lib.Api.yly_print import YlyPrint
import datetime
import random



def generate_order_number():
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_digits = str(random.randint(0, 999)).zfill(3)
    order_number = f'{current_time}{random_digits}'
    return order_number

def printer():
    client_id="1074100376"
    client_secret="62088c583c3388c249d33543b126e819"
    machine_id="4004820161"

    config = Config(client_id, client_secret)
    oauth_client = Oauth(config)

    token_data = oauth_client.get_token()
    access_token = token_data['body']['access_token']

    rpc_client = RpcClient(config, access_token)

    with open('printer.txt', 'r',encoding="UTF-8") as file:
        contents = file.read()


    print_service = YlyPrint(rpc_client)
    response=print_service.index(machine_id, contents, generate_order_number())
