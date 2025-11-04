
# coChain Mode

A Brevis app can be deployed in the "pure-ZK" and "OP" (aka coChain) models. [This section](../introduction/brevis-cochain.md) provides a detailed introduction to the two deployment models.&#x20;

The aforementioned sections have introduced the workflow for the "pure-ZK" model. In this section, we describe how to deploy your Brevis app under the coChain model to enable use cases like "proof-of-completeness" and achieve fine-grained tradeoffs between trust assumptions and costs/latency.

To deploy in the coChain model, the developer should first follow the same steps as in the "pure-ZK" model to define [data access](data-access-module.md), write an [application circuit](application-circuit.md), and integrate with the [smart contract](contract-integration.md) (the "[Compiling & Proving](compiling-and-proving.md)" part can be skipped for the coChain Model since no actual proving is needed if no challenge occurs).

Then, the developer needs to contact the Brevis team and send their application circuit source code offline to the Brevis team. The Brevis team will wrap the circuit as a Go plugin and dynamically deploy the plugin in our coChain PoS network. Once it's done, the validators in our coChain network will be able to dry run the circuit and verify the circuit outputs are indeed calculated with the on-chain data as defined in the data access module (the coChain network will also verify the on-chain data). Then, the coChain-verified computation result can be used in the developers' app smart contract.

There are some differences when using the Brevis SDK in the coChain model as compared to the "pure-ZK" model:

1. In the coChain model, the app service is not required to actually run the circuit proving. The dry run result is enough for submission to Brevis with an option parameter set with OP-related values.
2. In the coChain model, the option parameter in `BrevisRequest.sendRequest` should be set with OP-related values.
3. In the coChain model, the `handelOpProofResult` interface should be implemented by the developer's custom app smart contract instead of the `handelProofResult` interface as in the "pure-ZK" model.
4. In the coChain model, `challengeWindow` should be set in the developer's custom app smart contract. Note that each request won't be fulfilled on-chain until the corresponding challenge window has passed.

## Contract Integration in the coChain Model

As described above, a few additional things should be implemented in the contract to develop a contract that integrates with the coChain mode.

Below is an example that extends the MyAppContract in the [previous section](contract-integration.md) to make it usable for the coChain mode.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract MyCoChainAppContract is MyAppContract {
    
    // Handle optimistic proof result. 
    // This example handles optimistic results in the same way as handling zk results,
    // your app can choose to do differently.
    function handleOpProofResult(
        bytes32 _vkHash,
        bytes calldata _circuitOutput
    ) internal override {
        handleProofResult(_vkHash, _circuitOutput);
    }

   /**
     * @notice config params to handle the optimistic proof result
     * @param _challengeWindow The challenge window to accept optimistic results. 
     *                         0: POS, maxInt: disable optimistic result
     * @param _sigOption bitmap to express expected sigs. bit 0 is bvn, bit 1 is avs
     */
    function setBrevisOpConfig(
        uint64 _challengeWindow, 
        uint8 _sigOption
    ) external onlyOwner {
        brevisOpConfig = BrevisOpConfig(_challengeWindow, _sigOption);
    }
}
```
