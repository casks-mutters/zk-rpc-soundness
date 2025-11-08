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
- **Latency Meaning:** Average latency measures how fast your RPC node responds to basic queries like `eth_blockNumber`. Low latency (<0.5s) indicates healthy RPC performance.  
- **Block Age:** A block older than ~30 seconds usually signals the node is out of sync or connected to a congested network.  
- **Timeouts:** If a node is slow or non-responsive, consider using an alternative RPC provider.  
- **RPC Diversity:** You can test multiple endpoints (e.g., Infura, Alchemy, Blast, QuickNode) to find the most reliable one.  
- **Automation:** Integrate this script into your CI/CD pipeline or monitoring system to detect degraded RPC performance early.  
- **ZK Use Case:** In Aztec or Zama environments, consistent and responsive RPC nodes are critical for reproducible proofs and sound on-chain data.  
- **L2s & Testnets:** Works seamlessly with Arbitrum, Optimism, Base, Polygon, and all EVM-based chains.  
- **Advanced Monitoring:** You can extend the script to log results over time or compare block height across multiple RPCs to detect desynchronization.  
- **Security Note:** Always use HTTPS RPC URLs for production or sensitive workloads.  
- **Exit Codes:**  
  - `0` → Success  
  - `2` → RPC or block fetch failure.  
