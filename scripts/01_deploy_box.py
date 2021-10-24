from scripts.utils import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def main():
    account = get_account()
    print(f"Deploying to : {network.show_active()}")
    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})

    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}. You can now upgrade to V2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(proxy_box.retrieve())
