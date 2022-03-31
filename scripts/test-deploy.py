from brownie import *
from brownie import interface
from brownie import \
    PlanckCat, \
    PlanckCatMinter, \
    accounts, \
    Contract
import os
import json

DEPLOYER = accounts.load('Bob')
ADDRESSES = ['0x8e8b3e19717A5DDCfccce9Bf3b225E61efDD7937']
PCD = "0xe356FBD8a927Eb1725116Ef56B6BB9c58392B75E"
MINTER = "0x9ba2D3D2ED1a70ab7826978329DC04C6B1fbc888"


def print_logs(tx):
    for i in range(len(tx.events['log'])):
        print(tx.events['log'][i]['k'] + ": " + str(tx.events['log'][i]['v']))


def get_pcd_abi():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, 'constants/PlanckCatABI.json')
    abi_file = open(path)
    return json.load(abi_file)


def get_pcd_minter_abi():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, 'constants/PlanckCatMinterABI.json')
    abi_file = open(path)
    return json.load(abi_file)


def deploy_PCD(deployer):
    return PlanckCat.deploy(
        "ipfs://QmXiTKKMxuLwTxQQpLvQkxunwuuhXpKEwow3CuLXy7LttM/",
        {"from": deployer},
    )


def deploy_minter(pcd, deployer):
    return PlanckCatMinter.deploy(
        pcd,
        {"from": deployer},
    )


def mint_batch(currentId, addresses, minter, pcd):
    mint = minter.mintBatch(currentId, addresses, {"from": pcd})


def main():
    # pcd = deploy_PCD(DEPLOYER)

    # minter = deploy_minter(pcd, DEPLOYER)
    pcd_abi = get_pcd_abi()
    pcd_minter_abi = get_pcd_minter_abi()

    pcd = Contract.from_abi("PCD", PCD, pcd_abi)
    pcd_minter = Contract.from_abi("Minter", MINTER, pcd_minter_abi)

    # pcd.safeMint(DEPLOYER, {"from": DEPLOYER})
    pcd_minter.mintBatch(2, ADDRESSES, {"from": DEPLOYER})
