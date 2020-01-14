##############################################################################
################## Algorithmic trading (Auto place order) #####################
###############################################################################

import requests
import json
import decimal
import hmac
import time
import pandas as pd
import hashlib




binance_keys = {
    'api_key': "PASTE API KEY HERE",
    'secret_key': "PASTE SECTRET KEY HERE"
}

class Binance:
