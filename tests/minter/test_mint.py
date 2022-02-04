import pytest
from brownie import reverts


# NOTE: Have fixture so current id from PFP token creation
# starts back at 0 for each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_mint_batch(minter, cat, alice, bob, rando, gov):
    tos = [alice, bob, rando]
    current_id = 0

    expect_balance = cat.balanceOf(minter)

    # mint pcds to this contract
    tx = minter.mintBatch(current_id, tos, {"from": gov})

    # check that mint events emitted
    assert "Mint" in tx.events
    assert len(tx.events["Mint"]) == len(tos)

    # loop through each receiver to check state after mint
    for i, to in enumerate(tos):
        # check claimable bool has flipped
        assert minter.claimable(i, to) is True

        # check minter is current owner of minted planck cat (escrowed)
        assert cat.ownerOf(i) == minter

        # check escrowed for each to in tos has added associated id
        assert minter.escrowed(to, 0) == i

        # NOTE: canClaim() tests in test_views.py
        assert minter.canClaim(to) == [i]

        # check count for number available to claim increased
        assert minter.count(to) == 1

        # check mint event for the individual mint
        tx.events["Mint"][i]["to"] == to
        tx.events["Mint"][i]["id"] == i

    # check pcds escrowed in minter
    expect_balance += len(tos)
    actual_balance = cat.balanceOf(minter)
    assert actual_balance == expect_balance


def test_mint_batch_many_to_one(minter, cat, alice, bob, rando, gov):
    tos = [alice, alice, alice]
    current_id = 0

    expect_balance = cat.balanceOf(minter)

    # mint pcds to this contract
    tx = minter.mintBatch(current_id, tos, {"from": gov})

    # check that mint events emitted
    assert "Mint" in tx.events
    assert len(tx.events["Mint"]) == len(tos)

    # check canClaim has ids for all minted to alice
    expect_ids = [i for i in range(len(tos))]
    expect_count = len(expect_ids)

    # check ids added to alice's escrowed
    # NOTE: canClaim() tests in test_views.py
    assert minter.canClaim(alice) == expect_ids

    # check count increased by number minted for alice
    assert minter.count(alice) == expect_count

    # check per id based properties ..
    for i, id in enumerate(expect_ids):
        assert minter.claimable(id, alice) is True
        assert cat.ownerOf(id) == minter
        assert minter.escrowed(alice, i) == id
        assert tx.events["Mint"][i]["to"] == alice
        assert tx.events["Mint"][i]["id"] == id

    # check pcds escrowed in minter
    expect_balance += len(tos)
    actual_balance = cat.balanceOf(minter)
    assert actual_balance == expect_balance


def test_mint_batch_reverts_when_not_minter_role(minter, rando):
    current_id = 0
    with reverts("!minter"):
        _ = minter.mintBatch(current_id, [rando], {"from": rando})


def test_mint_batch_reverts_when_not_current_id(minter, gov, alice, bob,
                                                rando):
    tos = [alice, bob, rando]
    current_id = 100

    with reverts("!currentId"):
        _ = minter.mintBatch(current_id, tos, {"from": gov})


def test_mint_custom_batch(minter, cat, alice, bob, rando, gov):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    expect_balance = cat.balanceOf(minter)

    # mint pcds to this contract
    tx = minter.mintCustomBatch(current_id, tos, uris, {"from": gov})

    # check that mint events emitted
    assert "Mint" in tx.events
    assert len(tx.events["Mint"]) == len(tos)

    # loop through each receiver to check state after mint
    for i, to in enumerate(tos):
        # check claimable bool has flipped
        assert minter.claimable(i, to) is True

        # check minter is current owner of minted planck cat (escrowed)
        assert cat.ownerOf(i) == minter

        # check escrowed for each to in tos has added associated id
        assert minter.escrowed(to, 0) == i

        # NOTE: canClaim() tests in test_views.py
        assert minter.canClaim(to) == [i]

        # check count for number available to claim increased
        assert minter.count(to) == 1

        # check mint event for the individual mint
        tx.events["Mint"][i]["to"] == to
        tx.events["Mint"][i]["id"] == i

    # check pcds escrowed in minter
    expect_balance += len(tos)
    actual_balance = cat.balanceOf(minter)
    assert actual_balance == expect_balance


def test_mint_custom_batch_many_to_one(minter, cat, alice, bob, rando, gov):
    tos = [alice, alice, alice]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    expect_balance = cat.balanceOf(minter)

    # mint pcds to this contract
    tx = minter.mintCustomBatch(current_id, tos, uris, {"from": gov})

    # check that mint events emitted
    assert "Mint" in tx.events
    assert len(tx.events["Mint"]) == len(tos)

    # check canClaim has ids for all minted to alice
    expect_ids = [i for i in range(len(tos))]
    expect_count = len(expect_ids)

    # check ids added to alice's escrowed
    # NOTE: canClaim() tests in test_views.py
    assert minter.canClaim(alice) == expect_ids

    # check count increased by number minted for alice
    assert minter.count(alice) == expect_count

    # check per id based properties ..
    for i, id in enumerate(expect_ids):
        assert minter.claimable(id, alice) is True
        assert cat.ownerOf(id) == minter
        assert minter.escrowed(alice, i) == id
        assert tx.events["Mint"][i]["to"] == alice
        assert tx.events["Mint"][i]["id"] == id

    # check pcds escrowed in minter
    expect_balance += len(tos)
    actual_balance = cat.balanceOf(minter)
    assert actual_balance == expect_balance


def test_mint_custom_batch_reverts_when_not_minter_role(minter, rando):
    current_id = 0
    with reverts("!minter"):
        _ = minter.mintCustomBatch(current_id, [rando], ["https://rando.lol"],
                                   {"from": rando})


def test_mint_custom_batch_reverts_when_arrays_not_same_length(minter, gov,
                                                               alice, bob):
    tos = [alice, bob]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    with reverts("tos != uris"):
        _ = minter.mintCustomBatch(current_id, tos, uris, {"from": gov})


def test_mint_custom_batch_reverts_when_not_current_id(minter, gov, alice, bob,
                                                       rando):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 100

    with reverts("!currentId"):
        _ = minter.mintCustomBatch(current_id, tos, uris, {"from": gov})
