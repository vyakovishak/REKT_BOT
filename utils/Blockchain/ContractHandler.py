import json

import requests


def open_settings_file():
    # try:
    #     with open('./utils/Blockchain/ContractsABI.json', 'r') as openfile:
    #         return json.load(openfile)
    # except:
    with open('./utils/Blockchain/ContractsABI.json', 'r') as openfile:
        return json.load(openfile)


def write_to_settings_file(oldABIs, newABIs, contractAddress):
    oldABIs[contractAddress] = newABIs
    # try:
    #     with open('./utils/Blockchain/ContractsABI.json', 'w') as openfile:
    #         json.dump(oldABIs, openfile, indent=4, sort_keys=True)
    # except:
    with open('./utils/Blockchain/ContractsABI.json', 'w') as openfile:
        json.dump(oldABIs, openfile, indent=4, sort_keys=True)


def get_contract_abi_DOGE_chain(contractAddress):
    contract = open_settings_file()
    if contractAddress in contract:
        return contract[contractAddress]
    else:
        newABI = requests.get(
            f"https://explorer.dogechain.dog/api?module=contract&action=getabi&address={contractAddress}").json().get(
            'result')
        write_to_settings_file(contract, newABI, contractAddress)
        return newABI
