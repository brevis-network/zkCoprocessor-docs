
# Prover Client

## Prove

The developer can use prove() to notify the Brevis Prover Service proving application circuit with inputs. The response will return AppCircuitInfo and Proof. Because of time consumption in proving, we recommend it be used for <mark style="color:red;">circuits with small amount of constraints only</mark>. Otherwise, proving parallelism will be broken.

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/prover-client.ts#L19-L22" %}

| Name          | Type                                                                                                                                   | Description                                                                                                                                                             |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| proveRequest  | [ProveRequest](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L32-L37)  | Brevis prover service will use it to prove circuit computation validity. It contains receipts, list of storage information and transactions used in application circuit |
| proveResponse | [ProveResponse](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L39-L43) | It contains application circuit info and circuit proof                                                                                                                  |

## ProveAsync

Unlike prove(), proveAysnc will not wait for application circuit proof. It returns a _<mark style="color:orange;">proof\_id</mark>_ instead. Developers can retrieve proof from Brevis Prover Service later with this proof\_id.

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/prover-client.ts#L24-L27" %}

| Name               | Type                                                                                                                                        | Description                                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| proveRequest       | [ProveRequest](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L32-L37)       | Brevis prover service will use it to prove circuit computation validity. It contains receipts, list of storage information and transactions used in application circuit |
| proveAsyncResponse | [ProveAsyncResponse](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L45-L49) | It contains application circuit info and proof\_id                                                                                                                      |

## GetProof

GetProof is used to retrieve proof from the Brevis Prover Service. Brevis Prover Service uses memory to persist the application circuit proof. When receiving a GetProof request, Brevis Prover Service will check whether the proof is ready. If it is ready, Brevis Prover Service will return proof and <mark style="color:purple;">release it from memory</mark>. Hence, _<mark style="color:red;">**developers have to store the proof somewhere**</mark>_ if there is an intention of proof data persistence.

{% embed url="https://github.com/brevis-network/brevis-sdk-typescript/blob/9071f89277b5c0a95e69066037eacf19cd763add/src/prover-client.ts#L29-L32" %}

| Name               | Type                                                                                                                                      | Description               |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| proveRequest       | [GetProofRequest](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L51-L53)  |                           |
| proveAsyncResponse | [GetProofResponse](https://github.com/brevis-network/brevis-proto/blob/b7d1e8abff8c3ce29d0fa2106b991d259875c78f/sdk/prover.proto#L55-L60) | application circuit proof |
