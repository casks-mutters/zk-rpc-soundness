# app.py
import os
import sys
import json
import time
import argparse
from datetime import datetime
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

NETWORK_NAMES = {
    1: "Ethereum Mainnet",
    5: "Goerli Testnet",
    11155111: "Sepolia Testnet",
    137: "Polygon Mainnet",
    42161: "Arbitrum One",
    10: "Optimism Mainnet",
    8453: "Base Mainnet",
}

def fetch_block_latency(w3: Web3, samples: int = 3, delay: float = 1.0) -> float:
    """
    Measure average latency of RPC calls to fetch 'latest' block numbers.
    """
    total = 0.0
    for _ in range(samples):
        start = time.time()
        try:
            _ = w3.eth.block_number
        except Exception as e:
            raise RuntimeError(f"RPC call failed: {e}")
        total += time.time() - start
        time.sleep(delay)
    return total / samples

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-rpc-soundness — measure RPC responsiveness and block height stability across EVM-compatible networks (for Aztec/Zama and Web3 monitoring)."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--samples", type=int, default=3, help="Number of latency samples (default: 3)")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds (default: 1.0)")
    p.add_argument("--json", action="store_true", help="Output results as JSON")
    return p.parse_args()

def main() -> None:
    start = time.time()
    args = parse_args()

    # ✅ Validate RPC URL
    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": 10}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL or --rpc argument.")
        sys.exit(1)

    # Print header
    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-rpc-soundness")
    print(f"🔗 RPC: {args.rpc}")

    # Network info
    try:
        chain_id = w3.eth.chain_id
        network_name = NETWORK_NAMES.get(chain_id, "Unknown Network")
        print(f"🧭 Chain ID: {chain_id} ({network_name})")
    except Exception:
        chain_id = None
        network_name = "Unknown"
        print("⚠️ Could not fetch chain ID.")

    # Measure latency
    try:
        latency = fetch_block_latency(w3, samples=args.samples, delay=args.delay)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)


     #New: Retry fetching the latest block up to 3 times
    for attempt in range(3):
        try:
            block = w3.eth.get_block("latest")
            block_number = block.number
            timestamp = block.timestamp
            break
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1}/3 failed to fetch latest block: {e}")
            time.sleep(2)
    else:
        print("❌ Failed to fetch latest block after 3 retries.")
        sys.exit(2)

    # Print metrics
    print(f"🧱 Latest Block: {block_number}")
    print(f"⏰ Block Timestamp: {datetime.utcfromtimestamp(timestamp).isoformat()}Z")
    print(f"⚡ Average RPC Latency: {latency:.3f}s per request")

    # Sanity check for block delay
    block_age = time.time() - timestamp
    if block_age > 30:
        print(f"⚠️ Warning: Block is {block_age:.1f}s old — node may be lagging.")
    else:
        print("✅ Node block height is up-to-date.")

    elapsed = time.time() - start
    print(f"⏱️ Completed in {elapsed:.2f}s")

    # JSON Output
    if args.json:
        result = {
            "rpc": args.rpc,
            "chain_id": chain_id,
            "network_name": network_name,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "latest_block": block_number,
            "block_timestamp": datetime.utcfromtimestamp(timestamp).isoformat() + "Z",
            "average_latency_seconds": round(latency, 3),
            "block_age_seconds": round(block_age, 2),
            "elapsed_seconds": round(elapsed, 2),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0)

if __name__ == "__main__":
    main()
