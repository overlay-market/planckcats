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


def test_can_claim(minter, gov, alice, bob):
    current_id = 2  # 2 given prior test
    tos = [alice, alice, bob]

    # mint the batch
    minter.mintBatch(current_id, tos, {"from": gov})

    # check available to claim
    expect_ids_alice = [2, 3]
    expect_ids_bob = [4]

    actual_ids_alice = minter.canClaim(alice)
    actual_ids_bob = minter.canClaim(bob)

    assert expect_ids_alice == actual_ids_alice
    assert expect_ids_bob == actual_ids_bob

    # alice claims 3
    minter.claim(3, {"from": alice})

    # check available to claim again
    expect_ids_alice = [2]
    expect_ids_bob = [4]

    actual_ids_alice = minter.canClaim(alice)
    actual_ids_bob = minter.canClaim(bob)

    assert expect_ids_alice == actual_ids_alice
    assert expect_ids_bob == actual_ids_bob

    # bob claims 4
    minter.claim(4, {"from": bob})

    # check available to claim again
    expect_ids_alice = [2]
    expect_ids_bob = []

    actual_ids_alice = minter.canClaim(alice)
    actual_ids_bob = minter.canClaim(bob)

    assert expect_ids_alice == actual_ids_alice
    assert expect_ids_bob == actual_ids_bob

    # alice claims 2
    minter.claim(2, {"from": alice})

    # check available to claim again
    expect_ids_alice = []
    expect_ids_bob = []

    actual_ids_alice = minter.canClaim(alice)
    actual_ids_bob = minter.canClaim(bob)

    assert expect_ids_alice == actual_ids_alice
    assert expect_ids_bob == actual_ids_bob
