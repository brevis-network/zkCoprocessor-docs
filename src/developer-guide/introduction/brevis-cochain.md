# Brevis coChain

Brevis can operate both in the "pure-ZK" and "OP" (aka coChain) models.&#x20;

In the "pure-ZK" model, ZK proofs for data access and computation results are required to be generated upfront and submitted to the smart contract applications for ZK verification and app-specific processing. While the pure-ZK model provides simplicity and a trustless framework to work from, it is not without its own set of drawbacks:

* **High Proof Generation Costs and Limited Scalability**: While Brevis delivers world-leading performance in ZK Coprocessing and is confident in the innovations of ZK performance optimization, we must acknowledge the fundamental computational overhead introduced by ZK at this current stage. The costs of ZK proof generation and the resulting delays still present challenges. These costs ultimately contribute to a suboptimal user experience and act as barriers to the widespread adoption of data-driven dApps.
* **Inability to Generate Proofs for Some Key Use Cases:** Within the pure-ZK model, it is extremely challenging to generate proofs of non-existence. For example, proving that a user did not engage in a transaction with a specific protocol using ZK is very difficult. It would require a comprehensive ZK proof encompassing every transaction across all historical blocks—a feat that is practically infeasible. However, non-existence proofs can be utilized in important use cases such as new user acquisition, identity, account abstraction, and compliance.&#x20;

These limitations, if left unaddressed, render ZK Coprocessors impractical for numerous high-value applications, especially those involving substantially large amounts of data and users, where maintaining a minimal cost per user is crucial.

This is why we are introducing Brevis coChain (OP Model).

<figure><img src="../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

Brevis coChain is a Proof-of-Stake (PoS) blockchain featuring on-Ethereum staking and slashing functionalities. It accepts coprocessing requests from smart contracts and “**optimistically”** generates coprocessing results through PoS consensus. These PoS-generated results are submitted to blockchains as “proposals” that are subject to be “challenged” via Zero-Knowledge (ZK) proofs. Successful ZK-proof challenges will trigger the slashing of the corresponding validators’ stakes directly on Ethereum. If no challenge is initiated, the results can be used by dApps directly without incurring ZK proof generation costs. Additionally, Brevis coChain is set to integrate with EigenLayer, empowering developers to dynamically adjust the level of crypto-economics security used in the proposal stage. This fusion of crypto-economics and ZK proofs not only ensures the secure and trustless nature of Brevis but also provides developers with a versatile tradeoff space to explore so they can design according to their specific use case.

Also as an important note, developers will be able to seamlessly integrate with Brevis coChain with no extra effort required. By leveraging the Brevis SDK, you only need to write the application’s business logic once. Then, you have the flexibility to deploy your applications in either the “pure-ZK” model or the coChain model.\
