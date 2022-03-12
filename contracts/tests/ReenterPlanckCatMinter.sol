// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "../PlanckCatMinter.sol";

contract ReenterPlanckCatMinter is ERC721Holder {
    using Counters for Counters.Counter;
    address minter;
    address deployer;
    Counters.Counter private _tokenIdCounter;
    address[] public arr = [msg.sender, msg.sender];

    constructor(address _minter) {
        deployer = msg.sender;
        minter = _minter;
    }

    function reenter() public {
        require(msg.sender == deployer, "!deployer");
        /// attacker mints 2 NFTs with the following call
        PlanckCatMinter(minter).mintBatch(0, arr);
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes memory
    ) public virtual override returns (bytes4) {
        _tokenIdCounter.increment();

        if (_tokenIdCounter.current() == 2) {
            return this.onERC721Received.selector;
        }
        /// attacker hopes to mint 2 more NFTs by re-entering here
        PlanckCatMinter(minter).mintBatch(2, arr);

        return this.onERC721Received.selector;
    }
}
