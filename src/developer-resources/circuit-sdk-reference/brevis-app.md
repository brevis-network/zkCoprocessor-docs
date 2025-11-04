# Brevis App

`sdk.BrevisApp` is the framework around your custom circuit. It handles the conversion of your data to circuit inputs and interacting with Brevis's system. To create a `BrevisApp`, use:

```go
import "github.com/brevis-network/brevis-sdk/sdk"
```

```go
app := sdk.NewBrevisApp(
    1, // data source chain id
    "RPC_URL", // corresponding chain RPC URL, you can find many here: https://chainlist.org/chain/1
    "OUTPUT_DIR", // brevis sdk will save source data into OUTPUT_DIR/input/data.json for future reference
)
```

## Adding Source Data

### Source Data Types

The Brevis application circuit supports proving receipt,  storage value, and transaction by adding TransactionData, ReceiptData, and StorageData. Developers only need to set up the <mark style="color:red;">\*required</mark> values and the Brevis app will prepare the rest automatically.

#### ReceiptData

<table><thead><tr><th width="163">Name</th><th width="152">Type</th><th>Description</th></tr></thead><tbody><tr><td>TxHash</td><td><a href="https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56">common.Hash</a></td><td>Receipt's transaction hash (<mark style="color:red;"><strong>*required</strong></mark>)</td></tr><tr><td>BlockNum</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td>Receipt's block number</td></tr><tr><td>BlockBaseFee</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td><a href="https://ethereum.org/en/developers/docs/gas/#base-fee">Block base fee</a></td></tr><tr><td>MptKeyPath</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td>Rlp encoded receipt index using <a href="https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/rlp/raw.go#L228">this</a></td></tr><tr><td>Fields</td><td>[<a href="brevis-app.md#logfielddata">LogFieldData</a>]</td><td>Array of field information will be used in receipt (Usp to 4 fields in each receipt)</td></tr></tbody></table>

#### LogFieldData

| Name       | Type                                                                                                                         | Description                                                                                                          |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| LogPos     | uint                                                                                                                         |  the log's position in the receipt (<mark style="color:red;">**\*required**</mark>)                                  |
| IsTopic    | bool                                                                                                                         | Whether the field is a topic  (<mark style="color:red;">**\*required**</mark>)                                       |
| FieldIndex | uint                                                                                                                         | The index of the field in either a log's topics or data. (<mark style="color:red;">**\*required**</mark>)            |
| Contract   | [common.Address](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L213) | The contract from which the event is emitted                                                                         |
| EventID    | [common.Hash](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56)     | The event ID of the event to which the field belong (aka topics\[0])                                                 |
| Value      | [common.Hash](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56)     | The value of the field in event, aka the actual thing we care about, only 32-byte fixed length values are supported. |

#### StorageData

