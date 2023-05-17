import json


class FTM:
    RPC = "https://rpc.ankr.com/fantom/"
    RPC_2 = "https://rpcapi.fantom.network/"
    RPC_3 = "https://fantom-mainnet.public.blastapi.io/"
    RPC_4 = "https://rpc.ftm.tools/"
    ChainID = 250
    Symbol = "FTM"
    BrowserURL = "https://ftmscan.com"
    GraphQL = "https://xapi.fantom.network/"
    TransactionTracing = "https://rpcapi-tracing.fantom.network/"
    TestRPC = "https://rpc.ankr.com/fantom_testnet/"
    TestRPC_2 = "https://xapi.testnet.fantom.network/lachesis/"
    TestRPC_3 = "https://rpc.testnet.fantom.network/"
    TestRPC_4 = "https://fantom-testnet.public.blastapi.io/"
    TestChainID = 4002
    BrowserTestURL = "https://testnet.ftmscan.com/"
    WS_URL = "wss://wsapi.fantom.network/"
    WS_URL_2 = "wss://fantom-mainnet.public.blastapi.io/"


class ETH:
    API_Key = "8FK6T2QUG749GRRDADM1NCST1VJR1DQZQS"
    RPC = "https://api.etherscan.io/"
    ChainID = 1
    RPC_2 = "https://eth-mainnet-public.unifra.io"
    RPC_3 = "https://eth-mainnet.nodereal.io/v1/1659dfb40aa24bbb8153a677b98064d7"
    RPC_4 = "https://rpc.ankr.com/eth"
    Symbol = "ETH"


class Test_ETH:
    RPC = "https://api-goerli.etherscan.io/"
    ChainID = 5
    Symbol = "GoerliETH"


class BSC:
    RPC = "https://rpc-bsc.bnb48.club"
    RPC_2 = "https://rpc.ankr.com/bsc"
    RPC_3 = "https://bsc-dataseed2.ninicoin.io"
    RPC_4 = "https://bsc-dataseed3.ninicoin.io"
    ChainID = 56
    Symbol = "BNB"


class DOGE:
    RPC = "https://rpc-us.dogechain.dog"
    RPC_2 = "https://dogechain.ankr.com"
    RPC_3 = "https://rpc01-sg.dogechain.dog"
    RPC_4 = "https://rpc02-sg.dogechain.dog"
    ChainID = 2000
    Symbol = "DOGE"


def open_settings_file():
    with open('BlockChainSettings.json', 'r') as openfile:
        return json.load(openfile)


def write_to_settings_file(settings):
    with open('BlockChainSettings.json', 'w') as openfile:
        json.dump(settings, openfile, indent=4, sort_keys=True)


def get_setting(userNetwork):
    settings = dict(DOGE=DOGE, BSC=BSC, ETH=ETH, FTM=FTM, Test_ETH=Test_ETH)

    return settings.get(userNetwork)

