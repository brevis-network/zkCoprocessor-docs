# Trusted Setup



Brevis SDK is built upon the PLONK proving backend, which requires a KZG trusted setup. The setup process of Brevis SDK circuits is based on Bn254 KZG SRS from the AZTEC Ignition MPC ceremony.

AZTEC ran Ignition, an MPC ceremony to generate a CRS for privacy network and other zero-knowledge systems like PLONK from October 25th 2019 to the January 2nd 2020.

**Generate SRS steps:**

* Get the ignition transcript files on Mainnet: [https://aztec-ignition.s3.eu-west-2.amazonaws.com/index.html#MAIN%20IGNITION](https://aztec-ignition.s3.eu-west-2.amazonaws.com/index.html#MAIN%20IGNITION/)
* Verify that each participant signed the SHA256 digest of each transcript file they generated. the verifier tool is provided by Gnark team: [https://github.com/Consensys/gnark-ignition-verifier](https://github.com/Consensys/gnark-ignition-verifier)
* Generate SRS file via [gnark-ignition-verifier](https://github.com/Consensys/gnark-ignition-verifier) main script, the participants generated 100.8 million BN254 points, Approximately corresponding to the constraints gates K = 26.

**Pubilc SRS resource:**

Link:   [https://kzg-srs.s3.us-west-2.amazonaws.com/kzg\_srs\_100800000\_bn254\_MAIN\_IGNITION](https://kzg-srs.s3.us-west-2.amazonaws.com/kzg_srs_100800000_bn254_MAIN_IGNITION)&#x20;

MD5 checksum: **0x2abd249241a7fe883379db93530365f8**
