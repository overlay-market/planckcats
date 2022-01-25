from brownie import chain


def test_minter_fixture(minter, cat, gov):
    # check constructor params set
    assert minter.pcd() == cat
    assert minter.periodMint() == 86400
    assert minter.capMint() == 3
    assert minter.allowedMint() == 3
    assert minter.timestampPeriodLast() == chain[-1]["timestamp"]

    # should have minter role
    assert cat.hasRole(cat.MINTER_ROLE(), minter) is True
