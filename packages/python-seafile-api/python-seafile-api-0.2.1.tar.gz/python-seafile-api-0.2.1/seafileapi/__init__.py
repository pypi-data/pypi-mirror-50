from seafileapi.client import SeafileApiClient

def connect(server, username, password, token=None):
    client = SeafileApiClient(server, username, password, token)
    return client
