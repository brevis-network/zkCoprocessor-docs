
# Brevis Client

## Submit

By calling the `submit` function, Brevis client will wrap circuit inputs and send them to Brevis Gateway to finish the rest of the proving process.&#x20;

The _<mark style="color:blue;">**submit**</mark>_ is a wrapper of two fundamental calls to the Brevis gateway. The[ first one ](brevis-client.md#preparequery)is used to initialize the proving process on the Brevis gateway. The [second one](brevis-client.md#submitproof) will upload application circuit proof to the Brevis gateway for future proof aggregation.&#x20;

We highly recommend developers use this to kick off Brevis SDK integration for simple testing. _<mark style="color:orange;">**For best practice, we recommend using subsequent APIs to reduce proving latency.**</mark>_ Generally, it takes some time to prove the application circuit, from seconds to minutes. At the same time, Brevis Gateway can operate the parallel proving. It will save lots of time&#x20;

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/brevis-client.ts#L51-L74" %}

| Name            | Type                                                                                                                                       | Description                                                                                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| proveRequest    | [ProveRequest](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L32-L37)      | Brevis prover service will use it to prove circuit computation validity. It contains receipts, list of storage information and transactions used in application circuit |
| proof           | [ProveResponse](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L39C1-L43C2) | Proving response given by Brevis prover service                                                                                                                         |
| srcChainId      | number                                                                                                                                     | Circuit input data original chain                                                                                                                                       |
| dstChainId      | number                                                                                                                                     | Which chain the final proof will be posted on                                                                                                                           |
| option          | [QueryOption](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/brevis/gateway.proto#L64-L67)   |                                                                                                                                                                         |
| apiKey          | string                                                                                                                                     | Identification which is used for Brevis partner flow                                                                                                                    |
| callbackAddress | string                                                                                                                                     | Developer's application contract address. Used for Brevis partner flow only                                                                                             |

## PrepareQuery

PrepareQuery will trigger Brevis gateway proving initialization. After that, Brevis gateway will return [QueryKey](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/brevis/gateway.proto#L182-L185) and fee for this proving. Then developers can guide users to submit on-transaction <mark style="color:purple;">SendRequest</mark> tx. Please note that it is _**not required**_ for application circuit proof. In this way, parallel proving can be achieved.&#x20;

{% hint style="info" %}
On-chain tx is not required if there is a partnership between the developer's project and Brevis.&#x20;
{% endhint %}

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/brevis-client.ts#L76-L86" %}

| Name            | Type                                                                                                                                            | Description                                           |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| proveRequest    | [ProveRequest](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L32-L37)           | see above                                             |
| appCircuitInfo  | [AppCircuitInfo](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/common/circuit_data.proto#L4-L13) | Brevis prover service will generate it automatically  |
| srcChainId      | number                                                                                                                                          | see above                                             |
| dstChainId      | number                                                                                                                                          | see above                                             |
| option          | [QueryOption](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/brevis/gateway.proto#L64-L67)        |                                                       |
| apiKey          | string                                                                                                                                          | see above                                             |
| callbackAddress | string                                                                                                                                          | see above                                             |

## SubmitProof

After proof is generated by the Brevis Prover Service,  it should be uploaded to the Brevis gateway for proof aggregation.

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/brevis-client.ts#L88-L90" %}

| Name       | Type                                                                                                                                    | Description                                      |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| queryKey   | [QueryKey](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/brevis/gateway.proto#L182-L185) | Query identification  returned by Brevis gateway |
| dstChainId | number                                                                                                                                  | see above                                        |
| proof      | String                                                                                                                                  | Provided by Brevis Prover Service                |

## Wait

Developers can use wait() to check query status. It will get query status from the Brevis gateway periodically. You can find all possible query status [here](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/brevis/gateway.proto#L101-L120).

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/brevis-client.ts#L93-L118" %}
