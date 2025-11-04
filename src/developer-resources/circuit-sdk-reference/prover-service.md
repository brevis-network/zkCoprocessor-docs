# Prover Service

The prover service is the most convenient way to quickly spin up a service from your circuit.&#x20;

### Setting up the Prover Service

```go
// Config for automatic management of compilation outputs
config := prover.ServiceConfig{
    // SetupDir saves the circuit compilation outputs (proving key, verifying key,
    // verifying key hash)
    SetupDir: "$HOME/circuitOut",
    // SrsDir saves the SRS files that will be automatically downloaded. These files
    // can be shared across different circuits. So the best practice is to have them
    // in a shared directory for all projects. Default to use the same dir as
    // SetupDir if not specified
    SrsDir:   "$HOME/kzgsrs",
    // RpcURL will be used to query on-chain data by sending rpc call.
    RpcURL string
    // Source chain id.
    ChainId int
}
// Spin up a new prover service for appCircuit. This automatically compiles your
// circuit and sets up proving/verifying keys if your circuit changes or if it's
// your first time compiling
proverService, err := prover.NewService(appCircuit, config)
// listen to port 33247
err = proverService.Serve(33247)
```

### Automatic Compilation Management

The compilation and setup steps of your application circuit is automatically taken care of. You are only providing two directory paths that tells the prover service where to save the output files on your disk.

### Interacting with the Prover Service

The prover service is designed to integrate tightly with the Typescript SDK, but you can also access its API directly if you are familiar with gRPC and protobuf.

#### Using the Typescript SDK

Please refer to the docs for [Typescript SDK](https://github.com/brevis-network/brevis-sdk-typescript).

#### Using gRPC

You can find the protobuf definitions in [this repo](https://github.com/brevis-network/brevis-proto/blob/d9a9843fc4562e9a3fdcbf16ec831d0e85bba08b/sdk/prover.proto#L9).

> **Note:** 
If you are using Go, you can simply import `github.com/brevis-network/brevis-sdk/sdk/proto/sdkproto`

