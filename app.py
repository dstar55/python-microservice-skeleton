from connexion.resolver import RestyResolver

import connexion
import os

import config

app = config.connexion_app
app.add_api('items.yaml', resolver = RestyResolver('api'))

if __name__ == '__main__':

    app.run(port = 9090)
