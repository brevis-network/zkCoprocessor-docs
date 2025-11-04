# Introduction

Brevis is a highly efficient ZK coprocessor that empowers smart contracts to read from the full historical on-chain data from all supported blockchains and run customizable computations in a completely trust-free way. With the power of trust-free historical data, Brevis enables exciting new use cases like data-driven DeFi, user retention and engagement features, trust-free active liquidity management, omnichain activity-based identity, and many more. Read [this blog for examples. ](https://blog.brevis.network/2023/11/01/uniswap-v4-hook-brevis-zk-coprocessor-data-driven-dex-experiences/)

Integrating your dApp with Brevis only takes three simple steps:

1. **Data Access**: Smart contracts, through Brevis's APIs, can trustlessly access the full historical on-chain data, such as states, transactions, and events, from Ethereum and other chains.
2. **Computation**: Developers then can build and deploy their customized business logic as application circuits without any prior knowledge of ZK using Brevis's SDK. Brevis runs the computation and generates a ZK proof off-chain for the results.&#x20;
3. **Using the Results:** The computation results, along with the ZK proof, are submitted back on-chain for application smart contracts to seamlessly verify and consume.

Check out this short intro video to get an idea of what Brevis does:

{% embed url="https://www.youtube.com/embed/TMwaMF1JziE?si=ZVeBvCAZwRiBFJ3a" %}

You can also check out a concrete example of Uniswap v4 trading fee discount hook built with Brevis SDK.&#x20;

{% embed url="https://www.youtube.com/watch?v=1cjC8D_-jso" %}

In the following sections, we break down these steps with an end-to-end workflow.
