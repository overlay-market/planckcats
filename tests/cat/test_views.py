def test_token_uri_when_regular_mint(cat, gov, alice):
    base_uri = cat.defaultBaseURI()

    # mint a cat first then check uri
    tx = cat.safeMint(alice, {"from": gov})
    id = tx.events["Transfer"]["tokenId"]

    # uri should be default base + tokenId + .json
    expect = f"{base_uri}{id}.json"
    actual = cat.tokenURI(id)
    assert actual == expect


def test_token_uri_when_custom_mint(cat, gov, alice):
    custom_uri = "https://planckerella.lol/"

    # mint a cat first then check uri
    tx = cat.safeMintCustom(alice, custom_uri, {"from": gov})
    id = tx.events["Transfer"]["tokenId"]

    # uri should be default custom + tokenId + .json
    expect = f"{custom_uri}{id}.json"
    actual = cat.tokenURI(id)
    assert actual == expect
