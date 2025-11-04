# Limits and Performance

Brevis is built as a highly performant and highly scalable ZK Coprocessor. As Brevis is currently running in Alpha mainnet with a low-capacity prover infrastructure, there are some limits in the public version worth mentioning here. However, note that our developer partners have implemented use cases handling more than 100X more scale than the public version. Therefore, we suggest developers to use the public version as a testbed for now and talk to us about your production launch.&#x20;

We also provide a brief overview of some performance benchmarks.&#x20;

## Data Access Limits in Public Alpha

{% hint style="info" %}
_The limits below are set up in a data-driven way according to Ethereum historical trace, which should cover >99% use cases._

_If your project requests higher limits, please_ [_reach out to us_](https://form.typeform.com/to/lduiliob?typeform-source=brevis.network)_. Brevis can support **much higher data limits** on a partner-request basis._&#x20;
{% endhint %}

### Transaction

Only transactions of _type 0 (legacy)_ and type _2 (dynamic fee)_ are supported.

### Storage

The maximum length of a storage value is **32 bytes**.

## Application Circuit Size Limit

Circuit size is described by a metric called "constraints". The constraints number is printed to console whenever you [compile your circuit](circuit-sdk-reference/peripheral-apis.md#compile). Your circuits will have a constraints upper limit of **2^26**.

## Application Circuit Output Limit

There is no artificially imposed upper limit for the amount of [circuit outputs](circuit-sdk-reference/circuit-api.md#output) you can have, but the more outputs you have, the bigger your circuit will be. The amount of outputs will be bound by the circuit size limit described above.

## Performance Benchmarks

Brevis will give you the lowest operation overhead, cost and the best user experience for your dApps. Brevis is highly horizontally scalable and can easily support much higher scalability than the current publicly available version. Please contact us if you have large-scale use cases.

The current public deployment is supported by a tiny cluster of 2 AWS servers with low-cost commodity hardware. In this deployment, Brevis achieves 5-10X faster proving performance than other solutions with comparable configuration of limits. See below benchmarks to get an idea.&#x20;

<table><thead><tr><th width="200">Data Type</th><th width="212">Number of Data Points</th><th>End-to-end Coprocessing Time*</th></tr></thead><tbody><tr><td>Transaction Receipt</td><td>64</td><td>58s</td></tr><tr><td>Transaction Receipt</td><td>256</td><td>68s</td></tr><tr><td>Transaction Receipt</td><td>1024</td><td>127s</td></tr><tr><td>Transaction Receipt</td><td>4096</td><td>344s</td></tr><tr><td>Storage Slot</td><td>64</td><td>69s</td></tr><tr><td>Storage Slot</td><td>256</td><td>81s</td></tr><tr><td>Storage Slot</td><td>1024</td><td>142s</td></tr><tr><td>Storage Slot</td><td>4096</td><td>350s</td></tr><tr><td>Transaction</td><td>64</td><td>65s</td></tr><tr><td>Transaction</td><td>256</td><td>77s</td></tr><tr><td>Transaction</td><td>1024</td><td>144s</td></tr><tr><td>Transaction</td><td>4096</td><td>323s</td></tr></tbody></table>

&#x20;\*End-to-end time here account for the time from the query to the App Service to the completion of aggregated application and data access proof generation.&#x20;
