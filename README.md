# planckcats
meow ... Planck Cat DAO

## Requirements

To run the project you need:

- Python >= 3.9.2
- [Brownie >= 1.17.2](https://github.com/eth-brownie/brownie)
- Local Ganache environment installed

## Modules

### PlanckCat

ERC721 with AccessControl priveleges for the DAO to initiate mints. Additional (non-standard) methods:

```
function safeMintCustom(address to, string memory _customURI) public onlyRole(MINTER_ROLE);
```

Allows custom PFP cats to be minted by `MINTER_ROLE`.

### PlanckCatMinter

Bulk minting contract that holds the freshly minted NFTs in escrow until the receivers choose to claim. DAO determined parameters

```
uint256 public periodMint; // period over which bulk minting can occur
uint256 public capMint; // cap to number of PCD minted within periodMint
```

decide the number of cats that can be minted in a given period of time.
