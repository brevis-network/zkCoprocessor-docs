# Circuit API

## CircuitAPI

`sdk.CircuitAPI` is the top-level API that is passed to the user's `Define` function. It houses many building-block functions that aim to speed up the circuit building process.

#### Global Checks

```go
// AssertInputsAreUnique Asserts that all input data (Transaction, Receipt,
// StorageSlot) are different from each other
AssertInputsAreUnique()
```

#### Output Functions

Data output from the output functions are eventually exposed in your on-chain contracts.

```go
// OutputBytes32 adds an output of solidity bytes32/uint256 type
OutputBytes32(v Bytes32)

// OutputBool adds an output of solidity bool type
OutputBool(v Uint248)

// OutputUint adds an output of solidity uint_bitSize type where N is in range
// [8, 248] with a step size 8. e.g. uint8, uint16, ..., uint248. Panics if a
// bitSize of non-multiple of 8 is used. Panics if the bitSize exceeds 248. For
// outputting uint256, use OutputBytes32 instead
OutputUint(bitSize int, v Uint248)

// OutputAddress adds an output of solidity address type.
OutputAddress(v Uint248)
```

> **Note:** 
You can output as many variables as you want, but since all circuits have a limited size, the actual amount of outputs you can have is bound by the upper limit of the circuit size.


#### Type Casting Functions

```go
// ToBytes32 casts the input to a Bytes32 type. Supports Bytes32, Int248,
// Uint521, and Uint248.
ToBytes32(i interface{}) Bytes32

// ToUint521 casts the input to a Uint521 type. Supports Uint521, Bytes32,
// Uint248
ToUint521(i interface{}) Uint521

// ToUint248 casts the input to a Uint248 type. Supports Uint248, Int248,
// Bytes32, and Uint521
ToUint248(i interface{}) Uint248

// ToInt248 casts the input to a Int248 type. Supports Int248, Uint248,
// and Bytes32
ToInt248(i interface{}) Int248
```

#### Dynamic Storage Key Functions

You should use these function if you find the storage key you want to compute can only be deteremined at runtime. If you know the storage you are interested in is fixed, you should compute these keys outside of the circuit and initialize them with `sdk.ConstBytes32()`

```go
// StorageKey computes the storage key for an element in a solidity state variable
func (api *CircuitAPI) StorageKey(slot Bytes32) Bytes32

// StorageKeyOfArrayElement computes the storage key for an element in a solidity
// array state variable. arrStorageKey is the storage key for the plain slot of
// the array variable. index determines the array index. offset determines the
// offset (in terms of bytes32) within each array element.
func (api *CircuitAPI) StorageKeyOfArrayElement(
    arrStorageKey Bytes32, elementSize int, index, offset Uint248) Bytes32

// StorageKeyOfStructFieldInMapping computes the storage key for a struct field
// stored in a solidity mapping. Implements keccak256(h(k) | p) for computing
// mapping or nested mapping's storage key where the value is a struct The
// mapping keys are of the order which you would access the solidity mapping. For
// example, to access nested mapping at slot 1 value with m[a][b] and
// subsequently the 4th index of the struct value, use
// StorageKeyOfStructFieldInMapping(1, 4, a, b). If your a and b are not of
// Bytes32 type, cast them to Bytes32 first using api.ToBytes32.
//
// https://docs.soliditylang.org/en/v0.8.24/internals/layout_in_storage.html#mappings-and-dynamic-arrays
//
// IMPORTANT NOTE: the result hash is actually the MPT key of the storage, which is
// keccak256(storageKey). So the final formula is keccak256(keccak256(h(k) | p)).
func (api *CircuitAPI) StorageKeyOfStructFieldInMapping(
	slot, offset int, mappingKey Bytes32, nestedMappingKeys ...Bytes32) Bytes32
```

## Data Type Specific APIs

### Uint248 API

