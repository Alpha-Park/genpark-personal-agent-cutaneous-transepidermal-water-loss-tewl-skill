"""
Example usage of Cutaneous Transepidermal Water Loss (TEWL) Skill.
Demonstrates normal skin barrier vs severe detergent disruption and recovery kinetics.
"""

import json
from client import TransepidermalWaterLossClient


def main():
    print("=== Testing Cutaneous Transepidermal Water Loss (TEWL) Skill ===")
    client = TransepidermalWaterLossClient(sensor_distance_mm=4.0)

    # 1. Healthy intact skin (Skin temp=32.0 C, RH=45%; Ambient temp=22.0 C, RH=35%)
    res_intact = client.calculate_tewl(
        temp_surface_c=32.0,
        rh_surface_pct=45.0,
        temp_ambient_c=22.0,
        rh_ambient_pct=35.0,
        baseline_tewl=None
    )
    print("\n[Case 1: Healthy Intact Epidermal Barrier]")
    print(json.dumps(res_intact, indent=2))

    # 2. Detergent-stripped / impaired stratum corneum (elevated humidity gradient)
    res_disrupted = client.calculate_tewl(
        temp_surface_c=33.5,
        rh_surface_pct=85.0,
        temp_ambient_c=22.0,
        rh_ambient_pct=30.0,
        baseline_tewl=res_intact["tewl_flux_g_m2_h"]
    )
    print("\n[Case 2: Compromised Barrier / Acute Disruption]")
    print(json.dumps(res_disrupted, indent=2))

    # Assertions
    assert res_intact["status"] == "success"
    assert res_disrupted["status"] == "success"
    assert res_disrupted["tewl_flux_g_m2_h"] > res_intact["tewl_flux_g_m2_h"]
    assert res_disrupted["barrier_integrity_score"] < res_intact["barrier_integrity_score"]
    print("\n[SUCCESS] All Cutaneous TEWL test cases passed!")


if __name__ == "__main__":
    main()
