"""
JSON-RPC 2.0 Protocol and Message Framing for MCP
Version: 1.0.0
"""

import json
from typing import Any, Dict, Optional, Union


class JsonRpcError:
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


class JsonRpcMessage:
    """Represents a JSON-RPC 2.0 message."""

    def __init__(
        self,
        method: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        msg_id: Optional[Union[str, int]] = None,
        result: Optional[Any] = None,
        error: Optional[Dict[str, Any]] = None,
    ):
        self.method = method
        self.params = params or {}
        self.msg_id = msg_id
        self.result = result
        self.error = error

    @property
    def is_request(self) -> bool:
        return self.method is not None and self.msg_id is not None

    @property
    def is_notification(self) -> bool:
        return self.method is not None and self.msg_id is None

    @property
    def is_response(self) -> bool:
        return self.msg_id is not None and (self.result is not None or self.error is not None)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"jsonrpc": "2.0"}
        if self.msg_id is not None:
            data["id"] = self.msg_id

        if self.method is not None:
            data["method"] = self.method
            if self.params:
                data["params"] = self.params

        if self.result is not None:
            data["result"] = self.result
        elif self.error is not None:
            data["error"] = self.error

        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def make_response(cls, msg_id: Optional[Union[str, int]], result: Any) -> "JsonRpcMessage":
        return cls(msg_id=msg_id, result=result)


    @classmethod
    def make_error(
        cls,
        msg_id: Optional[Union[str, int]],
        code: int,
        message: str,
        data: Optional[Any] = None,
    ) -> "JsonRpcMessage":
        err_dict: Dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            err_dict["data"] = data
        return cls(msg_id=msg_id, error=err_dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JsonRpcMessage":
        return cls(
            method=data.get("method"),
            params=data.get("params"),
            msg_id=data.get("id"),
            result=data.get("result"),
            error=data.get("error"),
        )

    @classmethod
    def from_json(cls, raw_json: str) -> "JsonRpcMessage":
        data = json.loads(raw_json)
        if not isinstance(data, dict) or data.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC 2.0 payload")
        return cls.from_dict(data)
