// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "./interfaces/IPlanckCat.sol";

contract PlanckCatMinter is ERC721Holder {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    address public immutable pcd;

    mapping(uint256 => mapping(address => bool)) public claimable;

    // onlyMinter params to limit PCDs that can be bulk minted within a period
    uint256 public periodMint; // period over which bulk minting can occur
    uint256 public capMint; // cap to number of PCD minted within periodMint

    // dynamic quantities that change within the given mint period
    uint256 public allowedMint; // remaining PCD available to mint in periodMint
    uint256 public timestampPeriodLast; // start timestamp of current periodMint

    constructor(address _pcd, uint256 _periodMint, uint256 _capMint) {
        pcd = _pcd;
        periodMint = _periodMint;
        capMint = _capMint;
        allowedMint = _capMint;
        timestampPeriodLast = block.timestamp;
    }

    modifier onlyMinter() {
        require(IPlanckCat(pcd).hasRole(MINTER_ROLE, msg.sender), "!minter");
        _;
    }

    /// @notice refreshes allowed PCD to be bulk minted if one periodMint has passed
    function refresh() public {
        uint256 dt = block.timestamp - timestampPeriodLast;
        if (dt >= periodMint) {
            allowedMint = capMint;
            timestampPeriodLast = block.timestamp;
        }
    }

    /// @notice mint new planck cats for claiming
    /// @dev mints to this planck cat minter contract first to avoid security
    /// @dev issues with ERC721 call back. After all are minted,
    /// @dev users can call claim() function. Technically the callback
    /// @dev shouldn't affect us given the onlyMinter modifier, but still.
    function mint(
        uint256 currentId,
        address[] memory tos,
        string[] memory uris
    ) external onlyMinter {
        require(tos.length == uris.length, "tos != uris");
        require(isCurrentId(currentId), "!currentId");

        // refresh allowed mint amount if enough time has passed
        refresh();

        // check allowed to mint number of PCD specified
        require(tos.length <= allowedMint, "mint > max");
        allowedMint -= tos.length;

        // loop through and safe mint to this address. track who
        // can claim which minted NFT thru claimable
        address _pcd = pcd;
        for (uint256 i = 0; i < tos.length; i++) {
            address to = tos[i];
            string memory uri = uris[i];

            IPlanckCat(_pcd).safeMintCustom(address(this), uri);
            claimable[currentId][to] = true;
            currentId++;
        }
    }

    /// @notice claim planck cats by ID
    function claim(uint256[] memory ids) external {
        address _pcd = pcd;

        // Loop thru and transfer all escrowed IDs user can claim
        for (uint256 i = 0; i < ids.length; i++) {
            uint256 id = ids[i];
            // check can actually claim id
            require(claimable[id][msg.sender], "!claimable");

            // transfer escrowed to msg.sender
            claimable[id][msg.sender] = false;
            IPlanckCat(_pcd).safeTransferFrom(address(this), msg.sender, id, "");
        }
    }

    /// @notice check whether currentId is the ID of the next cat to be minted
    /// @dev IPlanckCat(_pcd)_tokenIdCounter.current() == currentId
    function isCurrentId(uint256 currentId) public view returns (bool) {
        address _pcd = pcd;

        // Gameplan: tokenURI(currentId) should revert on call to PCD BUT
        // tokenURI(currentId-1) should not IF isCurrentId(currentId) == true
        string memory nonexistentReason = "ERC721Metadata: URI query for nonexistent token";
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
                try IPlanckCat(_pcd).tokenURI(currentId - 1) returns (string memory) {
                    // last minted ID was currentId-1, so currentId is actually the current id
                    return true;
                } catch {}
            }
        }
        return false;
    }

    /// @notice sets the mint period over which can bulk mint PCD
    function setPeriodMint(uint256 _periodMint) external onlyMinter {
        periodMint = _periodMint;
    }

    /// @notice sets the cap on number of PCD that can be bulk minted every periodMint
    function setCapMint(uint256 _capMint) external onlyMinter {
        capMint = _capMint;
    }
}
