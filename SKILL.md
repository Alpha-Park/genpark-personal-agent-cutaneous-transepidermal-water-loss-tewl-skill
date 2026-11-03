---
name: genpark-personal-agent-cutaneous-transepidermal-water-loss-tewl-skill
description: Transepidermal Water Loss (TEWL) and stratum corneum diffusion gradient analyzer based on Fick's first law of diffusion. Quantifies epidermal barrier integrity, irritant disruption, and hydration recovery kinetics.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - dermatology
  - skin-barrier
  - tewl
  - biophysics
  - openclaw
  - genpark
  - mcp
---

# Cutaneous Transepidermal Water Loss (TEWL) Skill

## Overview
This skill computes cutaneous water vapor flux ($g / (m^2 \cdot h)$) diffusing passively through the stratum corneum:
- **Diffusion Gradient**: Calculated from differential water vapor pressures measured across an open chamber or dual-sensor evaporimeter.
- **Barrier Integrity Evaluation**: Categorizes the barrier from healthy intact lipids ($<10.0\text{ g}/(m^2\cdot h)$) to severe disruption ($>30.0\text{ g}/(m^2\cdot h)$).
- **Perturbation & Recovery Kinetics**: Tracks recovery ratios post-cleansing, surfactant challenge, or environmental exposure.

## Mathematical Formulation
1. **Saturated Vapor Pressure ($P_{\text{sat}}$, Pa)**:
   $$P_{\text{sat}}(T) = 610.78 \exp\left(\frac{17.27 \times T}{T + 237.3}\right)$$
2. **Partial Vapor Pressure**:
   $$VP = P_{\text{sat}}(T) \times \frac{\text{RH}}{100}$$
3. **Fick's Diffusion Flux (TEWL)**:
   $$\text{TEWL} = D \times \frac{\Delta VP}{\Delta z}$$

## Usage
```python
from client import TransepidermalWaterLossClient

client = TransepidermalWaterLossClient()
res = client.calculate_tewl(
    temp_surface_c=32.0,
    rh_surface_pct=45.0,
    temp_ambient_c=22.0,
    rh_ambient_pct=35.0
)
print(res["evaluation"]["status"])
```
