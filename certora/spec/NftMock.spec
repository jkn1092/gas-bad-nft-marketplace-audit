/*
 * Verification of NftMock
 */

 using NftMock as nft;

methods {
    function mint() external; // This isn't env free because this will block ETH sent with this call. 
    function totalSupply() external returns(uint256) envfree ; // This is envfree because it's a view function, and the env doesn't matter
    function balanceOf(address) external returns(uint) envfree;
}

 invariant totalSupplyIsNotNegative()
    totalSupply() >= 0;

/*  rule sanity {
    env e;
    calldataarg arg;
    method f;
    nft.f(e, arg);
    satisfy true;
 } */

 rule minting_mints_one_nft {
    // Arrange
    env e;
    address minter;
    require e.msg.value == 0;
    require e.msg.sender == minter;
    mathint balanceBefore = nft.balanceOf(minter);

    // Act
    currentContract.mint(e);

    // Assert
    assert to_mathint(nft.balanceOf(minter)) == balanceBefore + 1, "Only 1 NFT should be minted";
 }

 rule no_change_to_total_supply(method f) {
    uint256 totalSupplyBefore = totalSupply();

    env e;
    calldataarg args;
    f(e, args);
    
    assert totalSupply() == totalSupplyBefore, "Total supply should not change";
}