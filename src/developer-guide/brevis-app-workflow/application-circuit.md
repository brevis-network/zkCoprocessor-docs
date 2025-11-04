
# Application Circuit

The application circuit is a Go program and is the core part of your Brevis app. It is where you process the data you obtained in the data access step with your intended business logic. Even though you are indeed writing a ZK circuit, you don't actually need to know anything about ZK. This is because Brevis's SDK has abstracted away many low-level circuit framework details and only exposes easy-to-use APIs. When certain low-level details have to be exposed, we will explain what needs to be done clearly.&#x20;

### Dependencies

```sh
go get github.com/brevis-network/brevis-sdk
```

### How to Build a Circuit

To implement an application circuit, you need to:

1. Define a struct that houses your custom inputs (custom inputs are optional). This is where you specify things like user wallet addresses, trading pairs, time periods or other "variables" that are going to be different across each query to your App Service.
2. Implement the `AppCircuit` interface that has two methods `Allocate` and `Define` .
3. Build your computation logic in `Define` with the help of `sdk.CircuitAPI`and `sdk.DataStream`
4. Output the computation result using various output methods from `sdk.CircuitAPI`

The circuit must implement the sdk.AppCircuit Interface:

```go
type AppCircuit interface {
	Define(api *CircuitAPI, input DataInput) error
	Allocate() (maxReceipts, maxSlots, maxTransactions int)
}
```

* `Define` is where you write your circuit logic.&#x20;
* `Allocate` defines the **maximal** number of receipts/storage slots/transactions your application is going to use. Note that the higher the upper bounds are, the slower the application circuit is going to run for the same number of actual inputs. Read [more on Allocate](../../developer-resources/circuit-sdk-reference/app-circuit-interface.md#allocate) to understand the best practices for writing your app circuit.

Here is a demonstration of a custom app circuit in action:


```go
package app

import "github.com/brevis-network/brevis-sdk/sdk"

// Must be a struct
type AppCircuit struct{
    // Custom inputs. These fields must be exported (first letter capitalized)
    // These are the inputs that can be different for each proof you generate
    // using the same circuit
    MyInputVar     sdk.Uint248
    MyInputBytes32 sdk.Bytes32
}

// The struct AppCircuit must implement the sdk.AppCircuit interface
var _ sdk.AppCircuit = &AppCircuit{} 

func (c *AppCircuit) Allocate() (maxReceipts, maxStorage, maxTransactions int) {
    // When we return 32, 64, 0, it means that we are allowing our circuit to process 
    // a maximum of 32 receipts, 64 storages, and 0 transactions
    return 32, 64, 0
}

var ConstEventID = ParseEventID(/* 0x123456... */)

func (c *AppCircuit) Define(api *sdk.CircuitAPI, input sdk.DataInput) error {
    // You can access the data you added through app.AddReceipt etc.
    receipts := sdk.NewDataStream(api, input.Receipts)
    
    // Checking some the receipts properties against some constants
    // In this example, by checking these, you are proving to your 
    // contract that you have checked that all events have a certain
    // event ID
    sdk.AssertEach(receipts, func(receipt sdk.Receipt) Variable {
        return api.Equal(receipt.Fields[0].EventID, ConstEventID)
    })

    // You can then perform various data stream operations on the data. 
    // You can find the usage of specific API later.
    blockNums := sdk.Map(receipts, func(r sdk.Receipt) sdk.Uint248 {
        return api.ToUint248(r.BlockNum)
    })
    minBlockNum := sdk.Min(blockNums)
    
    values := sdk.Map(receipts, func(r sdk.Receipt) sdk.Uint248 {
        return api.ToUint248(r.Value)
    })
    sum := sdk.Sum(values)
    
    // sdk.Reduce(...)
    // sdk.GroupBy(...)
    // and more ...
    
    // You can output any number of computation results using sdk.OutputXXX APIs 
    // These results will be available for use in your contract when the proof 
    // is verified on-chain 
    api.OutputUint(64, minBlockNum)
    api.OutputUint(248, sum)
    // more output...
    
    return nil
}
```


## Circuit API

`sdk.CircuitAPI` is supplied to your circuit as a parameter of your `Define` function. It houses many  building blocks for circuit constructions. All control flows, logic operations, and math must go through circuit APIs.

* Global Checks: `AssertInputsAreUnique`
* Hashing: `StorageKey`, `StorageKeyOfArrayElement`, `StorageKeyOfStructFieldInMapping`
* Output: `OutputUint`, `OutputBytes32`, `OutputBool`, `OutputAddress`
* Casting: `ToBytes32`, `ToUint521`, `ToUint248`, `ToInt248`

### Type-Specific Circuit APIs

The sdk.CircuitAPI struct has several submodules for type specific operations: Uint32, Uint248, Uint521, Int248, Bytes32.

Not every type's API has the same set of operations. In general you will be looking to use the sdk.Uint248 type most of the time. The following is a list of operations supported for Uint248:

* Arithmetics:  `Add`, `Sub`, `Mul`, `Div`, `Sqrt`
* Logic: `Select`, `And`, `Or`, `Not`
* Comparison: `IsZero`, `IsEqual`, `IsLessThan`, IsGreaterThan
* Binary: `ToBinary`, `FromBinary`
* Assertions: `AssertIsEqual`, `AssertIsDifferent`, `AssertIsLessThanOrEqual`

An exhaustive list of circuit functions can be found under Circuit SDK Reference > [Circuit API](../../developer-resources/circuit-sdk-reference/circuit-api.md).

## Data Stream API

The data stream API allows you to perform data analysis computations over receipts/storages/transactions in a MapReduce style. To create a `DataStream`, simply wrap it around the data:

```go
txs := sdk.NewDataStream(api, input.Transactions)

mapped := sdk.Map(txs, func(tx sdk.Transaction) sdk.Uint248 { /* ... */ })

reduced := sdk.Reduce(
    mapped, // data to reduce on
    ConstUint248(0), // reducer base case
    func(acc sdk.Uint248, current sdk.Uint248) (newAcc sdk.Uint248) { /* reducer */ },
)
```

You can find a detailed listing of the data stream functions in [Data Stream API doc](../../developer-resources/circuit-sdk-reference/datastream-api.md).

## Circuit Inputs

The `input CircuitInput` parameter passed into your `Define` function is built from the [data preparation](data-access-module.md#querying-the-data) step. It contains the `Receipts`, `StorageSlots`, and `Transactions` that your circuit wants to process. Read [more on these types](../../developer-resources/circuit-sdk-reference/circuit-data-types.md#sdk.receipt-sdk.storageslot-sdk.transaction).

## Circuit Outputs

You can output your computation results and use them in your contract through the [output functions](../../developer-resources/circuit-sdk-reference/circuit-api.md#output). The values you output will be exposed to your app contract.

```go
api.OutputUint(64, someVariable)
api.OutputAddress(someAddress)
// and more ...
```

## Circuit Testing

The `brevis-sdk/test` package contains some testing utilities.

During development: use `test.IsSolved` to help in debugging circuit logic.

Before deployment: use `test.ProverSucceeded` and `test.ProverFailed` to check that your proofs are complete and sound.&#x20;

Read more about these utilities in [Circuit Testing](../../developer-resources/circuit-sdk-reference/peripheral-apis.md#circuit-testing).&#x20;
