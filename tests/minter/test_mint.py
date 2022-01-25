from brownie import reverts


def test_mint(minter, cat, alice, bob, rando, gov):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0

    minter.mint(current_id, tos, uris, {"from": gov})
    for i, to in enumerate(tos):
        assert minter.claimable(i, to) is True


def test_mint_reverts_when_not_minter(minter, rando):
    with reverts("!minter"):
        _ = minter.mint(0, [rando], ["https://rando.lol"], {"from": rando})


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
