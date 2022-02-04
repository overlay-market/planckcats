def test_minter_fixture(minter, cat, gov):
    # check constructor params set
    assert minter.pcd() == cat

    # should have minter role
    assert cat.hasRole(cat.MINTER_ROLE(), minter) is True
