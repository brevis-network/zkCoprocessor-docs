# App Circuit Interface

Your circuit needs to implement the `AppCircuit` interface to be used with the Brevis SDK.

```go
type AppCircuit interface {
	Define(api *CircuitAPI, input CircuitInput) error
	Allocate() (maxReceipts, maxStorage, maxTransactions int)
}
```

### `Define`

Define defines your app circuit logic. The code you write in Define is a set of instructions that tells the framework "how to build the circuit". You could use if statements and loops for constructing the circuit, but as soon as the circuit is compiled, meaning the ifs and loops are run to build the circuit, the wiring is set in stone and there is no more concept of ifs and loops.&#x20;

The first parameter `api *CircuitAPI` contains a set circuit building blocks. [Read more](circuit-api.md)

The second parameter `input CircuitInput` contains the data you want to process in the circuit. You should only need to access `input.Receipts`, `input.StorageSlots`, and `input.Transactions`. [more on these data types](circuit-data-types.md#sdk.receipt-sdk.storageslot-sdk.transaction)

### `Allocate`

You need to declare your data "slot" allocations because circuit inputs cannot be dynamic like data structures in normal programs.

The only thing you need to worry about is that when you add data into BrevisApp using `AddReceipt`, `AddStorageSlot`, and `AddTransaction`, the number of items you add to each type cannot exceed (but can be less than) the number you declare for that type.

For example, if this is your `Allocate` function:

```go
func (c *AppCircuit) Allocate() (maxReceipts, maxStorage, maxTransactions int) {
    return 32, 0, 0
}
```

Then you can have a maximum of 1 receipt, 2 storage, and 3 transactions as data points. The sum of these values cannot exceed `NumMaxDataPoints`.

{% hint style="warning" %}
The less slots you allocate, the better your circuit will perform. You should always aim for allocating the least amount of slots possible. If you intend to build multiple circuits for your use case, the slot allocations for these circuits don't need to be the same.
{% endhint %}

{% hint style="warning" %}
&#x20;For performance optimization, allocate maxReceipts/maxStorage/maxTransaction as an _<mark style="color:orange;">**integral multiple of 32.**</mark>_ <mark style="color:red;">0 is allowed</mark>_<mark style="color:orange;">**.**</mark>_ Brevis app will use NextPowerOf2(maxReceipts+maxStorage+maxTransaction) as NumMaxDataPoints
{% endhint %}

Here is a visualization that may help you develop a mental model:

<figure><img src="../../.gitbook/assets/img2.png" alt=""><figcaption></figcaption></figure>
