def test_minter_fixture(minter, cat, gov):
    assert minter.pcd() == cat

    # should have minter role
    assert cat.hasRole(cat.MINTER_ROLE(), minter) is True
