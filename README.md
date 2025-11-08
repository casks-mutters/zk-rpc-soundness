# zk-rpc-soundness

## Overview
**zk-rpc-soundness** is a CLI tool that verifies the responsiveness and synchronization accuracy of any EVM-compatible RPC endpoint.  
It measures request latency, current block height, and time drift — useful for developers and researchers working on **Aztec**, **Zama**, and other zk-rollup or cryptographic networks.

## Features
- Measures average RPC latency  
- Detects if a node is lagging behind the chain head  
- Reports block timestamp and block height  
- Works with Ethereum mainnet, L2s, and private devnets  
- JSON output for automation or dashboards  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Set an RPC URL or use via CLI:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Basic usage:
   python app.py

Custom sampling:
   python app.py --samples 5 --delay 2.0

JSON output:
   python app.py --json

## Example Output
🕒 Timestamp: 2025-11-08T13:01:23.417Z  
🔧 zk-rpc-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1 (Ethereum Mainnet)  
🧱 Latest Block: 21051245  
⏰ Block Timestamp: 2025-11-08T13:00:56Z  
⚡ Average RPC Latency: 0.234s per request  
✅ Node block height is up-to-date.  
⏱️ Completed in 1.89s  

## Notes
- If latency is consistently high, consider switching to a regional RPC or dedicated node.  
- Block age greater than 30s indicates possible sync delay or overloaded node.  
- Works across all EVM-compatible networks.  
- Use JSON output for CI/CD or RPC monitoring systems.  
- Ideal for ensuring RPC soundness before zero-knowledge proof submission in **Aztec** or **Zama** deployments.  
- Exit codes:  
  `0` → Success  
  `2` → RPC or block fetch error.  
