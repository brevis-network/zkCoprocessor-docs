# Legacy Deployments

{% hint style="info" %}
(_**Attention!**_) This page specifies our legacy deployments which will be **deprecated** in the future.&#x20;

This page is for reference only. If you want to integrate with Brevis, please use our [up-to-date deployments](contract-addresses-and-rpc-endpoints.md).
{% endhint %}

## Brevis SDK v0.1

**SDK version**: [https://github.com/brevis-network/brevis-sdk/tree/release/v0.1](https://github.com/brevis-network/brevis-sdk/tree/release/v0.1)

Brevis SDK V1 only supports same chain proving. Developer can choose **Optimism** or **Base Mainnet** to prove on-chain information

#### RPC Endpoint

<mark style="color:blue;">https://brvgw.brevis.network</mark>

#### **Optimism**

<table data-full-width="false"><thead><tr><th width="171">Contract</th><th>Address</th></tr></thead><tbody><tr><td>BrevisRequest</td><td><a href="https://optimistic.etherscan.io/address/0x9f5b558c95292f13fa9e0328ac4d3f129c2d9562">0x9f5b558c95292f13fa9e0328ac4d3f129c2d9562</a></td></tr><tr><td>BrevisProof</td><td><a href="https://optimistic.etherscan.io/address/0x6CD95817F275bDf5C9cC401CbCcbFfd99c7f186A">0x6CD95817F275bDf5C9cC401CbCcbFfd99c7f186A</a></td></tr></tbody></table>

#### **Base**&#x20;

<table data-full-width="false"><thead><tr><th width="171">Contract</th><th>Address</th></tr></thead><tbody><tr><td>BrevisRequest</td><td><a href="https://basescan.org/address/0x3463b37908cc3034c635f17f5a8012577cfc2663">0x3463b37908cc3034c635f17f5a8012577cfc2663</a></td></tr><tr><td>BrevisProof</td><td><a href="https://basescan.org/address/0x2294E22000dEFe09A307363f7aCD8aAa1fBc1983">0x2294E22000dEFe09A307363f7aCD8aAa1fBc1983</a></td></tr></tbody></table>

## Brevis SDK v0.2

**SDK version**: [https://github.com/brevis-network/brevis-sdk/tree/release/v0.2](https://github.com/brevis-network/brevis-sdk/tree/release/v0.2)

Brevis system supports proving data on the same chain including **Sepolia, Holesky,** and **BSC testnet**. You can choose proof request and the contract callback happens on the above chains. Meanwhile,  data from **Ethereum Mainnet** is available for developers on **Sepolia** and **Holesky**, by configuring the chainID in the [BrevisClient](brevis-sdk-typescript-reference/brevis-client.md#submit) section with the correct gateway endpoint.

#### **RPC Endpoint**

<mark style="color:blue;">https://appsdkv2.brevis.network</mark>

#### **Sepolia**

<table><thead><tr><th width="141.8515625">Contract</th><th>Addre</th></tr></thead><tbody><tr><td>BrevisRequest</td><td><a href="https://sepolia.etherscan.io/address/0x841ce48F9446C8E281D3F1444cB859b4A6D0738C">0x841ce48F9446C8E281D3F1444cB859b4A6D0738C</a></td></tr><tr><td>BrevisProof</td><td><a href="https://sepolia.etherscan.io/address/0xea80589a5f3A45554555634525deFF2EcB6CC4FF">0xea80589a5f3A45554555634525deFF2EcB6CC4FF</a></td></tr></tbody></table>

#### **Holesky**

<table><thead><tr><th width="141.8515625">Contract</th><th>Addre</th></tr></thead><tbody><tr><td>BrevisRequest</td><td><a href="https://holesky.etherscan.io/address/0xce17b03d7901173cbfa017b1ae3a9b8632f42c18">0xce17b03d7901173cbfa017b1ae3a9b8632f42c18</a></td></tr><tr><td>BrevisProof</td><td><a href="https://holesky.etherscan.io/address/0x728b3c4c8b88ad54b8118d4c6a65fac35e4cab6b">0x728b3c4c8b88ad54b8118d4c6a65fac35e4</a></td></tr></tbody></table>

#### **BSC Testnet**

<table><thead><tr><th width="141.8515625">Contract</th><th>Addre</th></tr></thead><tbody><tr><td>BrevisRequest</td><td><a href="https://testnet.bscscan.com/address/0xf7e9cb6b7a157c14bcb6e6bcf63c1c7c92e952f5">0xF7E9CB6b7A157c14BCB6E6bcf63c1C7c92E952f5</a></td></tr><tr><td>BrevisProof</td><td><a href="https://testnet.bscscan.com/address/0x2241C52472862038dFFdAb38b88410CAC2685D15">0x2241C52472862038dFFdAb38b88410CAC2685D15</a></td></tr></tbody></table>
