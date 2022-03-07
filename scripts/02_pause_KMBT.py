from brownie.network.contract import Contract
from scripts.helpful_scripts import get_account
from brownie import (
    KMBT,
    Contract,
)


def main():
    pause()


def pause():
    account = get_account(id="kc-test-account")
    print(f"account: {account}")
    proxy_kmbt = Contract.from_abi(
        "KMBT", "0xA01261685b57E80EF63eF9d86bfeFf1264447BAc", KMBT.abi
    )
    tx = proxy_kmbt.pause({"from": account, "priority_fee": 210640000000})
    tx.wait(1)
    print(f"Token paused: {proxy_kmbt.paused()}")
