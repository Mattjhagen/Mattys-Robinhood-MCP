#!/usr/bin/env python3
"""
MCP Bridge - Connect Python to Robinhood MCP (npm package)
Spawns npx robinhood-mcp and communicates via JSON-RPC stdio protocol
"""

import json
import subprocess
import threading
import queue
import time
import sys
from typing import Dict, List, Optional, Any

class MCPBridge:
    """
    Bridge to communicate with Robinhood MCP via stdio JSON-RPC
    """

    def __init__(self):
        self.process = None
        self.request_id = 0
        self.response_queue = {}
        self.reader_thread = None
        self.running = False

    def start(self):
        """Start the MCP process and reader thread"""
        if self.running:
            return

        try:
            # Spawn npx robinhood-mcp
            self.process = subprocess.Popen(
                ['npx', 'robinhood-mcp'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            self.running = True

            # Start reader thread
            self.reader_thread = threading.Thread(target=self._read_responses, daemon=True)
            self.reader_thread.start()

            # Give it a moment to initialize
            time.sleep(0.5)

            print("✅ MCP Bridge started")
            return True

        except Exception as e:
            print(f"❌ Failed to start MCP bridge: {e}")
            return False

    def _read_responses(self):
        """Background thread to read MCP responses"""
        while self.running and self.process:
            try:
                line = self.process.stdout.readline()
                if not line:
                    break

                # Parse JSON-RPC response
                try:
                    response = json.loads(line)
                    req_id = response.get('id')

                    if req_id is not None and req_id in self.response_queue:
                        self.response_queue[req_id].put(response)

                except json.JSONDecodeError:
                    # Ignore non-JSON lines (debug output, etc)
                    pass

            except Exception as e:
                if self.running:
                    print(f"Reader error: {e}", file=sys.stderr)
                break

    def _call_tool(self, tool_name: str, params: Dict = None) -> Dict:
        """
        Call an MCP tool and wait for response

        Args:
            tool_name: Name of the MCP tool
            params: Tool parameters

        Returns:
            Tool result or error dict
        """
        if not self.running:
            if not self.start():
                return {'error': 'MCP bridge not running'}

        # Generate request
        self.request_id += 1
        req_id = self.request_id

        request = {
            'jsonrpc': '2.0',
            'method': 'tools/call',
            'params': {
                'name': tool_name,
                'arguments': params or {}
            },
            'id': req_id
        }

        # Create response queue for this request
        self.response_queue[req_id] = queue.Queue()

        try:
            # Send request
            self.process.stdin.write(json.dumps(request) + '\n')
            self.process.stdin.flush()

            # Wait for response (10 second timeout)
            try:
                response = self.response_queue[req_id].get(timeout=10)

                # Clean up queue
                del self.response_queue[req_id]

                # Extract result
                if 'result' in response:
                    return response['result']
                elif 'error' in response:
                    return {'error': response['error']}
                else:
                    return response

            except queue.Empty:
                del self.response_queue[req_id]
                return {'error': 'MCP request timeout'}

        except Exception as e:
            if req_id in self.response_queue:
                del self.response_queue[req_id]
            return {'error': f'MCP call failed: {str(e)}'}

    def stop(self):
        """Stop the MCP process"""
        self.running = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                self.process.kill()
            self.process = None

        print("🛑 MCP Bridge stopped")

    # ============================================================================
    # ROBINHOOD API METHODS (matching RobinhoodAPI interface)
    # ============================================================================

    def get_account(self) -> Dict:
        """Get account information"""
        result = self._call_tool('get_account')

        if 'error' in result:
            return result

        # Extract account data from MCP response
        content = result.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '{}')
            return json.loads(text)

        return {'error': 'No account data'}

    def get_holdings(self) -> List[Dict]:
        """Get crypto holdings"""
        result = self._call_tool('get_holdings')

        if 'error' in result:
            return []

        # Extract holdings from MCP response
        content = result.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '[]')
            data = json.loads(text)
            return data.get('holdings', [])

        return []

    def get_best_bid_ask(self, symbols: List[str]) -> Dict:
        """Get quotes for symbols"""
        result = self._call_tool('get_best_bid_ask', {'symbols': symbols})

        if 'error' in result:
            return result

        content = result.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '{}')
            return json.loads(text)

        return {}

    def get_orders(self, limit: int = 10) -> List[Dict]:
        """Get order history"""
        result = self._call_tool('get_orders', {'limit': limit})

        if 'error' in result:
            return []

        content = result.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '[]')
            data = json.loads(text)
            return data.get('orders', [])

        return []

    def get_allocation(self) -> Dict:
        """Get portfolio allocation"""
        result = self._call_tool('get_allocation')

        if 'error' in result:
            return result

        content = result.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '{}')
            return json.loads(text)

        return {}

    def __del__(self):
        """Cleanup on destruction"""
        self.stop()


# Global singleton
_bridge_instance = None

def get_mcp_bridge() -> MCPBridge:
    """Get or create MCP bridge singleton"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MCPBridge()
    return _bridge_instance


if __name__ == '__main__':
    # Test the bridge
    print("🧪 Testing MCP Bridge")
    print("=" * 60)

    bridge = get_mcp_bridge()
    bridge.start()

    print("\n📊 Account:")
    account = bridge.get_account()
    print(json.dumps(account, indent=2))

    print("\n💰 Holdings:")
    holdings = bridge.get_holdings()
    print(json.dumps(holdings, indent=2))

    print("\n📈 BTC Quote:")
    quotes = bridge.get_best_bid_ask(['BTC-USD'])
    print(json.dumps(quotes, indent=2))

    print("\n🎯 Allocation:")
    allocation = bridge.get_allocation()
    print(json.dumps(allocation, indent=2))

    bridge.stop()
    print("\n✅ Bridge test complete")
