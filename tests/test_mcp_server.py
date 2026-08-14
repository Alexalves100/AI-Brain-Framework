"""
Unit Tests for Built-in MCP Server and Protocol
Version: 1.0.0
"""

import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.mcp import JsonRpcError, JsonRpcMessage, MCPServer, MCPToolRegistry

SAMPLE_CODE = '''
class AuthService:
    def login(self, username: str, password_hash: str) -> bool:
        if not username:
            return False
        return True
'''


class TestJsonRpcProtocol(unittest.TestCase):
    def test_message_creation_and_json(self):
        msg = JsonRpcMessage(method="ping", msg_id=1)
        self.assertTrue(msg.is_request)
        self.assertFalse(msg.is_notification)
        self.assertFalse(msg.is_response)

        raw = msg.to_json()
        parsed = JsonRpcMessage.from_json(raw)
        self.assertEqual(parsed.method, "ping")
        self.assertEqual(parsed.msg_id, 1)

    def test_response_and_error(self):
        resp = JsonRpcMessage.make_response(msg_id=42, result={"status": "ok"})
        self.assertTrue(resp.is_response)
        self.assertEqual(resp.result["status"], "ok")

        err = JsonRpcMessage.make_error(
            msg_id=42,
            code=JsonRpcError.METHOD_NOT_FOUND,
            message="Method not found",
        )
        self.assertTrue(err.is_response)
        self.assertEqual(err.error["code"], -32601)

    def test_invalid_json_rpc(self):
        with self.assertRaises(ValueError):
            JsonRpcMessage.from_json('{"foo": "bar"}')


class TestMCPToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = MCPToolRegistry()

    def test_get_tool_definitions(self):
        defs = self.registry.get_tool_definitions()
        self.assertIsInstance(defs, list)
        names = [d["name"] for d in defs]
        self.assertIn("clean_code_audit", names)
        self.assertIn("get_symbols_overview", names)
        self.assertIn("get_symbol_body", names)
        self.assertIn("security_scan", names)
        self.assertIn("compress_tokens", names)
        self.assertIn("analyze_complexity", names)
        self.assertIn("list_symbols", names)

    def test_execute_clean_code_audit(self):
        res = self.registry.execute_tool("clean_code_audit", {"code": SAMPLE_CODE})
        self.assertIn("score", res)
        self.assertGreaterEqual(res["score"], 80)


    def test_execute_get_symbols_overview(self):
        res = self.registry.execute_tool("get_symbols_overview", {"code": SAMPLE_CODE})
        self.assertIn("skeleton", res)
        self.assertIn("class AuthService:", res["skeleton"])

    def test_execute_get_symbol_body(self):
        res = self.registry.execute_tool(
            "get_symbol_body",
            {"code": SAMPLE_CODE, "symbol_name": "AuthService.login"},
        )
        self.assertTrue(res["found"])
        self.assertIn("def login", res["body"])

    def test_execute_security_scan(self):
        vulnerable_code = "query = 'SELECT * FROM users WHERE id = ' + user_id"
        res = self.registry.execute_tool("security_scan", {"code": vulnerable_code})
        self.assertIn("findings", res)

    def test_execute_compress_tokens(self):
        res = self.registry.execute_tool("compress_tokens", {"text": SAMPLE_CODE, "mode": "ast_skeleton"})
        self.assertIn("compressed_len", res)

    def test_execute_analyze_complexity(self):
        res = self.registry.execute_tool("analyze_complexity", {"code": SAMPLE_CODE})
        self.assertIn("cyclomatic_complexity", res)
        self.assertIn("cognitive_complexity", res)

    def test_execute_unknown_tool(self):
        with self.assertRaises(ValueError):
            self.registry.execute_tool("non_existent_tool", {})


class TestMCPServer(unittest.TestCase):
    def setUp(self):
        self.server = MCPServer()

    def test_initialize_handshake(self):
        msg = JsonRpcMessage(
            method="initialize",
            params={"protocolVersion": "2024-11-05", "clientInfo": {"name": "cursor"}},
            msg_id=1,
        )
        resp = self.server.handle_message(msg)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.msg_id, 1)
        self.assertEqual(resp.result["serverInfo"]["name"], "ai-brain-framework")
        self.assertIn("tools", resp.result["capabilities"])

    def test_ping(self):
        msg = JsonRpcMessage(method="ping", msg_id=2)
        resp = self.server.handle_message(msg)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.msg_id, 2)
        self.assertEqual(resp.result, {})

    def test_tools_list(self):
        msg = JsonRpcMessage(method="tools/list", msg_id=3)
        resp = self.server.handle_message(msg)
        self.assertIsNotNone(resp)
        self.assertIn("tools", resp.result)
        self.assertTrue(len(resp.result["tools"]) >= 7)

    def test_tools_call(self):
        msg = JsonRpcMessage(
            method="tools/call",
            params={
                "name": "get_symbols_overview",
                "arguments": {"code": SAMPLE_CODE},
            },
            msg_id=4,
        )
        resp = self.server.handle_message(msg)
        self.assertIsNotNone(resp)
        self.assertFalse(resp.result["isError"])
        self.assertIsInstance(resp.result["content"], list)
        self.assertEqual(resp.result["content"][0]["type"], "text")

    def test_prompts_list_and_get(self):
        # List
        msg_list = JsonRpcMessage(method="prompts/list", msg_id=5)
        resp_list = self.server.handle_message(msg_list)
        self.assertIn("prompts", resp_list.result)

        # Get
        msg_get = JsonRpcMessage(
            method="prompts/get",
            params={"name": "senior_developer_system_prompt", "arguments": {"role": "Staff Engineer"}},
            msg_id=6,
        )
        resp_get = self.server.handle_message(msg_get)
        self.assertIn("messages", resp_get.result)
        self.assertIn("Staff Engineer", resp_get.result["messages"][0]["content"]["text"])

    def test_unknown_method(self):
        msg = JsonRpcMessage(method="unknown/endpoint", msg_id=7)
        resp = self.server.handle_message(msg)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.error["code"], JsonRpcError.METHOD_NOT_FOUND)

    def test_run_stdio_stream(self):
        input_data = (
            json.dumps({"jsonrpc": "2.0", "id": 10, "method": "ping"}) + "\n"
            + json.dumps({"jsonrpc": "2.0", "id": 11, "method": "tools/list"}) + "\n"
        )
        in_stream = io.StringIO(input_data)
        out_stream = io.StringIO()

        self.server.run_stdio(in_stream=in_stream, out_stream=out_stream)

        output_lines = out_stream.getvalue().strip().splitlines()
        self.assertEqual(len(output_lines), 2)

        resp1 = json.loads(output_lines[0])
        self.assertEqual(resp1["id"], 10)
        self.assertEqual(resp1["result"], {})

        resp2 = json.loads(output_lines[1])
        self.assertEqual(resp2["id"], 11)
        self.assertIn("tools", resp2["result"])


if __name__ == "__main__":
    unittest.main()
