"""
MCP Server for Cutaneous Transepidermal Water Loss (TEWL) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import TransepidermalWaterLossClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cutaneous-transepidermal-water-loss-tewl-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_tewl",
                        "description": "Calculate Transepidermal Water Loss (TEWL) flux and evaluate epidermal barrier integrity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "temp_surface_c": {"type": "number", "description": "Skin surface temperature in deg C."},
                                "rh_surface_pct": {"type": "number", "description": "Skin surface relative humidity (%)."},
                                "temp_ambient_c": {"type": "number", "description": "Ambient temperature in deg C."},
                                "rh_ambient_pct": {"type": "number", "description": "Ambient relative humidity (%)."},
                                "sensor_distance_mm": {"type": "number", "description": "Distance between sensor ports in mm (default: 4.0)."},
                                "baseline_tewl": {"type": "number", "description": "Optional baseline TEWL for recovery comparison."}
                            },
                            "required": [
                                "temp_surface_c",
                                "rh_surface_pct",
                                "temp_ambient_c",
                                "rh_ambient_pct"
                            ]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_tewl":
            sensor_distance_mm = float(args.get("sensor_distance_mm", 4.0))
            client = TransepidermalWaterLossClient(sensor_distance_mm=sensor_distance_mm)
            try:
                res = client.calculate_tewl(
                    temp_surface_c=float(args["temp_surface_c"]),
                    rh_surface_pct=float(args["rh_surface_pct"]),
                    temp_ambient_c=float(args["temp_ambient_c"]),
                    rh_ambient_pct=float(args["rh_ambient_pct"]),
                    baseline_tewl=float(args["baseline_tewl"]) if "baseline_tewl" in args and args["baseline_tewl"] is not None else None
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
