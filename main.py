import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

def compute_equations(csv_file):
    df = csv_file
    
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
    dL = 0.32            

    #-------------------------------------------------
    # Equation (1)
    # Q = (0.077 * (Hdiff * 10^(-2))) / t
    #-------------------------------------------------
    df["Q"] = (0.077 * (df["Hdiff"] * 1e-2)) / df["t"]

    #-------------------------------------------------
    # Equation (2)
    #   Vavg = (Q) / ((π/4) × D² × 10^(-6))
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
    # so effectively Re = (ρ × Vavg × D× 10^(-3)/μ.
    #-------------------------------------------------
    df["Re"] = (rho * df["Vavg"] * df["D"]*1e-3) / mu

    #-------------------------------------------------
    # Equation (4)
    #   Fexp = [ P_avg × D × 10^(-3) ] / [ 2 × dl x ρ × (Vavg)² ]
    #   (Here ρ = 1×10^3, from your notes)
    #-------------------------------------------------
    df["Fexp"] = (df["P_avg"] * df["D"] * 1e-3) / (2.0 * dL*rho * (df["Vavg"]**2))

    #-------------------------------------------------
    # Equation (5)
    #   X = 3.7 × 10^[ -0.25 / sqrt(Fexp)  - 1.255 / (Re * sqrt(Fexp)) ]
    #-------------------------------------------------
    exponent_part = (-0.25 / np.sqrt(df["Fexp"])) 


    df["X"] = (3.7 * (10 ** exponent_part)) - (
        1.255 / (df["Re"] * np.sqrt(df["Fexp"]))
    )
    
    df["E"] = df["X"] * (df["D"] * 1e-3)

    # Compute the average E for D = 9.6
    e_avg = df.loc[df["D"] == 9.6, "E"].mean()

    # Step 2: Replace E for all other D values with the average E
    df.loc[df["D"] != 9.6, "E"] = e_avg

    df.loc[df["D"] != 9.6, "X"] = e_avg / (df.loc[df["D"] != 9.6, "D"]*1e-3)

    #-------------------------------------------------
    # Equation (6)
    #   Ftheo = (-1.737 ln[ 0.269 X  -  (2.185 / Re) ln(0.269 X  + 14.5 / Re) ])^-2

    #-------------------------------------------------
    df["Ftheo"] = 1/(-1.737 * np.log(
        0.269 * df["X"]
        - (2.185 / df["Re"]) * np.log((0.269 * df["X"])
        + (14.5 / df["Re"]))
    ))**2

    #------------------------------------------------
    # Least Counts  
    dD = 1e-5
    dQ = 1e-6
    dl = 1e-3
    #-------------------------------------------------
    #Error Calcuclation
    df["dQ/Q"] = dQ/df["Q"]
    df["dRe/Re"] = np.sqrt( (df["dQ/Q"])**2 + (dD/df["D"])**2 ) *100
    df["dFe/Fe"] = np.sqrt( ((df["P_max"]-df["P_min"])*9.81/df["P_avg"])**2 + (dD/df["D"])**2 + (2*df["dQ/Q"])**2 + (dl/0.85)**2 ) *100
    
    #-------------------------------------------------
    return df

    
# Example usage:
if __name__ == "__main__":
    pipe3 = pd.read_csv("pipe123.csv")
    pipe3 = pipe3.loc[pipe3["D"]==9.6]
    bend = pd.read_csv("Long,Short - Sheet1.csv")
    bend = pd.concat([bend, pipe3], ignore_index=True)
    data = compute_equations(bend)
    data.to_csv("bends.csv", index=True)

    #data2 = pd.read_csv("pipe123.csv")
    #data_pipes = compute_equations(data2)
    #data_pipes.to_csv("output2.csv")