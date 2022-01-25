def test_cat_fixture(cat, gov):
    assert cat.defaultBaseURI() == "https://planckcat.lol/planckerella/"
    assert cat.hasRole(cat.DEFAULT_ADMIN_ROLE(), gov) is True
    assert cat.hasRole(cat.MINTER_ROLE(), gov) is True
