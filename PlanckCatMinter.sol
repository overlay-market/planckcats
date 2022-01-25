// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "./interfaces/IPlanckCat.sol";

contract PlanckCatMinter is ERC721Holder {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    address public immutable pcd;

    mapping(uint256 => mapping(address => bool)) public claimable;

    constructor(address _pcd) {
        pcd = _pcd;
    }

    modifier onlyMinter {
        require(IPlanckCat(pcd).hasRole(MINTER_ROLE, msg.sender), "!minter");
        _;
    }

    /// @dev mints to this planck cat minter contract first to avoid security
    /// @dev issues with ERC721 call back. After all are minted,
    /// @dev users can call claim() function. Technically the callback
    /// @dev shouldn't affect us given the onlyMinter modifier
    function mint(uint256 currentId, address[] memory tos, string[] memory uris) external onlyMinter {
        require(tos.length == uris.length, "tos != uris");
        require(isCurrentId(currentId), "!currentId");

        address _pcd = pcd;
        for (uint256 i=0; i < tos.length; i++) {
            address to = tos[i];
            string memory uri = uris[i];

            IPlanckCat(_pcd).safeMintCustom(address(this), uri);
            claimable[currentId][to] = true;
            currentId++;
        }
    }

    function claim(uint256[] memory ids) external {
        address _pcd = pcd;
        for (uint256 i=0; i < ids.length; i++) {
            uint256 id = ids[i];
            if (claimable[id][msg.sender]) {
                claimable[id][msg.sender] = false;
                IPlanckCat(_pcd).safeTransferFrom(address(this), msg.sender, id, "");
            }
        }
    }

    /// @dev checks whether currentId is the ID of the next cat to be minted
    /// @dev IPlanckCat(_pcd)_tokenIdCounter.current() == currentId
    function isCurrentId(uint256 currentId) public returns (bool) {
        string memory nonexistentReason = "ERC721Metadata: URI query for nonexistent token";
        address _pcd = pcd;

        try IPlanckCat(_pcd).tokenURI(currentId) returns (string memory) {
            // if URI already exists, then not the current id
            return false;
        } catch Error(string memory reason) {
            if (currentId == 0) {
                return true;
            } else if (keccak256(bytes(reason)) == keccak256(bytes(nonexistentReason))) {
                // currentId hasn't been minted yet. Now check that
                // currentId - 1 has been minted, so we know currentId is the
                // next ID
                try IPlanckCat(_pcd).tokenURI(currentId-1) returns (string memory) {
                    // last minted ID was currentId-1, so currentId is actually the current id
                    return true;
                } catch {}
            }
        }
        return false;
    }
}