```go
// ToBinary decomposes the input v to a list (size n) of little-endian binary
// digits
ToBinary(v Uint248, n int) List[Uint248]

// FromBinary interprets the input vs as a list of little-endian binary digits
// and recomposes it to a Uint248
FromBinary(vs ...Uint248) Uint248

// Add returns a + b. Overflow can happen if a + b > 2^248
Add(a, b Uint248, other ...Uint248) Uint248

// Sub returns a - b. Underflow can happen if b > a
Sub(a, b Uint248) Uint248

// Mul returns a * b. Overflow can happen if a * b > 2^248
Mul(a, b Uint248) Uint248

// Div computes the standard unsigned integer division (like Go) and returns the
// quotient and remainder
Div(a, b Uint248)) (quotient, remainder Uint248)

// Sqrt returns √a
Sqrt(a Uint248) Uint248

// IsZero returns 1 if a == 0, and 0 otherwise
IsZero(a Uint248) Uint248

// IsEqual returns 1 if a == b, and 0 otherwise
IsEqual(a, b Uint248) Uint248

// IsLessThan returns 1 if a < b, and 0 otherwise
IsLessThan(a, b Uint248) Uint24

// IsGreaterThan returns 1 if a > b, and 0 otherwise
IsGreaterThan(a, b Uint248) Uint248

// And returns 1 if a && b [&& other[0] [&& other[1]...]] is true, and 0 otherwise
And(a, b Uint248, other ...Uint248) Uint248

// Or returns 1 if a || b [|| other[0] [|| other[1]...]] is true, and 0 otherwise
Or(a, b Uint248, other ...Uint248) Uint248

// Not returns 1 if a is 0, and 0 if a is 1. The user must make sure a is either
// 0 or 1
Not(a Uint248) Uint248

// Select returns a if s == 1, and b if s == 0
Select(s Uint248, a, b Uint248) Uint248

// AssertIsEqual asserts a == b
AssertIsEqual(a, b Uint248)

// AssertIsLessOrEqual asserts a <= b
AssertIsLessOrEqual(a, b Uint248)

// AssertIsDifferent asserts a != b
AssertIsDifferent(a, b Uint248)
```

### Uint521 API

```go
// ToBinary decomposes the input v to a list (size n) of little-endian binary digits
ToBinary(v Uint521, n int) List[Uint248

// FromBinary interprets the input vs as a list of little-endian binary digits
// and recomposes it to a Uint521
FromBinary(vs ...Uint248) Uint521

// Add returns a + b. Overflow can happen if a + b > 2^521
Add(a, b Uint521) Uint521

// Sub returns a - b. Underflow can happen if b > a
Sub(a, b Uint521) Uint521

// Mul returns a * b. Overflow can happen if a * b > 2^521
Mul(a, b Uint521) Uint521

// Div computes the standard unsigned integer division (like Go) and returns the
// quotient and remainder. Uses QuoRemHint
Div(a, b Uint521) (quotient, remainder Uint521)

// Select returns a if s == 1, and b if s == 0
Select(s Uint248, a, b Uint521) Uint521

// IsEqual returns 1 if a == b, and 0 otherwise
IsEqual(a, b Uint521) Uint248

// AssertIsEqual asserts a == b
AssertIsEqual(a, b Uint521)

// AssertIsLessOrEqual asserts a <= b
AssertIsLessOrEqual(a, b Uint521)
```

### Int248 API

```go
// ToBinary decomposes the input v to a list (size n) of little-endian binary digits
ToBinary(v Int248) List[Uint248]

// FromBinary interprets the input vs as a list of little-endian binary digits
// and recomposes it to an Int248. The MSB (most significant bit) of the input is
// interpreted as the sign bit
FromBinary(vs ...Uint248) Int248

// IsEqual returns 1 if a == b, and 0 otherwise
IsEqual(a, b Int248) Uint248

// IsLessThan returns 1 if a < b, and 0 otherwise
IsLessThan(a, b Int248) Uint248

// IsGreaterThan returns 1 if a > b, and 0 otherwise
IsGreaterThan(a, b Int248) Uint248

// IsZero returns 1 if a == 0, and 0 otherwise
IsZero(a Int248) Uint248

// ABS returns the absolute value of a
ABS(a Int248) Uint248

// Select returns a if s == 1, and b if s == 0
Select(s Uint248, a, b Int248) Int248

// AssertIsEqual asserts a == b
AssertIsEqual(a, b Int248)

// AssertIsDifferent asserts a != b
AssertIsDifferent(a, b Int248)
```

### Bytes32 API

```go
// ToBinary decomposes the input v to a list (size 256) of little-endian binary digits
ToBinary(v Bytes32) List[Uint248]

// FromBinary interprets the input vs as a list of little-endian binary digits
// and recomposes it to a Bytes32. Input size can be less than 256 bits, the
// input is padded on the MSB end with 0s.
FromBinary(vs ...Uint248) Bytes32

// IsEqual returns 1 if a == b, and 0 otherwise
IsEqual(a, b Bytes32) Uint248

// Select returns a if s == 1, and b if s == 0
Select(s Uint248, a, b Bytes32) Bytes32

// IsZero returns 1 if a == 0, and 0 otherwise
IsZero(a Bytes32) Uint248

// AssertIsEqual asserts a == b
AssertIsEqual(a, b Bytes32)

// AssertIsDifferent asserts a != b
AssertIsDifferent(a, b Bytes32)
```
