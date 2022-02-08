import os
import brownie.network as network, max_fee, priority_fee
from brownie import PlanckCat, PlanckCatMinter, Contract, accounts


def get_args():
    return {
        "account": os.getenv('BROWNIE_ACCOUNT'),
        "pcd": os.getenv('PCD')
    }


def check_if_not_pcd(add):
    p = Contract.from_explorer(add)
    if p.symbol() == 'PCD' and p.name() == 'PlanckCat':
        return False
    return True


def main():
    args = get_args()
    deployer = accounts.load(args['account'])
    pcd = args['pcd']
    breakpoint()

    if check_if_not_pcd(pcd):
        return "Environment variable PCD does not point to PlanckCatDao NFT"

    if network.show_active() == "mainnet":
        priority_fee("2 gwei")
        max_fee("150 gwei")

    return PlanckCatMinter.deploy(
        pcd,
        {"from": deployer},
        publish_source=True,
    )
