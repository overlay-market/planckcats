import pytest
from brownie import reverts


# NOTE: Have fixture so current id from PFP token creation
# starts back at 0 for each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_claim(minter, cat, gov, alice, bob, rando):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    # Mint the planck cats first
    # NOTE: mint() tests in test_mint.py
    minter.mint(current_id, tos, uris, {"from": gov})

    # prior balances to check against
    expect_balance_alice = cat.balanceOf(alice)
    expect_balance_bob = cat.balanceOf(bob)
    expect_balance_rando = cat.balanceOf(rando)
    expect_balance_minter = cat.balanceOf(minter)

    # claim the NFTs
    for id, to in enumerate(tos):
        tx = minter.claim([id], {"from": to})

        # check event of planck cat transfer
        assert "Transfer" in tx.events
        assert len(tx.events["Transfer"]) == 1
        assert tx.events["Transfer"]["from"] == minter
        assert tx.events["Transfer"]["to"] == to
        assert tx.events["Transfer"]["tokenId"] == id

        # check no longer claimable
        assert minter.claimable(id, to) is False

        # check to now owns the nft
        assert cat.ownerOf(id) == to

    # check balances after claim
    expect_balance_alice += 1
    expect_balance_bob += 1
    expect_balance_rando += 1
    expect_balance_minter -= 3

    actual_balance_alice = cat.balanceOf(alice)
    actual_balance_bob = cat.balanceOf(bob)
    actual_balance_rando = cat.balanceOf(rando)
    actual_balance_minter = cat.balanceOf(minter)

    assert expect_balance_alice == actual_balance_alice
    assert expect_balance_bob == actual_balance_bob
    assert expect_balance_rando == actual_balance_rando
    assert expect_balance_minter == actual_balance_minter


def test_claim_many(minter, cat, gov, alice, bob, rando):
    tos = [alice, alice, alice]
    uris = ["https://one.alice.lol/", "https://two.alice.lol/",
            "https://three.alice.lol/"]
    current_id = 0

    # Mint the planck cats first
    # NOTE: mint() tests in test_mint.py
    minter.mint(current_id, tos, uris, {"from": gov})
    ids = [0, 1, 2]

    # prior balances to check against
    expect_balance_alice = cat.balanceOf(alice)
    expect_balance_minter = cat.balanceOf(minter)

    # claim the NFTs
    tx = minter.claim(ids, {"from": alice})

    # check events of planck cat transfer
    assert "Transfer" in tx.events
    assert len(tx.events["Transfer"]) == 3
    for id, event in enumerate(tx.events["Transfer"]):
        assert event["from"] == minter
        assert event["to"] == alice
        assert event["tokenId"] == id

    # check balances of NFT have changed for minter and alice
    expect_balance_alice += 3
    expect_balance_minter -= 3
    actual_balance_alice = cat.balanceOf(alice)
    actual_balance_minter = cat.balanceOf(minter)
    assert actual_balance_alice == expect_balance_alice
    assert actual_balance_minter == expect_balance_minter

    # check alice now owns all NFTs and minter does not
    for id in ids:
        assert cat.ownerOf(id) == alice


def test_claim_reverts_when_no_token_minted(minter, cat, gov, alice, bob,
                                            rando):
    with reverts("!claimable"):
        _ = minter.claim([100], {"from": alice})


def test_claim_reverts_when_not_user(minter, cat, gov, alice, bob,
                                     rando):
    tos = [alice]
    uris = ["https://alice.lol/"]
    current_id = 0

    # Mint the planck cats first
    # NOTE: mint() tests in test_mint.py
    minter.mint(current_id, tos, uris, {"from": gov})

    with reverts("!claimable"):
        _ = minter.claim([current_id], {"from": rando})


def test_claim_reverts_when_already_claimed(minter, cat, gov, alice, bob,
                                            rando):
    tos = [alice]
    uris = ["https://alice.lol/"]
    current_id = 0

    # Mint the planck cats first
    # NOTE: mint() tests in test_mint.py
    minter.mint(current_id, tos, uris, {"from": gov})

    # claim the token then try to claim again
    _ = minter.claim([current_id], {"from": alice})

    # try to claim again
    with reverts("!claimable"):
        _ = minter.claim([current_id], {"from": alice})
