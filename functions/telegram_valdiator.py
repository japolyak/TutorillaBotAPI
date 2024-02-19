import os
import hmac
import hashlib
from urllib.parse import parse_qs


def init_data_is_valid(init_data: str) -> bool:
    parsed_query = parse_qs(init_data)
    bot_token = os.getenv("BOT_TOKEN")

    parsed_auth_date = parsed_query.get('auth_date', [''])[0]
    parsed_query_id = parsed_query.get('query_id', [''])[0]
    parsed_user = parsed_query.get('user', [''])[0]
    parsed_hash = parsed_query.get('hash', [''])[0]

    data_check_string = f"auth_date={parsed_auth_date}\nquery_id={parsed_query_id}\nuser={parsed_user}"

    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).digest()
    hex_signature = ''.join(format(b, '02x') for b in computed_hash)

    return hex_signature == parsed_hash
