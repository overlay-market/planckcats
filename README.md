# planckcats
meow ... Planck Cat DAO

## Requirements

To run the project you need:

- Python >= 3.9.2
- [Brownie >= 1.17.2](https://github.com/eth-brownie/brownie)
- Local Ganache environment installed

## Modules

### PlanckCat

ERC721 with AccessControl privileges for the DAO to initiate mints. Additional (non-standard) methods:

```
function safeMintCustom(address to, string memory _customURI) public onlyRole(MINTER_ROLE);
```

Allows custom PFP cats to be minted by `MINTER_ROLE`.

### PlanckCatMinter

Bulk minting contract that holds the freshly minted NFTs in escrow until the receivers choose to claim. DAO calls either of two batch minting methods:

```
function mintBatch(uint256 currentId, address[] memory tos) external onlyMinter;
function mintCustomBatch(uint256 currentId, address[] memory tos, string[] memory uris) external onlyMinter;
```

which mints the cats to the `PlanckCatMinter` contract. Newly minted cats are then held in escrow in the `PlanckCatMinter` contract until the receiver decides to claim their cat by calling

```
function claim(uint256 id) external;
```
