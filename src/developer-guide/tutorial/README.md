
# Tutorial

This tutorial will walk you through a minimal example of the aforementioned workflow for developing a Brevis app. Check out [this repo](https://github.com/brevis-network/brevis-sdk/tree/main/examples) for some more advanced examples, such as trading volume proof on Uniswap, TWAP, etc. You can also check out [this helpful video tutorial](https://x.com/brevis_zk/status/1789868342544834823) on building a trading volume-based fee discount feature in Uniswap v4.&#x20;

The example in this tutorial only supports pure ZK mode. Please follow [this previous section](../brevis-app-workflow/cochain-mode.md) to support coChain mode

## The App: Proving Token Transfer

Our app's goal is to allow anyone to prove to our on-chain contract that an Ethereum address has made a USDC token transfer whose amount is more than 500 USDC.&#x20;

We will implement this app step by step. The finished version is also available in this [repo](https://github.com/brevis-network/brevis-quickstart-ts).

### How can an ERC-20 Transfer be proven?

When an ERC-20 token transfer is made, a [_**Transfer**_**&#x20;event**](https://etherscan.io/tx/0x9ae76abb67f76f1a896e4655ba33cbcefdb4e5b587de028bd9c3cd1ee29df9b5#eventlog) will be emitted in the transaction receipt. By reading this log, we can find _From_ in topics and _Value_ in data.&#x20;

In the tutorial application, we are going to write an Brevis app checking that the value more than is 500000000 (500 with decimal 6) for a transaction receipt.&#x20;

## Contents

{% content-ref url="building-the-app-circuit.md" %}
[building-the-app-circuit.md](building-the-app-circuit.md)
{% endcontent-ref %}

{% content-ref url="writing-the-app-contract.md" %}
[writing-the-app-contract.md](writing-the-app-contract.md)
{% endcontent-ref %}

{% content-ref url="putting-everything-together.md" %}
[putting-everything-together.md](putting-everything-together.md)
{% endcontent-ref %}
