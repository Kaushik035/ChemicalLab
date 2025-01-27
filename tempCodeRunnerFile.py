    # # Least Counts  
    # dD = 1e-6
    # dQ = 1e-5

    # #-------------------------------------------------
    # #Error Calcuclation
    # df["dRe/Re"] = np.sqrt( (dQ/df["Q"])**2 + (dD/df["D"])**2 )
    # df["dFe/Fe"] = np.sqrt( ((df["P_max"]-df["P_min"])*9.81/df["P_avg"])**2 + (dD/df["D"])**2 + (2*dQ/df["Q"])**2 + (dl/0.85)**2 )
    
    # # Print out the combined table:
    # # Original columns + the new columns for Q, Vavg, Re, Fexp, X, Ftheo.
    # return df
