from brownie import *
from brownie import interface
from brownie import \
    PlanckCat, \
    PlanckCatMinter, \
    accounts
import os
import json

BOB = accounts.load('Bob')
ADDRESSES = ['0x8e8b3e19717A5DDCfccce9Bf3b225E61efDD7937']


def print_logs(tx):
    for i in range(len(tx.events['log'])):
        print(tx.events['log'][i]['k'] + ": " + str(tx.events['log'][i]['v']))


def deploy_PCD():
    pcd = BOB.deploy(
        PlanckCat, "ipfs://QmXiTKKMxuLwTxQQpLvQkxunwuuhXpKEwow3CuLXy7LttM/")

    return pcd


def deploy_minter(tokenAddress):
    minter = BOB.deploy(PlanckCatMinter, tokenAddress)

    return minter


def mint_batch(currentId, addresses, minter, deployer):
    mint = minter.mintBatch(currentId, addresses, {"from": deployer})


def main():
    pcd = deploy_PCD()

    minter = deploy_minter(pcd)

    print(pcd)
    print(minter)
    mint_batch(0, ADDRESSES, minter, BOB)
    # minter = deploy_minter()
