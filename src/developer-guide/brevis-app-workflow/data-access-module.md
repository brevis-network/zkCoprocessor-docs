
# Data Access Module

First, let's walk through the workflow for adding historical receipt/tx/storage data to your app via the [Brevis TypeScript SDK](https://github.com/brevis-network/brevis-sdk-typescript) which offers a convenient way for NodeJS to interact with the [prover service](../../developer-resources/circuit-sdk-reference/prover-service.md) and Brevis' system.

<img src="../../.gitbook/assets/image (30).png" alt="" width="563"><figcaption><p>High-level system diagram</p></figcaption>

### Install the Dependency

```bash
npm install brevis-sdk-typescript
```

### Adding Source Data

#### Initialize a Proof Request to Your Prover Service

```typescript
import { ProofRequest, Prover } from 'brevis-sdk-typescript';
// Assuming you started your prover service on port 33247, this is how you 
// initialize a client in your NodeJS program to interact with it.
const prover = new Prover('localhost:33247');

const proofReq = new ProofRequest();
```

#### Add the Data to the Proof Request

Depending on your project, you may want to first query an indexer, such as Dune, an Ethereum node, or your own service, to acquire the raw data (such as transactions) according to your business logic. This part is **not** handled by the Brevis SDK.

> **Note:** 
**So why can't we just use the indexer data directly on chain?**

If you directly post the data from an indexer to your contract without any validity proofs, your users would be trusting the entity who posted this data to behave correctly. Brevis's core role is to replace this trust of data validity on one party with a ZK proof so no one can fabricate data and computation results.&#x20;


After you acquire the raw data, you add the data to the `proofReq`. The data you add here is closely tied to how you [allocate](../../developer-resources/circuit-sdk-reference/app-circuit-interface.md#allocate) data slots for your circuit and is available in `CircuitInput` passed in to your `Define` function. [how to write an application circuit](application-circuit.md)

```typescript
proofReq.addReceipt(
    new ReceiptData({
        tx_hash: '0x53b37ec7975d217295f4bdadf8043b261fc49dccc16da9b9fc8b9530845a5794',
        fields: [
            new Field({
                log_index: 3,
                is_topic: false,
                field_index: 0,
            }),
            new Field({
                log_index: 3,
                is_topic: true,
                field_index: 2,    
            }),
            new Field({
                log_index: 2,
                is_topic: true,
                field_index: 1
            }),
        ],
    }),
);
proofReq.addStorage(
    new StorageData({
        block_num: 18233760,
        address: '0x5427FEFA711Eff984124bFBB1AB6fbf5E3DA1820',
        slot: '0x0000000000000000000000000000000000000000000000000000000000000000',
    }),
);
proofReq.addTransaction(
    new TransactionData({
        hash: '0x6dc75e61220cc775aafa17796c20e49ac08030020fce710e3e546aa4e003454c',
    }),
);
```

#### Add Custom Inputs

If you define [custom inputs](../../developer-resources/circuit-sdk-reference/custom-inputs.md) for your circuit, you need to fully assign them here in `ProofRequest`.

```go
// circuit custom input definition
type AppCircuit struct{
    // example custom field `MerkleProof`
    MerkleProof [8]sdk.Bytes32
}
```

```typescript
// assigning custom input in typescript
proofReq.setCustomInput({
    // key names match what we defined in AppCircuit
    MerkleProof: [
        // type of the field should also match what we define in AppCircuit
        asBytes32('0x1111111111111111111111111111111111111111111111111111111111111111'),
        asBytes32('0x2222222222222222222222222222222222222222222222222222222222222222'),
        // ...
    ],
});
```

> **Note:** 
The keys of the custom input object you add in typescript matches what you define in your app circuit. The first letter can also be lower cased, e.g. `merkleProof` in the above example


#### Custom Input Types

The types of the custom input you assign in `ProofRequest` must match what you define in your app circuit. All [primitive circuit data types](../../developer-resources/circuit-sdk-reference/circuit-data-types.md#primitive-types) are allowed here through the following functions.

For example, if your AppCircuit is defined as&#x20;

```go
type AppCircuit struct {
    MyUint32Input sdk.Uint32
    MyUint248Input1 sdk.Uint248
    MyUint248Input2 sdk.Uint248
    MyUint521Input1 sdk.Uint521
    MyUint521Input2 sdk.Uint521
    MyInt248Input sdk.Int248
    MyBytes32Input sdk.bytes32
}
```

In your Typescript program you would need to assign the custom input as

```typescript
proofReq.setCustomInput({
    MyUint32Input1: asUint32('1'),
    MyUint248Input1: asUint248('123'),
    // 0x prefixed hex input is also allowed
    MyUint248Input2: asUint248('0xabcdef'),
    MyUint521Input1: asUint521('123'),
    // 0x prefixed hex input is also allowed
    MyUint521Input2: asUint521('0xabcdef'),
    MyInt248Input: asInt248('-123'),
    MyBytes32Input: asBytes32('0x3333333333333333333333333333333333333333333333333333333333333333'),
});
```

The data you add here will be available for use in your[ Application Circuit.](application-circuit.md)

Read more about [Source Data Types](../../developer-resources/circuit-sdk-reference/brevis-app.md#source-data-types).

> **Note:** 
For advanced developers, there is also a way to access the receipt/tx/storage data via the [Go SDK](https://github.com/brevis-network/brevis-sdk). See [Go Workflow](../../developer-resources/circuit-sdk-reference/go-workflow.md) for details.

