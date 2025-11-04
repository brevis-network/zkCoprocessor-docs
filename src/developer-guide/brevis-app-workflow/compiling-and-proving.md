
# Compiling & Proving

{% hint style="info" %}
This section applies if your Brevis app uses the ["pure-ZK" model](../introduction/brevis-cochain.md). If you want to deploy your Brevis app under the [coChain model](cochain-mode.md), you may skip this section.
{% endhint %}

We recommend to host your circuit as a separate process as it can take up much more computing resource than typical web servers.&#x20;

## Spin Up a Prover for Your AppCircuit

The fastest way to spin up a prover is to use the prover service module in the Go SDK. `prover.NewService` automatically compiles your circuit and sets up proving/verifying keys if your circuit changes or if it's your first time compiling. Read more about [Prover Service](../../developer-resources/circuit-sdk-reference/prover-service.md).

{% code title="main.go" %}
```go
proverService, err := prover.NewService(&AppCircuit{}, config)
// listen to port 33247
proverService.Serve(33247)
```
{% endcode %}

{% hint style="info" %}
You can also opt for [manually compile & prove with Go](../../developer-resources/circuit-sdk-reference/go-workflow.md)
{% endhint %}

## Calling the Prover From Node.js

<img src="../../.gitbook/assets/image (30).png" alt="" width="563"><figcaption><p>High-level system diagram</p></figcaption>

### Sending the Proof Request to Your Prover

```typescript
const proofRes = await prover.prove(proofReq);
```

#### Error handling

```typescript
if (proofRes.has_err) {
    const err = proofRes.err;
    switch (err.code) {
    case ErrCode.ERROR_INVALID_INPUT:
        console.error('invalid receipt/storage/transaction input:', err.msg);
        // handle invalid data input...
        // this error means some of your input
        // data (receipt/storage/transaction) is not found or not supported
        // e.g. you added a transaction of type other than 0 or 2
        break;

    case ErrCode.ERROR_INVALID_CUSTOM_INPUT:
        console.error('invalid custom input:', err.msg);
        // handle invalid custom input assignment...
        break;

    case ErrCode.ERROR_FAILED_TO_PROVE:
        console.error('failed to prove:', err.msg);
        // handle failed to prove. usually marking some record as failed
        break;
    }
}
```

{% hint style="warning" %}
If you receive ERROR\_INVALID\_INPUT, check your data against [Limits and Performance](../../developer-resources/limits-and-performance.md) to see if any data exceeds the limits.
{% endhint %}

{% hint style="info" %}
#### Tip

If you want to reuse the proofs you can do serialize and deserialize `ProveResponse` by:

```typescript
import { ProveResponse } from 'brevis-sdk-typescript';
const serialized = proofRes.serialize();
const restored = ProveResponse.deserialize(serialized)
```
{% endhint %}

### Sending Your Proof to Brevis

```typescript
import { Brevis } from 'brevis-sdk-typescript';

// A client for interacting with Brevis' systems
const brevis = new Brevis('appsdkv3.brevis.network:443');
// submit() takes 
// the proof request
// proof response
// source chain ID where the data you want to use in your computation is from
// destination chain ID where your want to post the proof to
const brevisRes = await brevis.submit(proofReq, proofRes, 1, 11155111);

const id = brevisRes.id;
const fee = brevisRes.fee;
console.log(id, fee)
```

### Pay for Your Request on the Data Source Chain

Call `BrevisRequest.sendRequest()` with the id acquired from `brevisRes` and the fee (in native token). [contract addresses](../../developer-resources/contract-addresses-and-rpc-endpoints.md#contract-addresses)

_Note that this step is not needed if your application is partnered with a Brevis prover that serves off-chain requests._

### Wait for Your App Contract to be Called

Since Brevis calls your app contract's [callback function](contract-integration.md#handling-circuit-outputs-in-contract) when the final proof is submitted, you can listen to your app contract's event. Or, you could use the built-in function to wait for the final transaction submission.

```typescript
// wait() takes the request id and a destination chain id
brevis.wait(brevisRes.id, 11155111);
```
