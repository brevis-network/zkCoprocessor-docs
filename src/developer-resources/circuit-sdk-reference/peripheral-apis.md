# Peripheral APIs

Other than the APIs for building the circuit logic, the SDK also provides various other functions for:

* Compiling your circuit and setting up keys
* Generating/verifying proofs
* Testing you app circuit

## Manually Compiling the Circuit

You circuit needs to be compiled before you can generate a proof with it.

```go
appCircuit := &MyAppCircuit{ 
    // If you use any custom inputs, you MUST supply values for the input. The 
    // values you set don't matter but the number of values must be consistent 
    // between compiling time and proving time. This is because your input size 
    // determines circuit layout. And when the circuit is compiled, the layout of
    // your compiledCircuit is fixed.
    MyCustomInputSlice: []sdk.Uint248{
        ConstUint248(0), ConstUint248(0), ConstUint248(0)},
}
compiledCircuit, pk, vk, err := sdk.Compile(appCircuit, compileOutDir, srsDir)
```

> **Note:** 
### Pitfall Warning

When giving your custom inputs default values, the following won't work

```go
zero := ConstUint248(0)
appCircuit := &MyAppCircuit{
    MyCustomInputSlice: []sdk.Uint248{zero, zero, zero}, // won't work
}
```

The underlying circuit framework sees the three zeros as one input signal instead of three separate inputs because they are all one instances


#### `compileOutDir`

This is the output directory to save your compilation outputs (compiledCircuit, pk, and vk). A recommended practice is to have one directory for each circuit. The outputs will be saved under the configured `compileOutDir` as files names `compiledCircuit`, `pk`, and `vk`.

#### `srsDir`

Compiling requires downloading a structured reference string (SRS) provided by Brevis. You don't need to configure anything other than a cache directory `srsDir` to save the downloaded file as the downloading step is automatically handled.&#x20;

> **Note:** 
&#x20;Brevis generates the SRS file with Aztec Ignition Ceremony Data. The file size is more than 3G.  A good practice is to save them in a separate directory from your `compileOutDir`, and use the same `srsDir` for all your apps. Please [<mark style="color:red;">install curl</mark>](https://developers.greenwayhealth.com/developer-platform/docs/installing-curl) as a command line tool to speed up the download process.


#### Constraint Count

When you compile you will see output like this:

```
circuit compiled in 193.3395ms, number constraints 290546
```

Pay attention to "number constraints". This number is an important metric that basically tells you how big your circuit is. The bigger your circuit, the more memory you need and the slower a proof is generated. A rough benchmark is that a constraint count of 10 million can generate one proof in under a minute on the 32G M2 MacBook Pro. Your actual mileage may vary.

#### VK hash

You will also see the console prints out something that looks like this:

```
///////////////////////////////////////////////////////////////////////////////
// vk hash: 0x1d7f35f3a9b09f723857802db081adfa627b5cb389539ac04eedf6d422a52ed2
///////////////////////////////////////////////////////////////////////////////
```

This is the hashed value of your verifying key. You should record this value and store it in your app contract.

## Proving

Proving is straight-forward. It uses the previously acquired `circuitInput`, `compiledCircuit`, `pk`, and your circuit definition.

```go
witness, publicWitness, err := sdk.NewFullWitness(appCircuitAssignment, circuitInput)
proof, err := sdk.Prove(compiledCircuit, pk, witness)
```

### Verifying

Verifying is a cheap operation and is completely optional. You can choose to test verifying the proofs you generate before sending them to Brevis to make sure the proof and vk are correct.

```go
err := sdk.Verify(vk, publicWitness, proof)
```

## Circuit Testing

Testing utilities are located in the `github.com/brevis-network/brevis-sdk/test` package.

```go
// ProverSucceeded checks:
// - a proof can be generated with the application circuit/assignment and the 
//   sdk generated circuit inputs.
// - the generated proof can be verified.
ProverSucceeded(t *testing.T, app, assign sdk.AppCircuit, in sdk.CircuitInput)

// ProverFailed checks:
// - a proof cannot be generated with the application circuit & invalid 
//   assignment and the sdk generated circuit inputs.
ProverFailed(t *testing.T, app, assign sdk.AppCircuit, in sdk.CircuitInput)

// IsSolved checks if the given application circuit/assignment and the input 
// can be solved
IsSolved(t *testing.T, app, assign sdk.AppCircuit, in sdk.CircuitInput)
```

### `IsSolved`

This function is useful during development when you want to quickly debug and iterate on your circuit. It is a quick way to check if your circuit can be solved using the given inputs. This utility doesn't invoke the actual prover, so it's very fast.

### `ProverSucceeded`/`ProverFailed`

These utilities are like `IsSolved`, but they internally go through the entire proving/verifying cycle. You should use `ProverSucceeded` to check if a proof can be generated and verified with the valid data (completeness), and use `ProverFailed` to check that invalid data cannot produce valid proofs (soundness). This function is favored for testing before you go to deployment.
