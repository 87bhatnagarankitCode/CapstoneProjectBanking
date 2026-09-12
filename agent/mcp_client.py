import asyncio
import sys
import os
import json

async def main():
    print("=" * 60)
    print(" SUCCESS: Connected to local FastMCP Server via Stdio Pipes.")
    print("=" * 60)
    
    server_script = os.path.join(os.path.dirname(__file__), "mcp_server.py")
    
    proc = await asyncio.create_subprocess_exec(
        sys.executable, server_script,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        while True:
            # एकदम साफ गाइडेंस मैसेज जो यूजर को सही फॉर्मेट (LNK-XXXX) समझाएगा
            user_input = input("\nEnter Loan ID (Format: LNK-XXXX) or type 'exit/quit' to quit: ").strip()
            
            if user_input.lower() == 'exit':
                print("Exiting Cred MCP Production Shell... Goodbye!")
                break
                
            
            target_ids = [user_input] if user_input else ["LNK-1001", "LNK-1002"]
        
            for idx, target_id in enumerate(target_ids, 1):
                payload = {
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": "check_loan_application_status",
                        "arguments": {"record_id": target_id}
                    },
                    "id": idx
                }
            
                proc.stdin.write(json.dumps(payload).encode() + b"\n")
                await proc.stdin.drain()
                
                response_line = await proc.stdout.readline()
                if response_line:
                    response = json.loads(response_line.decode().strip())
                    print(f"\n[FastMCP Client] Target Query: {target_id}")
                    print(f"[Official JSON-RPC Packet Output]:\n{json.dumps(response, indent=2)}")
    finally:
        proc.terminate()
        await proc.wait()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
