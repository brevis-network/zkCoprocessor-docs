# Building the App Circuit

Our app's goal is to allow anyone to prove to an on-chain smart contract that an address made a USDC transfer with volume more than 500 USDC. We are going to implement this app step by step. You can find the finished version in this [Github repo](https://github.com/brevis-network/brevis-quickstart-ts).&#x20;

## Writing the Circuit

Edit [circuit.go](https://github.com/brevis-network/brevis-quickstart-ts/blob/main/prover/circuits/circuit.go) and write our circuit


```go
package circuits

import (
	"github.com/brevis-network/brevis-sdk/sdk"
)

type AppCircuit struct{}

var USDCTokenAddr = sdk.ConstUint248("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
var minimumVolume = sdk.ConstUint248(500000000) // minimum 500 USDC
var _ sdk.AppCircuit = &AppCircuit{}

func (c *AppCircuit) Allocate() (maxReceipts, maxStorage, maxTransactions int) {
	// Our app is only ever going to use one storage data at a time so
	// we can simply limit the max number of data for storage to 1 and
	// 0 for all others
	return 32, 0, 0
}

func (c *AppCircuit) Define(api *sdk.CircuitAPI, in sdk.DataInput) error {
	receipts := sdk.NewDataStream(api, in.Receipts)
	receipt := sdk.GetUnderlying(receipts, 0)

	// Check logic
	// The first field exports `from` parameter from Transfer Event
	// It should use the second topic in Transfer Event log
	api.Uint248.AssertIsEqual(receipt.Fields[0].Contract, USDCTokenAddr)
	api.Uint248.AssertIsEqual(receipt.Fields[0].IsTopic, sdk.ConstUint248(1))
	api.Uint248.AssertIsEqual(receipt.Fields[0].Index, sdk.ConstUint248(1))

	// Make sure two fields uses the same log to make sure account address linking with correct volume
	api.Uint32.AssertIsEqual(receipt.Fields[0].LogPos, receipt.Fields[1].LogPos)

	// The second field exports `Volume` parameter from Transfer Event
	// It should use Data in Transfer Event log
	api.Uint248.AssertIsEqual(receipt.Fields[1].IsTopic, sdk.ConstUint248(0))
	api.Uint248.AssertIsEqual(receipt.Fields[1].Index, sdk.ConstUint248(0))

	// Make sure this transfer has minimum 500 USDC volume
	api.Uint248.AssertIsLessOrEqual(minimumVolume, api.ToUint248(receipt.Fields[1].Value))

	api.OutputUint(64, api.ToUint248(receipt.BlockNum))
	api.OutputAddress(api.ToUint248(receipt.Fields[0].Value))
	api.OutputBytes32(receipt.Fields[1].Value)
	return nil
}
```


## Testing the Circuit

Edit [circuit\_test.go](https://github.com/brevis-network/brevis-quickstart-ts/blob/main/prover/circuits/circuit_test.go) for circuit testing. First, we assign correct values to the circuit input. Then, we use `test.ProverSucceeded` to test if our circuit can successfully generate a proof using the correct input.

[Read more on testing here](../brevis-app-workflow/application-circuit.md#circuit-testing)


```go
// ...

func TestCircuit(t *testing.T) {
	rpc := "RPC_URL"
	localDir := "$HOME/circuitOut/myBrevisApp"
	app, err := sdk.NewBrevisApp(1, rpc, localDir)
	check(err)

	txHash := common.HexToHash(
		"0x8a7fc50330533cd0adbf71e1cfb51b1b6bbe2170b4ce65c02678cf08c8b17737")

	app.AddReceipt(sdk.ReceiptData{
		TxHash: txHash,
		Fields: []sdk.LogFieldData{
			{
				IsTopic:    true,
				LogPos:     0,
				FieldIndex: 1,
			},
			{
				IsTopic:    false,
				LogPos:     0,
				FieldIndex: 0,
			},
		},
	})

	appCircuit := &AppCircuit{}
	appCircuitAssignment := &AppCircuit{}

	circuitInput, err := app.BuildCircuitInput(appCircuit)
	check(err)

	///////////////////////////////////////////////////////////////////////////////
	// Testing
	///////////////////////////////////////////////////////////////////////////////

	test.ProverSucceeded(t, appCircuit, appCircuitAssignment, circuitInput)
} 
```


## Spin Up a Prover for Your AppCircuit


```go
proverService, err := prover.NewService(&AppCircuit{}, config)
// ...
err = proverService.Serve(33247)
// ...
```


Then, we run the main program to start up the prover

```
go run main.go
```

<details>

<summary>Console Output</summary>

```
>> compiling circuit
10:34:52 INF compiling circuit
ignoring uninitialized slice: Input_StorageSlots_Toggles []frontend.Variable
ignoring uninitialized slice: Input_Transactions_Toggles []frontend.Variable
10:34:52 INF parsed circuit inputs nbPublic=6 nbSecret=1089
ignoring uninitialized slice: Input_StorageSlots_Toggles []frontend.Variable
ignoring uninitialized slice: Input_Transactions_Toggles []frontend.Variable
ignoring uninitialized slice: Input_StorageSlots_Toggles []frontend.Variable
ignoring uninitialized slice: Input_Transactions_Toggles []frontend.Variable
commit output: rounds 1, data len 480, padded len 1088
10:34:52 INF building constraint builder nbConstraints=608462
circuit compiled in 408.001292ms, number constraints 608462
circuit digest 0x1dfdcf1616c15230b5bcd7555570e324647743ca9111e968a6519e33136b036e
trying to read setup from cache...
no setup matching circuit digest 0x0e299aa204fde71d5da9b94e7b905857ba1ce912ec37ad00f54f1bb2fdea0705 is found in /Users/xxx/circuitOut
>> setup
size system 608468
size lagrange 1048576
init SRS disk cache dir /Users/xxx/kzgsrs
fetching srs ignition from file
srs ignition not found in file
downloading file https://kzg-srs.s3.us-west-2.amazonaws.com/kzg_srs_100800000_bn254_MAIN_IGNITION
writing srs ignition file
srs iginition ready
setup done in 2.392068s
///////////////////////////////////////////////////////////////////////////////
// vk hash: 0x25d2751bfc09b1222b834f3043762dad7e1591671f8c03456996cabe53a95c71
///////////////////////////////////////////////////////////////////////////////

67143336 bytes written to /Users/xxx/circuitOut/0x1dfdcf1616c15230b5bcd7555570e324647743ca9111e968a6519e33136b036e/pk
34368 bytes written to /Users/xxx/circuitOut/0x1dfdcf1616c15230b5bcd7555570e324647743ca9111e968a6519e33136b036e/vk
>> scan local storage: /Users/xxx/circuitOut/input/input/data.json
>> finish scan local storage: /Users/xxx/circuitOut/input/input/data.json
>> serving prover REST API at port 33257
>> serving prover GRPC at port 33247
```

</details>

> **Note:** 
command line tool [_**curl**_](https://everything.curl.dev/index.html) is required for downloading srs ignition file.&#x20;

At the same time, you may download it through browser directly and put it into your srs file folder. Brevis sdk will use $HOME/kzgsrs/kzg\_srs\_100800000\_bn254\_MAIN\_IGNITI as _<mark style="color:red;">**file path**</mark>_ if srsDir configuration is $HOME/kzgsrs.


#### &#x20;The VK Hash

Notice the highlighted log that look like this

```
///////////////////////////////////////////////////////////////////////////////
// vk hash: 0x25d2751bfc09b1222b834f3043762dad7e1591671f8c03456996cabe53a95c71
///////////////////////////////////////////////////////////////////////////////
```

This is the hash of your circuit's verifying key. You must store this hash in your contract and check it when handling contract callbacks. More on this in later steps.
