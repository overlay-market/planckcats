import pytest
from brownie import reverts


# NOTE: Have fixture so current id from PFP token creation
# starts back at 0 for each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_mint(minter, cat, alice, bob, rando, gov):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    expect_balance = cat.balanceOf(minter)
    expect_allowed_mint = minter.allowedMint()

    # mint pcds to this contract
    minter.mint(current_id, tos, uris, {"from": gov})

    # check claimable bool has flipped and minter is current owner
    # of each minted planck cat (escrowed in minter)
    for i, to in enumerate(tos):
        assert minter.claimable(i, to) is True
        assert cat.ownerOf(i) == minter

    # check pcds escrowed in minter
    expect_balance += len(tos)
    actual_balance = cat.balanceOf(minter)
    assert actual_balance == expect_balance

    # check allowed mint decremented
    expect_allowed_mint -= len(tos)
    actual_allowed_mint = minter.allowedMint()
    assert expect_allowed_mint == actual_allowed_mint


def test_mint_reverts_when_not_minter_role(minter, rando):
    current_id = 0
    with reverts("!minter"):
        _ = minter.mint(current_id, [rando], ["https://rando.lol"],
                        {"from": rando})


def test_mint_reverts_when_arrays_not_same_length(minter, gov, alice, bob):
    tos = [alice, bob]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    with reverts("tos != uris"):
        _ = minter.mint(current_id, tos, uris, {"from": gov})


def test_mint_reverts_when_not_current_id(minter, gov, alice, bob, rando):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 100

    with reverts("!currentId"):
        _ = minter.mint(current_id, tos, uris, {"from": gov})


def test_mint_reverts_when_greater_than_allowed(minter, gov, alice, bob,
                                                rando):
    current_id = 0

    # minting one more than allowed should revert
    num_mint = minter.allowedMint() + 1
    tos = [alice for i in range(num_mint)]
    uris = ["https://alice.lol/" for i in range(num_mint)]
    with reverts("mint > max"):
        _ = minter.mint(current_id, tos, uris, {"from": gov})

    # minting exact amount allowed should not revert
    num_mint = minter.allowedMint()
    tos = [alice for i in range(num_mint)]
    uris = ["https://alice.lol/" for i in range(num_mint)]
    minter.mint(current_id, tos, uris, {"from": gov})
