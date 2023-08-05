routes = {
    r'^\/admin\/assinantes$': {
        'POST': lambda handler: create_assinante(handler),
        'media_type': 'application/json'
    },
    r'^\/admin\/assinantes/.+$': {
        'GET': lambda handler: get_assinante(handler),
        'media_type': 'application/json'
    },
    r'^\/stream\/auth$':  {
        'POST': lambda handler: do_auth(handler),
        'media_type': 'application/json'
    },
    r'^\/stream\/data$':  {
        'POST': lambda handler: receive_data(handler),
        'media_type': 'application/json'
    }
}


def get_assinante(handler):
    return {}


def do_auth(handler):
    return {"accessToken": "123", "refreshToken": "321"}


def receive_data(handler):
    return {"sucessos": 0, "items": []}


def create_assinante(hander):
    return {}
