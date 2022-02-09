import click
import brownie.network as network
from brownie.network import max_fee, priority_fee
from brownie import PlanckCatMinter, Contract, accounts


def check_if_not_pcd(add):
    try:
        p = Contract.from_explorer(add)
    except Exception as e:
        print(e)
        return True

    if p.symbol() == 'PCD' and p.name() == 'PlanckCat':
        return False
    return True


def main():
    account = click.prompt('Enter deployer account address: ')
    pcd = click.prompt('Enter PlanckCat contract address: ')
    deployer = accounts.load(account)
    if check_if_not_pcd(pcd):
        print("PlanckCat contract address is incorrect")
        return

    if network.show_active() == "mainnet":
        priority_fee("2 gwei")
        max_fee("150 gwei")

    breakpoint()
    return PlanckCatMinter.deploy(
        pcd,
        {"from": deployer},
        publish_source=True,
    )
