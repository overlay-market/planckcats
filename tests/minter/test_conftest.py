def test_minter_fixture(minter, cat, gov):
    # check constructor params set
    assert minter.pcd() == cat
    assert minter.periodMint() == 604800
    assert minter.capMint() == 5
    assert minter.allowedMint() == 5

    # should have minter role
    assert cat.hasRole(cat.MINTER_ROLE(), minter) is True
