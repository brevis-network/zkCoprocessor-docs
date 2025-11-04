# FAQ/Troubleshooting

## FAQ

<details>

<summary>How do I know what "storage key" value to provide?</summary>

[evm.storage](https://evm.storage) is a good tool for this. Just type in a contract address and the storage layout will be shown. The slot of a specific state variable looks like `0x0000...0002` in the "Storage" tab. The storage key of that slot is simply `keccak256(slot)` for a single storage variable. But it can get much more complicated than that if the variable doesn't take up 32 bytes and is grouped with another one, or if it's an array or mapping. You can read more about storage layout in general on the [solidity doc](https://docs.soliditylang.org/en/v0.8.24/internals/layout_in_storage.html) website.

</details>

## Troubleshooting Common Errors

<details>

<summary><code>"invalid witness size" / "witness length is invalid"</code></summary>

If you are seeing witness size related errors, try cleaning your circuit output directory and recompile/setup your circuit.

</details>

