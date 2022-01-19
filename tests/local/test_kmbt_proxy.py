from brownie.network.contract import Contract
from scripts.helpful_scripts import encode_function_data, get_account
from brownie import (
    KMBT,
    network,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    accounts,
    exceptions,
)
from web3 import Web3

import pytest
import brownie

initial_supply = Web3.toWei(25000000000, "ether")


def test_proxy_delegates_calls():
    account = get_account()
    print(f"account: {account}")
    print(f"Deploying to {network.show_active()}")
    kmbt = KMBT.deploy({"from": account}, publish_source=False)

    #  if you do have a proxy admin and use some type of defi protocol, proxy admin should be a type of multisig e.g. Gnosis-safe, (not done here)

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=False)

    initializer = kmbt.initialize, "KOmbat", "KMBT", [], account, initial_supply, "", ""
    kmbt_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        kmbt.address,
        proxy_admin.address,
        kmbt_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=False,
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade!")
    proxy_kmbt = Contract.from_abi("KMBT", proxy.address, KMBT.abi)
    print(f"Initialized: {kmbt._initialized}")
    tx = proxy_kmbt.initialize(
        "KOmbat", "KMBT", [], account, initial_supply, "", "", {"from": account}
    )
    tx.wait(1)
    assert proxy_kmbt.name() == "KOmbat"


def test_proxy_pause_reverts_from_non_pauser_role():
    account = get_account()
    print(f"account: {account}")
    print(f"Deploying to {network.show_active()}")
    kmbt = KMBT.deploy({"from": account}, publish_source=False)

    #  if you do have a proxy admin and use some type of defi protocol, proxy admin should be a type of multisig e.g. Gnosis-safe, (not done here)

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=False)

    initializer = kmbt.initialize, "KOmbat", "KMBT", [], account, initial_supply, "", ""
    kmbt_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        kmbt.address,
        proxy_admin.address,
        kmbt_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=False,
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade!")
    proxy_kmbt = Contract.from_abi("KMBT", proxy.address, KMBT.abi)
    print(f"Initialized: {kmbt._initialized}")
    tx = proxy_kmbt.initialize(
        "KOmbat", "KMBT", [], account, initial_supply, "", "", {"from": account}
    )
    tx.wait(1)
    with brownie.reverts("KMBT: must have pauser role to pause"):
        proxy_kmbt.pause(
            {
                "from": get_account(id="test-account"),
                "gas_limit": 1000000,
                "allow_revert": True,
            }
        )
    assert proxy_kmbt.paused() == False
