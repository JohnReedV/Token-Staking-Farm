from brownie import accounts, network, config, ChenToken, TokenFarm
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]

KEPT_TOKENS = Web3.toWei(100, "ether")


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        return accounts[0]
    if id:
        return accounts.load[0]
    return accounts.add(config["wallets"]["from_key"])


def add_allowed_tokens(farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)
        return farm


def main():
    account = get_account()
    chen = ChenToken.deploy({"from": account})
    farm = TokenFarm.deploy(chen.address, {"from": account})
    # tx = chen.transfer(farm.address, chen.totalSupply() -
    #                   KEPT_TOKENS, {"from": account})
    # tx.wait(1)
    weth_token = config["networks"]["goerli"]["weth_token"]
    fau_token = config["networks"]["goerli"]["fau_token"]
    dict_of_allowed_tokens = {
        chen: config["networks"]["goerli"]["dai_usd_price_feed"],
        fau_token: config["networks"]["goerli"]["dai_usd_price_feed"],
        weth_token: config["networks"]["goerli"]["eth_usd_price_feed"]
    }
    add_allowed_tokens(farm, dict_of_allowed_tokens, account)
    return farm, chen
