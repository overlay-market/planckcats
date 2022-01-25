from brownie import reverts


def test_set_period_mint(minter, gov):
    period_mint = 1209600  # 14 days

    # change the mint period
    tx = minter.setPeriodMint(period_mint, {"from": gov})

    # check mint period changed
    expect = period_mint
    actual = minter.periodMint()
    assert expect == actual

    # check events emitted
    assert "PeriodMintUpdated" in tx.events
    assert tx.events["PeriodMintUpdated"]["user"] == gov
    assert tx.events["PeriodMintUpdated"]["_periodMint"] == expect


def test_set_cap_mint(minter, gov):
    cap_mint = 10  # 10 cats

    # change the mint cap
    tx = minter.setCapMint(cap_mint, {"from": gov})

    # check mint cap changed
    expect = cap_mint
    actual = minter.capMint()
    assert expect == actual

    # check events emitted
    assert "CapMintUpdated" in tx.events
    assert tx.events["CapMintUpdated"]["user"] == gov
    assert tx.events["CapMintUpdated"]["_capMint"] == expect


def test_set_period_mint_reverts_when_not_minter_role(minter, alice):
    period_mint = 1209600  # 14 days
    with reverts("!minter"):
        _ = minter.setPeriodMint(period_mint, {"from": alice})


def test_set_period_mint_reverts_when_less_than_min(minter, gov):
    period_mint = minter.MIN_PERIOD_MINT() - 1

    # check reverts when 1 less than min
    with reverts("periodMint < min"):
        _ = minter.setPeriodMint(period_mint, {"from": gov})

    # check does not revert when equal to min
    period_mint = minter.MIN_PERIOD_MINT()
    minter.setPeriodMint(period_mint, {"from": gov})


def test_set_period_mint_reverts_when_greater_than_max(minter, gov):
    period_mint = minter.MAX_PERIOD_MINT() + 1

    # check reverts when 1 greater than max
    with reverts("periodMint > max"):
        _ = minter.setPeriodMint(period_mint, {"from": gov})

    # check does not revert when equal to max
    period_mint = minter.MAX_PERIOD_MINT()
    minter.setPeriodMint(period_mint, {"from": gov})


def test_set_cap_mint_reverts_when_not_minter_role(minter, alice):
    cap_mint = 10
    with reverts("!minter"):
        _ = minter.setCapMint(cap_mint, {"from": alice})


def test_set_cap_mint_reverts_when_greater_than_max(minter, gov):
    cap_mint = minter.MAX_CAP_MINT() + 1

    # check reverts when 1 greater than max
    with reverts("capMint > max"):
        _ = minter.setCapMint(cap_mint, {"from": gov})

    # check does not revert when equal to max
    cap_mint = minter.MAX_CAP_MINT()
    minter.setCapMint(cap_mint, {"from": gov})