| Name         | Type                                                                                                                         | Description                                                                          |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| BlockNum     | [big.Int](https://pkg.go.dev/math/big)                                                                                       | Block number used for storage value (<mark style="color:red;">**\*required**</mark>) |
| BlockBaseFee | [big.Int](https://pkg.go.dev/math/big)                                                                                       | [Block base fee](https://ethereum.org/en/developers/docs/gas/#base-fee)              |
| Address      | [common.Address](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L213) | Address used for storage value (<mark style="color:red;">**\*required**</mark>)      |
| Slot         | [common.Hash](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56)     | Storage slot (<mark style="color:red;">**\*required**</mark>)                        |
| Value        | [common.Hash](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56)     | Storage value                                                                        |

#### TransactionData

<table><thead><tr><th width="163">Name</th><th width="152">Type</th><th>Description</th></tr></thead><tbody><tr><td>Hash</td><td><a href="https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56">common.Hash</a></td><td>Transaction hash (<mark style="color:red;"><strong>*required</strong></mark>)</td></tr><tr><td>BlockNum</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td>Receipt's block number</td></tr><tr><td>BlockBaseFee</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td><a href="https://ethereum.org/en/developers/docs/gas/#base-fee">Block base fee</a></td></tr><tr><td>MptKeyPath</td><td><a href="https://pkg.go.dev/math/big">big.Int</a></td><td>Rlp encoded receipt index using <a href="https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/rlp/raw.go#L228">this</a></td></tr><tr><td>LeafHash</td><td><a href="https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56">common.Hash</a></td><td><p>Hash of transaction raw data </p><p>with rlp prefix. </p></td></tr></tbody></table>

{% hint style="warning" %}
As of now, brevis will only prove the _**existence of a transaction**_, stay tuned for more tx information is usable
{% endhint %}

### Adding Source Data

The data you add here will be available to process in your app circuit.

```go
app.AddReceipt(sdk.ReceiptData{...})
app.AddStorage(sdk.StorageData{...})
app.AddTransaction(sdk.TransactionData{...})
```

The maximum amount of Receipt/Storage/Transaction data you can add to each type is restricted by the maximum amount you define in your circuit's `Allocate` function. [read more](app-circuit-interface.md#allocate)

Each of the three types of data has an index within its type. For example, if you call AddStorage twice:

```go
app.AddStorage(sdk.StorageData{/* StorageA */})
app.AddStorage(sdk.StorageData{/* StorageB */})
```

Then StorageA will be at index 0, and StorageB will be at index 1.

#### Pin an Index

You can also pin a piece of data to a specific index. For example, this will pin TransactionA at index 2.

```go
app.AddTransaction(sdk.TransactionData{/* TransactionA */}, 2)
```

Let's see pinning in a more complete example. Let's say  you defined your `Allocate` function to allocate 32 data for Receipt, 32 for Storage, and 64 for Transaction.&#x20;

```go
func (c *AppCircuit) Allocate() (maxReceipts, maxStorage, maxTransaction) {
    return 32, 32, 32
}
```

Then, you added data queries to your `BrevisApp` instance:

```go
app.AddReceipt(sdk.ReceiptData{/* ReceiptA */})

app.AddStorage(sdk.StorageData{/* StorageA */})
app.AddStorage(sdk.StorageData{/* StorageB */})

app.AddTransaction(sdk.TransactionData{/* TransactionA */})
// this one is fixed at index 2
const MyFixedSpot = 2
app.AddTransaction(sdk.TransactionData{/* TransactionB */}, MyFixedSpot)
```

The mental model of this would be:

<img src="../../.gitbook/assets/img1 (1).png" alt=""><figcaption></figcaption>

Notice how there is an empty slot in transactions because we allocated 64 slots for transactions, but only added two. We also fixated TransactionB at index 2, so the slot index 1 remains empty. TransactionB will always be at index 2.&#x20;

#### Accessing Data by Index in Circuit

Accessing data by index is closely related to how you allocate data slots. [read more about Allocate](app-circuit-interface.md#allocate)

```go
func (c *AppCircuit) Define(api *sdk.CircuitAPI, input sdk.CircuitInput) {
    transactions := sdk.NewDataStream(input.Transaction)
    // access transactionB directly
    transactionB := transactions.Get(MyFixedSpot)
}
```

## Building the `CircuitInput`

`sdk.CircutiInput` is the packaged data obtained from executing your data queries and converting them into circuit types. This is used in testing, compiling, and proving.

After you have added queries to your `BrevisApp`, call `app.BuildCircuitInput` with your circuit definition to build.

```go
// if your circuit has custom inputs, you'll need to supply a correct assignment 
// of those custom inputs
appCircuit := &AppCircuit{MyCustomInput: someCorrectValue}
circuitInput, err := app.BuildCircuitInput(appCircuit)
```

## Submitting the Proof to Brevis

{% hint style="info" %}
[Proof generation](peripheral-apis.md#proving-and-verifying) relies on a separate set of functions, but once you have a proof, your `BrevisApp` instance can handle submitting it to Brevis.
{% endhint %}

To submit your proof to Brevis, you need to first query Brevis RPC for the fee amount and acquire a `requestId`.&#x20;

#### PrepareRequest Input

| Name             | Type                                                                                                                                     | Description                                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| vk               | VerifyingKey                                                                                                                             | application circuit verifying key                                                                                   |
| witness          | witness.Witness                                                                                                                          | application circuit witness                                                                                         |
| srcChainId       | uint64                                                                                                                                   | the id of data source chain                                                                                         |
| dstChainId       | uint64                                                                                                                                   | the chain where the proven data is used                                                                             |
| appContract      | common.Address                                                                                                                           | developer's contract callback address                                                                               |
| callbackGasLimit | uint64                                                                                                                                   | Gas limit for contract callback                                                                                     |
| queryOption      | [queryOption](https://github.com/brevis-network/brevis-proto/blob/83520cce5a55c8a29057db2854dffed63b168b2b/brevis/gateway.proto#L64-L67) | ZK\_MODE: pure zk flow. <mark style="color:red;">recommended</mark> for developers. OP\_MODE: supported by BVN. wip |
| brevisPartnerKey | string                                                                                                                                   | <mark style="color:red;">not required</mark>. Developer can use empty string to skip this flow.                     |

```go
calldata, requestId, nonce, feeValue, err := app.PrepareRequest(
    vk, 
    witness,
    srcChainId, 
    dstChainId, 
    refundee, 
    appContract,
    callbackGasLimit,
    gwproto.QueryOption_ZK_MODE.Enum(),
    "")
```

#### PrepareRequest Output

| Name      | Type                                                                                                                     | Description                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| calldata  | \[]byte                                                                                                                  |  transaction calldata          |
| requestId | [common.Hash](https://github.com/ethereum/go-ethereum/blob/25bc07749ce21376e1023a6e16ec173fa3fc4e43/common/types.go#L56) | query key for future reference |
| nonce     | uint64                                                                                                                   | transaction parameter          |
| feeValue  | big.int                                                                                                                  | proving fee                    |

#### Submitting the Proof

```go
err := app.SubmitProof(proof)
```

You can optionally supply success and error callbacks. Note that the option `sdk.WithFinalProofSubmittedCallback` makes SubmitProof non-blocking. If you want a blocking way to wait for final proof submission, use `app.WaitFinalProofSubmitted`.

```go
// Choose one:

err := app.SubmitProof(proof, sdk.WithFinalProofSubmittedCallback(...)) // async
// Or
err := app.SubmitProof(proof)
tx, err := app.WaitFinalProofSubmitted(context.Background()) // blocks the routine
```

#### Paying the Fee

The provers in the Brevis network only start working after you pay the fee. To pay, call the `sendRequest` function on the `BrevisRequest` contract ([address](../contract-addresses-and-rpc-endpoints.md#contract-addresses)) with the `feeValue` you got from `PrepareRequest`.

{% hint style="info" %}
You can pay the fee any time after you acquire the `requestId` and `feeValue` from `PrepareRequest`. This process done in parallel with `SubmitProof` and `WaitFinalProofSubmitted`.
{% endhint %}

{% hint style="info" %}
#### Tip: Reducing End-to-end Proof Generation Time

Once PrepareRequest is called **AND** Brevis receives the fee, Brevis starts proving the proofs that are independent from your proof. If your circuit is big and wants to minimize the proof generation time, you can call PrepareRequest first, then pay the fee. This allows your proof and Brevis's proofs to be generated in parallel.
{% endhint %}
