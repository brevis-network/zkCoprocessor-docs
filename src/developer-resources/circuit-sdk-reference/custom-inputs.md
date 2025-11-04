# Custom Inputs

Custom inputs, or more canonically, private inputs are what makes our proofs zero-knowledge and succinct. Consider the following use case:

We want to send some users gifts if they can prove to our gift sender contract that their addresses are included in the merkle root recorded in some other contract's storage. This requires checking merkle proofs. But we don't actually need to let our gift sender contract know about these merkle proofs as long as we generate ZK proofs that proves the statement "there exists merkle proofs from these leaves to this storage value (a merkle root) of the contract". Such merkle proofs can be supplied as custom inputs.

```go
type AppCircuit struct{
    MerkleProof [8]sdk.Bytes32
}
// func (c *AppCircuit) Allocate() ...
// func (c *AppCircuit) Define() ...
```
