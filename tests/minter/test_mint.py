from brownie import reverts


def test_mint(minter, cat, alice, bob, rando, gov):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    minter.mint(0, tos, uris, {"from": gov})
    for i, to in enumerate(tos):
        assert minter.claimable(i, to) is True


def test_mint_reverts_when_not_minter(minter, rando):
    with reverts("!minter"):
        minter.mint(0, [rando], ["https://rando.lol"], {"from": rando})
