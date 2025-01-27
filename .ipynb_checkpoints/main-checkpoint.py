import pandas as pd
import numpy as np
import math

def compute_equations(csv_file):
    # Read CSV into a DataFrame
    csv_file = "data.csv"
    df = pd.read_csv(csv_file)
    
    #-------------------------------------------------
    # Assumed constants based on your notes:
    #
    #  ρ   = 1000  (f in your notes, the fluid density, 1×10^3)
    #  μ   = 1e-3  (the dynamic viscosity, 0.001)
    #  π   = math.pi
    #
    # Make sure that your CSV has columns named exactly:
    #   P_min, P_max, P_avg, Hi, Hf, Hdiff, t, D
    #   matching what you showed in your screenshot.
    #-------------------------------------------------

    rho = 1000.0         # fluid density
    mu  = 1e-3           # viscosity
    pi  = math.pi
    dl =1.0              

    #-------------------------------------------------
    # Equation (1)
    # Q = (0.077 * (Hdiff * 10^(-2))) / t
    #-------------------------------------------------
    df["Q"] = (0.077 * (df["Hdiff"] * 1e-2)) / df["t"]

    #-------------------------------------------------
    # Equation (2)
    #   Vavg = (4 × Q) / (π × D² × 10^(-6))
    #   Make sure to use π * (D^2) * 10^(-6)
    #-------------------------------------------------
    df["Vavg"] = ( df["Q"]) / ((pi /4.0)* (df["D"]**2) * 1e-6)
    print(pi)

    #-------------------------------------------------
    # Equation (3)
    #   Re = f × Vavg × D × 10^(-3) / 0.001
    #
    # In your notes it looks like f = 1000 kg/m³,
    # and μ (viscosity) = 0.001 Pa·s = 1e-3,
    # so effectively Re = (ρ × Vavg × D)/μ.
    #-------------------------------------------------
    df["Re"] = (rho * df["Vavg"] * df["D"]*1e-3) / mu

    #-------------------------------------------------
    # Equation (4)
    #   Fexp = [ P_avg × D × 10^(-3) ] / [ 2 × ρ × (Vavg)² ]
    #   (Here ρ = 1×10^3, from your notes)
    #-------------------------------------------------
    df["Fexp"] = (df["P_avg"] * df["D"] * 1e-3) / (2.0 * dl*rho * (df["Vavg"]**2))

    #-------------------------------------------------
    # Equation (5)
    #   X = 3.7 × 10^[ -0.25 / sqrt(Fexp)  - 1.255 / (Re * sqrt(Fexp)) ]
    #-------------------------------------------------
    exponent_part = (-0.25 / np.sqrt(df["Fexp"])) 


    df["X"] = (3.7 * (10 ** exponent_part)) - (
        1.255 / (df["Re"] * np.sqrt(df["Fexp"]))
    )

    #-------------------------------------------------
    # Equation (6)
    #   Ftheo = -1.737 ln[ 0.269 X  -  (2.185 / Re) ln(0.269 X  + 1.49 / Re) ]

    #-------------------------------------------------
    df["Ftheo"] = 1/(-1.737 * np.log(
        0.269 * df["X"]
        - (2.185 / df["Re"]) * np.log((0.269 * df["X"])
        + (14.5 / df["Re"]))
    ))**2

    # Print out the combined table:
    # Original columns + the new columns for Q, Vavg, Re, Fexp, X, Ftheo.
    print(df)

# Example usage:
if __name__ == "__main__":
    # Replace "data.csv" with the path to your actual CSV file
    compute_equations("csv_file.csv")
