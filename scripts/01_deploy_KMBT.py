from brownie.network.contract import Contract
from scripts.helpful_scripts import encode_function_data, get_account
from brownie import (
    KMBT,
    network,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    accounts,
    config,
)
from web3 import Web3

initial_supply = Web3.toWei(20000000000, "ether")


def main():
    deploy()


def deploy():
    account = get_account(id="kc-test-account")
    print(f"account: {account}")
    print(f"Deploying to {network.show_active()}")
    kmbt = KMBT.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    #  if you do have a proxy admin and use some type of defi protocol, proxy admin should be a type of multisig e.g. Gnosis-safe, (not done here)

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=False)

    initializer = kmbt.initialize, "KOmbat", "KMBT", [], account, initial_supply, "", ""
    kmbt_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        kmbt.address,
        proxy_admin.address,
        kmbt_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade!")
    proxy_kmbt = Contract.from_abi("KMBT", proxy.address, KMBT.abi)
    print(f"Initialized: {kmbt._initialized}")
    tx = proxy_kmbt.initialize(
        "KOmbat", "KMBT", [], account, initial_supply, "", "", {"from": account}
    )
    tx.wait(1)
    print(f"account: {account}")
    print(f"Token name: {proxy_kmbt.name()}")
    print(f"Token symbol: {proxy_kmbt.symbol()}")
    print(f"Total Supply: {proxy_kmbt.totalSupply()}")
