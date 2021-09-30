// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract ChenToken {
    string public name = "Chen Token";
    string public symbol = "CHEN";
    uint256 public decimals = 18;
    uint256 public totalSupply = 100000000000000000000000000;

    mapping(address => mapping(address => uint256)) public allowance;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );

    constructor() {
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _value)
        external
        returns (bool success)
    {
        require(
            balanceOf[msg.sender] >= _value,
            "Cannot send more than you have"
        );
        balanceOf[msg.sender] = balanceOf[msg.sender] - (_value);
        balanceOf[_to] = balanceOf[_to] + (_value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(
        address _from,
        address _to,
        uint256 _value
    ) external returns (bool) {
        require(_value <= balanceOf[_from], "Cannot send more than you have");
        require(
            _value <= allowance[_from][msg.sender],
            "Cannot send more than you have"
        );
        allowance[_from][msg.sender] = allowance[_from][msg.sender] - (_value);
        emit Transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) external returns (bool) {
        require(_spender != address(0));
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
}
