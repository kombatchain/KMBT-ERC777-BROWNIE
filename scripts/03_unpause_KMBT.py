from brownie.network.contract import Contract
from scripts.helpful_scripts import get_account
from brownie import (
    KMBT,
    Contract,
)


def main():
    unpause()


def unpause():
    account = get_account(id="kc-test-account")
    print(f"account: {account}")
    proxy_kmbt = Contract.from_abi(
        "KMBT", "0xA01261685b57E80EF63eF9d86bfeFf1264447BAc", KMBT.abi
    )
    tx = proxy_kmbt.unpause({"from": account})
    tx.wait(1)
    print(f"Token paused: {proxy_kmbt.paused()}")
