from web3 import Web3
from utils.Blockchain import BlockChainSettings
from utils.Blockchain.ContractHandler import get_contract_abi_DOGE_chain


class BlockChainConnect:
    def __init__(self, chainName, webSocketStatus=False):
        self.chainName = chainName
        self.webSocketSwitch = webSocketStatus
        self.ChainID = BlockChainSettings.get_setting(chainName).ChainID
        self.RPC = BlockChainSettings.get_setting(chainName).RPC_2
        self.Symbol = BlockChainSettings.get_setting(chainName).Symbol
        self.web3 = self.connect()

    def connect(self):
        if not self.webSocketSwitch:
            web3 = Web3(Web3.HTTPProvider(self.RPC))
            return web3

    def contract_settings(self, contractAddress):
        return self.web3.eth.contract(address=Web3.toChecksumAddress(contractAddress), abi=get_contract_abi_DOGE_chain(contractAddress))

    def get_coin_balance(self, contractAddress: str, userAddress: str):
        return self.from_wei(
            self.contract_settings(Web3.toChecksumAddress(contractAddress)).functions.balanceOf(Web3.toChecksumAddress(userAddress)).call())

    def get_native_coin_balance(self, walletAddress: str):
        return self.from_wei(self.web3.eth.getBalance(Web3.toChecksumAddress(walletAddress)))

    def from_wei(self, balance):
        return self.web3.fromWei(balance, "ether")

    def get_transaction(self, transaction: str) :
        return self.web3.eth.get_transaction(transaction)


Chain = BlockChainConnect(chainName="DOGE")
print(Chain.web3.isConnected())
tx = Chain.get_coin_balance(contractAddress="0x7fc009adc0b7a5e9c81f2e0e7a14c6c281abb99c", userAddress="0x2A5bac6615C1516C89e3b657a19C8620D815674a")
print(tx)
