def test_is_current_id_when_zero_minted(minter):
    # check 0 is current id
    assert minter.isCurrentId(0) is True
    assert minter.isCurrentId(1) is False


def test_is_current_id_when_some_minted(minter, cat, gov, alice, bob):
    # mint two so currentId = 2
    cat.safeMint(alice, {"from": gov})
    cat.safeMint(bob, {"from": gov})

    # check 2 is current id
    assert minter.isCurrentId(2) is True
    assert minter.isCurrentId(1) is False
    assert minter.isCurrentId(3) is False
