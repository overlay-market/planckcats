import pytest
from brownie import PlanckCat, ReenterPlanckCat


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
def attacc(cat, alice):
    # alice is the attacker that deploys a malicious contract
    yield alice.deploy(ReenterPlanckCat, cat)
