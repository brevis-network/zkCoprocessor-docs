# Circuit Data Types

## `DataInput`

`CircuitInput` is a parameter of your circuit definition function `Define`.  The only thing you care about are the three lists of receipts/storages/transactions. You can treat the data in these three `DataPoints` lists as proven to be valid. This is because when you submit your proof to Brevis, the provers there will check this data for you.

```go
type DataInput struct {
	Receipts     DataPoints[Receipt]
	StorageSlots DataPoints[StorageSlot]
	Transactions DataPoints[Transaction]
}
```

You can create a `sdk.DataStream` around the list you want to process or you can directly access them.

> **Note:** 
Not every data point in the lists is necessarily valid. For example, if you allocate 3 slots for receipts but add only two receipts through `app.AddReceipt`, then the last receipt item would remain empty. When using DataStream methods, e.g.`sdk.NewDataStream(input.Receipts).Mean(...)`,  empty checks are done for you so that when you do aggregation operations such as `Mean`, you won't account for data located at those empty slots. If you access `DataPoints` directly (e.g. inputs.Receipts\[3]), you are forgoing this automatic empty check.


## `CircuitVariable` Data Types

You must use the data types specifically defined for circuit use. You can still use custom Go types for non-circuit operations, but anything that goes into `CircuitAPI` and `DataStream` functions are circuit data types. These variables can be casted to each other through [casting](circuit-api.md#type-casting-functions) (some are not convertible to others yet, please pay attention to the documentation of each casting function). The following pre-defined types all implement the `CircuitVariable` interface.

### Primitive Types

#### `sdk.Uint32`

This type is the lowest cost type to use in circuit. It represents an unsigned integer up to 32 bits. You can perform arithmetics, comparisons, binary conversion, selection, and logic operations on it. This type could be useful in representing data like block number. If there are many comparisons, we recommend using Uint32 if you can ensure the value will not overflow.&#x20;

#### `sdk.Uint248`

This type is the default type to use in circuit because it's "native" to the underlying elliptic curve's scalar field. It represents an unsigned integer up to 248 bits. It is the return type of other type's operations (e.g. `Bytes32`'s `ToBinary` operation returns a list of `Uint248`). It is also used where boolean values are appropriate (e.g. the return type of `IsEqual` should be boolean but is represented using a `Uint248` 0 or 1). You can perform arithmetics, comparisons, binary conversion, selection, and logic operations on it. You should always prefer using Uint248 to represent data if possible.

#### `sdk.Int248`

This type supports representing negative numbers. Uses 1 bit as the sign bit, so the absolute value can only be up to 247 bits.

#### `sdk.Uint521`

This type supports arithmetics up to 521 bits. If you need to multiply two `Uint248`s and know that they can overflow, cast them to this type before doing the calculation. Note that this type internally uses field emulation and has much higher cost than Uint248 arithmetics. You should only use this whenever necessary.

#### `sdk.Bytes32`

This type is equivalent to solidity's bytes32, and in turn, is also used where uint256 needs to be represented. The `Value` fields in `Receipt.LogField`, `Transaction`, and `Storage` are all this type. You can only perform comparison and selection over variables of this type. `Bytes32` are used in many places instead of `Uint521` for performance reasons because most of the time a `Bytes32` can be down casted to `Uint248` (e.g. when you know that `Value` field in `StorageSlot` that is actually a `uint64` in a Solidity contract). Other times, we only use `Bytes32` for equality checks (hashes, keys, etc...). You can always cast to `Uint521` if you really need it.

### Composite Types

#### `sdk.List`

Lists can hold `CircuitVariable`s of a homogeneous type (e.g. `sdk.List[sdk.Uint248]`). List itself also implements the CircuitVariable interface. List is simply a Go slice under the hood, so you can use `append()` to add elements and `list[i]` to access elements.

#### `sdk.Tuple2 ... sdk.Tuple8`

There are 7 pre-defined Tuple types from size 2 to 8. This is your go-to method of defining your custom data structures. You can use any type that implements `CircuitVariable` in Tuple fields. Nested Tuples are also possible.

> **Note:** 
#### Tip:

If your Tuple gets too long, you can create a Go type alias for it to make your code more readable.

```go
type MySchema = sdk.Tuple8[
    sdk.Transaction, 
    sdk.Tuple2[Uint521, Uint521], 
    sdk.Int248, 
    sdk.Uint248, 
    sdk.Bytes32, 
    sdk.List[sdk.Uint248], 
    sdk.Uint248, 
    sdk.Receipt,
]
```


#### `sdk.Receipt`/`sdk.StorageSlot`/`sdk.Transaction`

These are the types of the input data of your app circuit.

```go
// Receipt is a collection of LogField.
type Receipt struct {
	BlockNum     Uint32
	// Block base fee
	BlockBaseFee Uint248  
	// Receipt index indicator
	MptKeyPath   Uint32
	Fields       [NumMaxLogFields]LogField
}

// LogField represents a single field of an event.
type LogField struct {
	// The contract from which the event is emitted
	Contract Uint248
	// The log position in receipt
	LogPos Uint32
	// The event ID of the event to which the field belong (aka topics[0])
	EventID Uint248
	// Whether the field is a topic (aka "indexed" as in solidity events)
	IsTopic Uint248
	// The index of the field. For example, if a field is the second topic of a log, then Index is 1; if a field is the
	// third field in the RLP decoded data, then Index is 2.
	Index Uint248
	// The value of the field in event, aka the actual thing we care about, only 32-byte fixed length values are supported.
	Value Bytes32
}
```

> **Note:** 
For each transaction receipt, you can choose to use up to `NumMaxLogFields` fields. Currently this limit is set to 3.


```go
type StorageSlot struct {
	BlockNum     Uint32
	// Block base fee
	BlockBaseFee Uint248
	// The contract to which the storage slot belong
	Contract Uint248
	// The storage slot
	Slot Bytes32
	// The storage slot value
	Value Bytes32
}
```

```go
type Transaction struct {
	BlockNum     Uint32
	// Block base fee
	BlockBaseFee Uint248
	// Transaction index indicator
	MptKeyPath   Uint32
	// Hash of rlpPrefix and transaction raw data 
	LeafHash Bytes32
}
```

> **Note:** 
Currently, only transactions of type 0 (legacy) and 2 (dynamic fee) are supported.


## Defining Constant Variables

You may declare constant variables in your circuit. Consider those the "hardwires" of your circuit. The `sdk` package contains some utility functions for this purpose. These functions are not a part of the Circuit API and should only be used outside of the circuit to initialize constant circuit variables.

```go
// ConstUint248 initializes a constant Uint248. This function does not generate
// circuit wires and should only be used outside of circuit. Supports all int and
// uint variants, bool, []byte (big-endian), *big.Int, and string inputs. If
// input is string, this function uses *big.Int SetString function to interpret
// the string
ConstUint248(data interface{}) Uint248

// ConstUint521 initializes a constant Uint521. This function does not generate
// circuit wires and should only be used outside of circuit. Supports all int and
// uint variants, bool, []byte (big-endian), *big.Int, and string inputs. If
// input is string, this function uses *big.Int SetString function to interpret
// the string
ConstUint521(data interface{}) Uint521

// ConstInt248 initializes a constant Int248. This function does not generate
// circuit wires and should only be used outside of circuit. The input big int
// can be negativ
ConstInt248(data *big.Int) Int248

// ConstBytes32 initializes a constant Bytes32 circuit variable. Panics if the
// length of the supplied data bytes is larger than 32
ConstBytes32(data []byte) Bytes32
```
