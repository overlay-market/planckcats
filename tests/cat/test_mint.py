def test_safe_mint(cat, gov, alice):
    expect_balance = cat.balanceOf(alice)

    # mint a cat first then check uri
    tx = cat.safeMint(alice, {"from": gov})

    # check event
    assert "Transfer" in tx.events
    assert len(tx.events["Transfer"]) == 1
    assert tx.events["Transfer"]["from"] == \
        "0x0000000000000000000000000000000000000000"
    assert tx.events["Transfer"]["to"] == alice.address

    # id was emitted thru event
    id = tx.events["Transfer"]["tokenId"]

    # check balance of alice increased
    expect_balance += 1
    actual_balance = cat.balanceOf(alice)
    assert expect_balance == actual_balance

    # check alice is owner of new token
    assert cat.ownerOf(id) == alice


def test_safe_mint_custom(cat, gov, alice):
    expect_balance = cat.balanceOf(alice)

    # mint a cat first then check uri
    tx = cat.safeMintCustom(alice, "https://planckerella.lol",
                            {"from": gov})

    # check event
    assert "Transfer" in tx.events
    assert len(tx.events["Transfer"]) == 1
    assert tx.events["Transfer"]["from"] == \
        "0x0000000000000000000000000000000000000000"
    assert tx.events["Transfer"]["to"] == alice.address

    # id was emitted thru event
    id = tx.events["Transfer"]["tokenId"]

    # check balance of alice increased
    expect_balance += 1
    actual_balance = cat.balanceOf(alice)
    assert expect_balance == actual_balance

    # check alice is owner of new token
    assert cat.ownerOf(id) == alice
