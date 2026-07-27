"""
WebSocket Example
Version: 1.0.0
Minimal WebSocket server using only Python stdlib with AI-Brain-Framework.
Demonstrates: handshake, frame parsing, text/binary frames, ping/pong, close.
"""

import base64
import hashlib
import json
import socket
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from framework import create_default_orchestrator, Context, InputValidator


GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def handshake(reader, writer, path):
    """Perform WebSocket server handshake."""
    lines = []
    while True:
        line = reader.readline().decode("utf-8").strip()
        if not line:
            break
        lines.append(line)

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    key = headers.get("sec-websocket-key", "")
    if not key:
        return False

    accept = base64.b64encode(
        hashlib.sha1((key + GUID).encode()).digest()
    ).decode()
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
    )
    writer.write(response.encode())
    writer.flush()
    return True


def encode_frame(payload: bytes, opcode=0x1):
    """Encode a WebSocket frame (text by default)."""
    header = bytes([0x80 | opcode])
    length = len(payload)
    if length < 126:
        header += bytes([length])
    elif length < 65536:
        header += bytes([126]) + struct.pack(">H", length)
    else:
        header += bytes([127]) + struct.pack(">Q", length)
    return header + payload


def decode_frame(data):
    """Decode a single WebSocket frame from bytes."""
    if len(data) < 2:
        return None, b""
    fin = data[0] & 0x80
    opcode = data[0] & 0x0F
    masked = data[1] & 0x80
    length = data[1] & 0x7F

    offset = 2
    if length == 126:
        if len(data) < offset + 2:
            return None, data
        length = struct.unpack(">H", data[offset:offset+2])[0]
        offset += 2
    elif length == 127:
        if len(data) < offset + 8:
            return None, data
        length = struct.unpack(">Q", data[offset:offset+8])[0]
        offset += 8

    if masked:
        if len(data) < offset + 4:
            return None, data
        mask = data[offset:offset+4]
        offset += 4

    if len(data) < offset + length:
        return None, data

    payload = data[offset:offset+length]
    if masked:
        payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))

    return (fin, opcode, payload), data[offset+length:]


def handle_client(conn, addr, orchestrator):
    """Handle a single WebSocket client."""
    reader = conn.makefile("rb")
    writer = conn.makefile("wb")
    path = reader.readline().decode("utf-8").strip().split(" ")[1] if True else "/"

    if not handshake(reader, writer, path):
        conn.close()
        return

    print(f"[+] Client connected: {addr}")
    conn.settimeout(60)

    buffer = b""
    try:
        while True:
            try:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buffer += chunk
            except socket.timeout:
                writer.write(encode_frame(b"", opcode=0x9))
                writer.flush()
                continue

            while buffer:
                frame, buffer = decode_frame(buffer)
                if frame is None:
                    break

                _, opcode, payload = frame
                if opcode == 0x8:
                    writer.write(encode_frame(b"", opcode=0x8))
                    writer.flush()
                    return
                if opcode == 0x9:
                    writer.write(encode_frame(payload, opcode=0xA))
                    writer.flush()
                    continue
                if opcode in (0x1, 0x2):
                    msg = payload.decode("utf-8", errors="ignore")
                    try:
                        data = json.loads(msg)
                    except Exception:
                        data = {"raw": msg}

                    user_msg = (data.get("message") or "") if isinstance(data, dict) else ""
                    if not InputValidator.length(user_msg, 1, 1000):
                        writer.write(encode_frame(
                            json.dumps({"error": "invalid message"}).encode()
                        ))
                        writer.flush()
                        continue

                    ctx = Context()
                    ctx.set("query", user_msg)
                    ctx.set("code", user_msg)
                    results = orchestrator.run_pipeline(
                        ["brain", "security", "token_economy"], ctx
                    )

                    response = {
                        "received": user_msg,
                        "results": [
                            {
                                "engine": r.metadata.get("engine", r.status.value),
                                "status": r.status.value,
                                "output": r.output,
                            }
                            for r in results
                        ],
                    }
                    writer.write(encode_frame(
                        json.dumps(response, ensure_ascii=False).encode()
                    ))
                    writer.flush()
    finally:
        print(f"[-] Client disconnected: {addr}")
        conn.close()


def main():
    orchestrator = create_default_orchestrator()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 8002))
    server.listen(5)
    print("WebSocket demo running on ws://127.0.0.1:8002")
    try:
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr, orchestrator)
    except KeyboardInterrupt:
        print("\nStopping.")


if __name__ == "__main__":
    main()
