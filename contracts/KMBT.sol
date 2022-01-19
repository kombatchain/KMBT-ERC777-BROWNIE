// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/token/ERC777/ERC777Upgradeable.sol";
import "@openzeppelin/contracts/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts/utils/PausableUpgradeable.sol";

contract KMBT is
    Initializable,
    ERC777Upgradeable,
    PausableUpgradeable,
    AccessControlUpgradeable
{
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    /**
     * @dev Grants `DEFAULT_ADMIN_ROLE`, `MINTER_ROLE` and `PAUSER_ROLE` to the
     * account that deploys the contract.
     *
     */

    function initialize(
        string memory name,
        string memory symbol,
        address[] memory defaultOperators,
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData
    ) public initializer {
        __ERC777_init(name, symbol, defaultOperators);
        __AccessControl_init();
        __Pausable_init();

        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());

        _setupRole(MINTER_ROLE, _msgSender());
        _setupRole(PAUSER_ROLE, _msgSender());
        mint(to, amount, userData, operatorData);
    }

    /**
     * @dev Creates `amount` new tokens for `to`.
     *
     * Requirements:
     *
     * - the caller must have the `MINTER_ROLE`.
     */
    function mint(
        address to,
        uint256 amount,
        bytes memory userData,
        bytes memory operatorData
    ) internal {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "KMBT: must have minter role to mint"
        );
        _mint(to, amount, userData, operatorData);
    }

    /**
     * @dev Pauses all token transfers.
     *
     * Requirements:
     *
     * - the caller must have the `PAUSER_ROLE`.
     */
    function pause() public {
        require(
            hasRole(PAUSER_ROLE, _msgSender()),
            "KMBT: must have pauser role to pause"
        );
        _pause();
    }

    /**
     * @dev Unpauses all token transfers.
     *
     * Requirements:
     *
     * - the caller must have the `PAUSER_ROLE`.
     */
    function unpause() public {
        require(
            hasRole(PAUSER_ROLE, _msgSender()),
            "KMBT: must have pauser role to unpause"
        );
        _unpause();
    }

    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256 amount
    ) internal virtual override(ERC777Upgradeable) whenNotPaused {
        //require(!paused(), "KMBT: token transfer attempt whilst paused");

        super._beforeTokenTransfer(operator, from, to, amount); // Call parent hook
    }

    uint256[48] private __gap;
}
