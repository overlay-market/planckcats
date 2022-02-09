import click
import os
import json
import brownie.network as network
from brownie.network import max_fee, priority_fee
from brownie import PlanckCatMinter, Contract, accounts


def get_pcd_abi():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, 'constants/PlanckCatABI.json')
    abi_file = open(path)
    return json.load(abi_file)


def check_if_not_pcd(add):
    try:
        p = Contract.from_explorer(add)
    except Exception as e:
        print(e)
        return True

    abi_json = get_pcd_abi()
    if p.abi == abi_json:
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

    click.echo(f'Contract is ready to be deployed on {network.show_active()}.')
    click.echo('Continue? [y/n]', nl=False)
    c = (click.getchar()).lower()
    if c == 'n':
        click.echo('Deployment aborted')
        return
    elif c == 'y':
        click.echo('Deploying contract!')
    else:
        click.echo('Invalid input')
        return

    return PlanckCatMinter.deploy(
        pcd,
        {"from": deployer},
        publish_source=True,
    )
