// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/access/IAccessControl.sol";

interface IPlanckCat is IERC721, IAccessControl {
    function safeMintCustom(address to, string memory _customURI) external;
    function tokenURI(uint256 tokenId) external view returns (string memory);
}
