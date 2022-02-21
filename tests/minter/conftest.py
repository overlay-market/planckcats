import pytest
from brownie import PlanckCat, PlanckCatMinter, ReenterPlanckCatMinter


@pytest.fixture(scope="module")
def gov(accounts):
    yield accounts[0]


@pytest.fixture(scope="module")
def alice(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def bob(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def rando(accounts):
    yield accounts[3]


@pytest.fixture(scope="module", params=["https://planckcat.lol/planckerella/"])
def cat(gov, request):
    uri = request.param
    cat_contract = gov.deploy(PlanckCat, uri)
    yield cat_contract


@pytest.fixture(scope="module")
def create_minter(gov, alice, cat):
    def create_minter(pcd=cat):
        minter = gov.deploy(PlanckCatMinter, pcd)
        pcd.grantRole(pcd.MINTER_ROLE(), minter, {"from": gov})
        return minter

    yield create_minter


@pytest.fixture(scope="module")
def minter(create_minter):
    yield create_minter()


@pytest.fixture(scope="module")
def attacc_minter(minter, alice):
    # alice is the attacker that deploys a malicious contract
    yield alice.deploy(ReenterPlanckCatMinter, minter)
