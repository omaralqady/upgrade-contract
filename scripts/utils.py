from brownie import (
    accounts,
    network,
    config,
)
import eth_utils

FORKED_LOCAL_ENVS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account, proxy, new_impl_address, proxy_admin=None, initializer=None, *args
):
    tx = None
    if proxy_admin:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy_admin.upgradeAndCall(
                proxy.address,
                new_impl_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            tx = proxy_admin.upgrade(proxy.address, new_impl_address, {"from": account})
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy.upgradeAndCall(
                new_impl_address, encoded_function_call, {"from": account}
            )
        else:
            tx = proxy.upgrade(new_impl_address, {"from": account})

    return tx
