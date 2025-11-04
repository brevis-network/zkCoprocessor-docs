# DataStream API

The data streams is an abstraction around the `sdk.CircuitVariable` interface. This abstraction aims to enable the developer to quickly process the data series in the familiar MapReduce style and not worry about the underlying circuitry (most of the time).

### The `sdk.CircuitVariable` Interface

Any type that satisfy this interface can be used in DataStreams. That means all pre-defined [circuit data types](circuit-data-types.md) can be used in data streams.&#x20;

> **Note:** 
It might be tempting to define your own struct that conforms to this interface and use them in data streams, but it can be error prone. Most of the time, you should find the TupleN types good enough for your needs.


## Data Stream Functions


```go
// GetUnderlying gets an element from the DataStream. Performed on the underlying data
// directly. It also requires the underlying data slot is valid
GetUnderlying[T CircuitVariable](ds *DataStream[T], index int) T

// RangeUnderlying selects a range of the data stream. Performed on the underlying data directly.
RangeUnderlying[T CircuitVariable](ds *DataStream[T], start, end int) *DataStream[T]

// WindowUnderlying splits a DataStream into many equal sized List. Performed on the
// underlying data directly. Panics if `size` does not divide the length of the
// underlying list. Use Range to cut the list length into a multiple of `size`
// first
WindowUnderlying[T CircuitVariable](ds *DataStream[T], size int, step ...int) *DataStream[List[T]]

// Map maps each valid element in the data stream by calling the user defined mapFunc
type MapFunc[T, R CircuitVariable] func(current T) R
Map[T, R CircuitVariable](ds *DataStream[T], mapFunc MapFunc[T, R]) *DataStream[R]

// Reduce reduces the data stream to another CircuitVariable
type ReduceFunc[T, R CircuitVariable] func(accumulator R, current T) (newAccumulator R)
Reduce[T, R CircuitVariable](ds *DataStream[T], initial R, reduceFunc ReduceFunc[T, R]) R

// FilterFunc must return 1/0 to include/exclude `current` in the filter result
type FilterFunc[T CircuitVariable] func(current T) Uint248
Filter[T CircuitVariable](ds *DataStream[T], filterFunc FilterFunc[T]) *DataStream[T]

// AssertFunc returns 1 if the assertion passes, and 0 otherwise
type AssertFunc[T CircuitVariable] func(current T) Uint248
// AssertEach asserts on each valid element in the data stream
AssertEach[T CircuitVariable](ds *DataStream[T], assertFunc AssertFunc[T])

// SortFunc returns 1 if a, b are sorted, 0 if not.
type SortFunc[T CircuitVariable] func(a, b T) Uint248
// IsSorted returns 1 if the data stream is sorted to the criteria of sortFunc, 0 if not.
IsSorted[T CircuitVariable](ds *DataStream[T], sortFunc SortFunc[T]) Uint248

// AssertSorted Performs the sortFunc on each valid pair of data points and assert the result to be 1.
AssertSorted[T CircuitVariable](ds *DataStream[T], sortFunc SortFunc[T])

// Count returns the number of valid elements (i.e. toggled on) in the data stream.
Count[T CircuitVariable](ds *DataStream[T]) Uint248 

type ZipMap2Func[T0, T1, R CircuitVariable] func(a T0, b T1) R
// ZipMap2 zips a data stream with a list and apply the map function over the
// zipped data. The underlying toggles of the result data stream depends on the
// toggles from the source data stream. Panics if the underlying data lengths
// mismatch
// Example: ZipMap2([1,2,3], [4,5,6], mySumFunc) -> [5,7,9]
ZipMap2[T0, T1, R CircuitVariable](a *DataStream[T0], b List[T1], zipFunc ZipMap2Func[T0, T1, R]) *DataStream[R]

type ZipMap3Func[T0, T1, T2, R CircuitVariable] func(a T0, b T1, c T2) R
// ZipMap3 zips a data stream with two other lists and apply the map function
// over the zipped data. The underlying toggles of the result data stream depends
// on the toggles from the source data stream.
// Example: ZipMap3([1,2,3], [4,5,6], [7,8,9], mySumFunc) -> [12,15,18]
ZipMap3[T0, T1, T2, R CircuitVariable](a *DataStream[T0], b List[T1], c List[T2], zipFunc ZipMap3Func[T0, T1, T2, R]) *DataStream[R]

type GetValueFunc[T any] func(current T) Uint248
// GroupBy a given field (identified through the field func), call reducer on
// each group, and returns a data stream in which each element is an aggregation
// result of the group. The optional param maxUniqueGroupValuesOptional can be
// supplied to optimize performance. It assumes the worst case (all values in the
// data stream are unique) if no maxUniqueGroupValuesOptional is configured.
GroupBy[T, R CircuitVariable](
	ds *DataStream[T],
	reducer ReduceFunc[T, R],
	reducerInit R,
	field GetValueFunc[T],
	maxUniqueGroupValuesOptional ...int,
) (*DataStream[R], error)

// MinGeneric finds out the minimum value from the data stream with the user
// defined sort function. Uses Reduce under the hood. Note if the data stream is
// empty (all data points are toggled off), this function returns MaxUint248.
MinGeneric[T CircuitVariable](ds *DataStream[T], initialMin T, lt SortFunc[T]) T

// MaxGeneric finds out the maximum value from the data stream with the user
// defined sort function. Uses Reduce under the hood. Note if the data stream is
// empty (all data points are toggled off), this function returns 0.
MaxGeneric[T CircuitVariable](ds *DataStream[T], initialMax T, gt SortFunc[T]) T

// Min finds out the minimum value from the data stream. Uses MinGeneric. Note if
// the data stream is empty (all data points are toggled off), this function
// returns MaxUint248.
Min(ds *DataStream[Uint248]) Uint248

// Max finds out the maximum value from the data stream. Uses MaxGeneric. Note if
// the data stream is empty (all data points are toggled off), this function
// returns 0.
Max(ds *DataStream[Uint248]) Uint248

// Sum sums values of the selected field in the data stream. Uses Reduce
Sum(ds *DataStream[Uint248]) Uint248

// Mean calculates the arithmetic mean over the selected fields of the data stream. Uses Sum.
Mean(ds *DataStream[Uint248]) Uint248

// Show pretty prints the data stream. Useful for debugging. 
Show()
```

