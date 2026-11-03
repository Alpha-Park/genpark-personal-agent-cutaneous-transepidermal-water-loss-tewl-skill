"""
Cutaneous Transepidermal Water Loss (TEWL) & Barrier Integrity Client.
Zero-mock pure Python standard library implementation.
Calculates water vapor flux based on Fick's first law of diffusion,
evaluates stratum corneum barrier integrity, chemical/environmental disruption, and recovery kinetics.
"""

import math
from typing import Dict, Any, List, Optional


class TransepidermalWaterLossClient:
    """
    Computes TEWL vapor flux (g / (m^2 * h)) from dual relative humidity and temperature sensor arrays
    or calibrated evaporimeter gradient probes.
    """

    def __init__(self, sensor_distance_mm: float = 4.0):
        if sensor_distance_mm <= 0:
            raise ValueError("Sensor distance must be positive.")
        self.sensor_distance_mm = sensor_distance_mm
        # Evaporimeter calibration constant in g / (m^2 * h * hPa) normalized to standard 4 mm chamber:
        self.diffusivity_constant = 0.670

    def _saturated_vapor_pressure_pa(self, temp_c: float) -> float:
        """
        Calculates saturated vapor pressure of water using the Magnus-Tetens approximation.
        P_sat (Pa) = 610.78 * exp((17.27 * T) / (T + 237.3))
        """
        return 610.78 * math.exp((17.27 * temp_c) / (temp_c + 237.3))

    def calculate_tewl(
        self,
        temp_surface_c: float,
        rh_surface_pct: float,
        temp_ambient_c: float,
        rh_ambient_pct: float,
        baseline_tewl: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates TEWL flux and barrier integrity status.
        temp_surface_c: Temperature near skin surface (deg C).
        rh_surface_pct: Relative humidity near skin surface (%).
        temp_ambient_c: Temperature at outer sensor port (deg C).
        rh_ambient_pct: Relative humidity at outer sensor port (%).
        baseline_tewl: Optional baseline TEWL for recovery index calculation.
        """
        if not (0 <= rh_surface_pct <= 100) or not (0 <= rh_ambient_pct <= 100):
            raise ValueError("Relative humidity must be between 0% and 100%.")

        p_sat_surface = self._saturated_vapor_pressure_pa(temp_surface_c)
        p_sat_ambient = self._saturated_vapor_pressure_pa(temp_ambient_c)

        # Actual partial vapor pressures in Pascals (Pa)
        vp_surface_pa = p_sat_surface * (rh_surface_pct / 100.0)
        vp_ambient_pa = p_sat_ambient * (rh_ambient_pct / 100.0)

        delta_vp_pa = max(0.0, vp_surface_pa - vp_ambient_pa)
        # Convert vapor pressure gradient to hectopascals (hPa / mbar) for standard evaporimeter flux
        delta_vp_hpa = delta_vp_pa / 100.0

        # TEWL Flux = Constant * (delta_VP_hpa / distance_factor)
        # Standard evaporimeter chamber normalized to 4 mm spacing
        distance_factor = self.sensor_distance_mm / 4.0
        tewl_flux = (self.diffusivity_constant * delta_vp_hpa) / distance_factor

        # Clinical barrier classification:
        # Normal healthy stratum corneum: TEWL 4.0 - 10.0 g/(m^2 * h)
        # Mild dryness / slight compromise: 10.0 - 18.0 g/(m^2 * h)
        # Moderate barrier impairment (mild eczema / solvent disruption): 18.0 - 30.0 g/(m^2 * h)
        # Severe barrier breakdown (acute dermatitis, tape-stripped): > 30.0 g/(m^2 * h)
        if tewl_flux < 10.0:
            barrier_score = 95.0 - (tewl_flux * 2.0)
            status = "Intact Stratum Corneum Barrier"
            recommendation = "Optimal lipid matrix and natural moisturizing factor (NMF) retention."
        elif tewl_flux < 18.0:
            barrier_score = 75.0 - ((tewl_flux - 10.0) * 2.5)
            status = "Mild Epidermal Micro-Barrier Compromise"
            recommendation = "Subclinical lipid depletion; application of ceramide-rich emollient recommended."
        elif tewl_flux < 30.0:
            barrier_score = 55.0 - ((tewl_flux - 18.0) * 2.0)
            status = "Moderate Barrier Disruption / Hyper-Permeability"
            recommendation = "Impaired hydrophobic barrier. Avoid surfactants; replenish occlusives and physiologic lipids."
        else:
            barrier_score = max(5.0, 30.0 - ((tewl_flux - 30.0) * 0.8))
            status = "Severe Stratum Corneum Barrier Failure"
            recommendation = "Critical transepidermal evaporative loss. Protect with dense occlusive ointment; evaluate for contact dermatitis."

        recovery_ratio = None
        if baseline_tewl is not None and baseline_tewl > 0:
            # Ratio relative to undisturbed baseline
            recovery_ratio = round(tewl_flux / baseline_tewl, 2)

        return {
            "status": "success",
            "tewl_flux_g_m2_h": round(tewl_flux, 2),
            "delta_vapor_pressure_hpa": round(delta_vp_hpa, 2),
            "surface_vapor_pressure_pa": round(vp_surface_pa, 1),
            "ambient_vapor_pressure_pa": round(vp_ambient_pa, 1),
            "barrier_integrity_score": round(barrier_score, 1),
            "baseline_ratio": recovery_ratio,
            "evaluation": {
                "status": status,
                "recommendation": recommendation,
                "sensor_distance_mm": self.sensor_distance_mm
            }
        }
