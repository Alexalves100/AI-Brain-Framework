"""
Model Context Protocol (MCP) Server Implementation in Pure Python
Version: 1.0.0
"""

import json
import sys
from typing import Any, Dict, Optional, TextIO

from ..prompts.senior_prompts import SeniorPromptTemplates
from ..standards.senior_guidelines import SeniorGuidelines
from .protocol import JsonRpcError, JsonRpcMessage
from .tools import MCPToolRegistry


class MCPServer:
    """
    Native pure Python MCP Server implementing the official Model Context Protocol.
    Works seamlessly over stdio with Claude Desktop, Cursor, Windsurf, VS Code, and Roo Code.
    Zero external dependencies.
    """

    SERVER_NAME = "ai-brain-framework"
    SERVER_VERSION = "1.0.0"
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self):
        self.tool_registry = MCPToolRegistry()
        self.running = False

    def handle_message(self, message: JsonRpcMessage) -> Optional[JsonRpcMessage]:
        """Processes a single incoming JSON-RPC message."""
        method = message.method
        msg_id = message.msg_id
        params = message.params or {}

        if method == "initialize":
            return self._handle_initialize(msg_id, params)

        elif method == "notifications/initialized":
            # Client notification: no response needed
            return None

        elif method == "ping":
            return JsonRpcMessage.make_response(msg_id, {})

        elif method == "tools/list":
            return self._handle_tools_list(msg_id)

        elif method == "tools/call":
            return self._handle_tools_call(msg_id, params)

        elif method == "prompts/list":
            return self._handle_prompts_list(msg_id)

        elif method == "prompts/get":
            return self._handle_prompts_get(msg_id, params)

        elif method == "resources/list":
            return JsonRpcMessage.make_response(msg_id, {"resources": []})

        else:
            if message.is_notification:
                return None
            return JsonRpcMessage.make_error(
                msg_id=msg_id,
                code=JsonRpcError.METHOD_NOT_FOUND,
                message=f"Method not found: '{method}'",
            )

    def _handle_initialize(self, msg_id: Any, params: Dict[str, Any]) -> JsonRpcMessage:
        return JsonRpcMessage.make_response(
            msg_id=msg_id,
            result={
                "protocolVersion": self.PROTOCOL_VERSION,
                "serverInfo": {
                    "name": self.SERVER_NAME,
                    "version": self.SERVER_VERSION,
                },
                "capabilities": {
                    "tools": {},
                    "prompts": {},
                    "resources": {},
                },
            },
        )

    def _handle_tools_list(self, msg_id: Any) -> JsonRpcMessage:
        tools = self.tool_registry.get_tool_definitions()
        return JsonRpcMessage.make_response(msg_id=msg_id, result={"tools": tools})

    def _handle_tools_call(self, msg_id: Any, params: Dict[str, Any]) -> JsonRpcMessage:
        name = params.get("name")
        arguments = params.get("arguments", {})

        if not name:
            return JsonRpcMessage.make_error(
                msg_id=msg_id,
                code=JsonRpcError.INVALID_PARAMS,
                message="Missing tool name parameter",
            )

        try:
            output = self.tool_registry.execute_tool(name, arguments)
            # Format according to official MCP content blocks specification
            content_text = json.dumps(output, indent=2, ensure_ascii=False) if isinstance(output, (dict, list)) else str(output)
            return JsonRpcMessage.make_response(
                msg_id=msg_id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": content_text,
                        }
                    ],
                    "isError": False,
                },
            )
        except Exception as e:
            return JsonRpcMessage.make_response(
                msg_id=msg_id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error executing tool '{name}': {str(e)}",
                        }
                    ],
                    "isError": True,
                },
            )

    def _handle_prompts_list(self, msg_id: Any) -> JsonRpcMessage:
        prompts = [
            {
                "name": "senior_developer_system_prompt",
                "description": "Injects Senior Staff Engineer Clean Code guardrails (SOLID, Guard Clauses, Type Hints, Defensive Error Handling).",
                "arguments": [
                    {
                        "name": "role",
                        "description": "Optional engineering role title",
                        "required": False,
                    }
                ],
            },
            {
                "name": "feature_implementation_prompt",
                "description": "Generates structured Senior Engineer prompt for implementing a new feature with clean architecture.",
                "arguments": [
                    {
                        "name": "feature_description",
                        "description": "Description of the feature to build",
                        "required": True,
                    }
                ],
            },
        ]
        return JsonRpcMessage.make_response(msg_id=msg_id, result={"prompts": prompts})

    def _handle_prompts_get(self, msg_id: Any, params: Dict[str, Any]) -> JsonRpcMessage:
        name = params.get("name")
        arguments = params.get("arguments", {})

        if name == "senior_developer_system_prompt":
            role = arguments.get("role", "Principal Software Architect")
            content = SeniorGuidelines.get_system_prompt(role_title=role)
            return JsonRpcMessage.make_response(
                msg_id=msg_id,
                result={
                    "messages": [
                        {
                            "role": "user",
                            "content": {"type": "text", "text": content},
                        }
                    ]
                },
            )

        elif name == "feature_implementation_prompt":
            feature_desc = arguments.get("feature_description", "")
            content = SeniorPromptTemplates.get_feature_implementation_prompt(feature_desc)
            return JsonRpcMessage.make_response(
                msg_id=msg_id,
                result={
                    "messages": [
                        {
                            "role": "user",
                            "content": {"type": "text", "text": content},
                        }
                    ]
                },
            )

        return JsonRpcMessage.make_error(
            msg_id=msg_id,
            code=JsonRpcError.INVALID_PARAMS,
            message=f"Unknown prompt: '{name}'",
        )

    def run_stdio(self, in_stream: Optional[TextIO] = None, out_stream: Optional[TextIO] = None) -> None:
        """Starts listening for JSON-RPC messages on standard I/O."""
        in_s = in_stream or sys.stdin
        out_s = out_stream or sys.stdout
        self.running = True

        for line in in_s:
            if not self.running:
                break
            stripped = line.strip()
            if not stripped:
                continue

            try:
                msg = JsonRpcMessage.from_json(stripped)
                response = self.handle_message(msg)
                if response:
                    out_s.write(response.to_json() + "\n")
                    out_s.flush()
            except Exception as e:
                err_resp = JsonRpcMessage.make_error(
                    msg_id=None,
                    code=JsonRpcError.PARSE_ERROR,
                    message=f"Parse error: {str(e)}",
                )
                out_s.write(err_resp.to_json() + "\n")
                out_s.flush()
