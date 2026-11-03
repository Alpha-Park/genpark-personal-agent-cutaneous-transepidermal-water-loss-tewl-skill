# Cutaneous Transepidermal Water Loss (TEWL) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Cutaneous Transepidermal Water Loss (TEWL) and Stratum Corneum Barrier Integrity Analyzer based on Fick's first law of diffusion.

```mermaid
flowchart TD
    A[Dual Temp & RH Sensors: Surface & Ambient] --> B[Magnus-Tetens Saturation Pressures]
    B --> C[Compute Partial Vapor Pressure Gradient]
    C --> D[Fickian Vapor Flux: TEWL in g/m2/h]
    D --> E[Stratum Corneum Barrier Integrity Score]
    E --> F[Clinical & Cosmetic Barrier Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Physical Diffusion Laws**: Magnus-Tetens formula and Fick's first law of steady-state diffusion.
- **Micro-Climate Sensitivity**: Compensates for sensor geometry and ambient conditions.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
