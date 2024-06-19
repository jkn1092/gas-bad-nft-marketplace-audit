/*
 * Certora Formal Verification Spec for GasBadNftMarketplace
 */ 

using GasBadNftMarketplace as gasBadMarketplace; 
using NftMock as nft;
using NftMarketplace as marketplace;

// The methods that we acknowledge in CVL 
methods {
    function buyItem(address,uint256) external;
    function cancelListing(address,uint256) external;
    function listItem(address,uint256,uint256) external;
    function withdrawProceeds() external;
    function updateListing(address,uint256,uint256) external;

    // View Functions
    function getListing(address,uint256) external returns (INftMarketplace.Listing) envfree;
    function getProceeds(address) external returns (uint256) envfree;

    // Dispatcher means the safeTransferFrom function will only be called by an NftMock
    function _.safeTransferFrom(address,address,uint256) external => DISPATCHER(true);
    function _.onERC721Received(address, address, uint256, bytes) external => DISPATCHER(true); 
}

ghost mathint listingUpdatesCount {
    init_state axiom listingUpdatesCount == 0;
}

ghost mathint log4Count {
    init_state axiom log4Count == 0;
}

hook Sstore s_listings[KEY address nftAddress][KEY uint256 tokenId].price uint256 price STORAGE {
    listingUpdatesCount = listingUpdatesCount + 1;
}

hook LOG4(uint offset, uint length, bytes32 t1, bytes32 t2, bytes32 t3, bytes32 t4) uint v {
    log4Count = log4Count + 1;
}

/*//////////////////////////////////////////////////////////////
                                RULES
//////////////////////////////////////////////////////////////*/

invariant anytime_mapping_updated_emit_event() 
    listingUpdatesCount <= log4Count;



rule calling_any_function_should_result_in_each_contract_having_the_same_state(method f, method f2, address listingAddr, uint256 tokenId, address seller){
    env e;
    calldataarg args;

    require(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    require(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);

    require(f.selector == f2.selector);
    gasBadMarketplace.f(e, args);
    marketplace.f2(e, args);

    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).price == marketplace.getListing(e, listingAddr, tokenId).price);
    assert(gasBadMarketplace.getListing(e, listingAddr, tokenId).seller == marketplace.getListing(e, listingAddr, tokenId).seller);
    assert(gasBadMarketplace.getProceeds(e, seller) == marketplace.getProceeds(e, seller));
}

