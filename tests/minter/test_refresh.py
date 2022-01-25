import pytest
from brownie import chain


# NOTE: Have fixture so current id from PFP token creation
# starts back at 0 for each test
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


def test_refresh(minter, gov, alice, bob, rando):
    tos = [alice, bob, rando]
    uris = ["https://alice.lol/", "https://bob.lol/", "https://rando.lol/"]
    current_id = 0
    period_mint = minter.periodMint()

    # Mint the planck cats first
    # NOTE: mint() tests in test_mint.py
    minter.mint(current_id, tos, uris, {"from": gov})

    # get prior values
    expect_allowed_mint = minter.allowedMint()
    expect_timestamp_period_last = minter.timestampPeriodLast()

    # Check no refresh happens when dt < periodMint
    # mine the chain to 1 second before refresh
    mine_time = minter.timestampPeriodLast() + period_mint - 1
    chain.mine(timestamp=mine_time)

    # refresh tx
    _ = minter.refresh()

    # gather expect vs actual values
    actual_allowed_mint = minter.allowedMint()
    actual_timestamp_period_last = minter.timestampPeriodLast()

    # check allowed and timestamp haven't changed when no refresh
    assert expect_allowed_mint == actual_allowed_mint
    assert expect_timestamp_period_last == actual_timestamp_period_last

    # Check refresh happens when dt >= periodMint
    # mine the chain to exact time refresh can happen
    mine_time = minter.timestampPeriodLast() + period_mint
    chain.mine(timestamp=mine_time)

    # refresh tx
    tx = minter.refresh()

    # gather expect vs actual values
    expect_allowed_mint = minter.capMint()
    expect_timestamp_period_last = chain[tx.block_number]['timestamp']
    actual_allowed_mint = minter.allowedMint()
    actual_timestamp_period_last = minter.timestampPeriodLast()

    # check allowed and timestamp have changed when refresh
    assert expect_allowed_mint == actual_allowed_mint
    assert expect_timestamp_period_last == actual_timestamp_period_last
