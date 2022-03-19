"""
Created on Thu Mar 10 14:10:15 2022

@author: Dhruv Jain, Multi-Body Dynamics Research Group, Purdue University

Obj: To compute family of L4 Short Period Orbit
    Single Shooter Variabl Time Setup
    1. Continue in 'JC' + Periodicity (sym_period_targ=1)
    2. PALC + Periodicity (sym_period_targ=1) {Phase Constraint is added}

Initial Condition obtained from:
D. Grebow, "Generating Periodic Orbits in the Circular Restricted Three-Body Problem with Applications to Lunar South Pole Coverage," M.S., May 2006.
"""

import numpy as np
import plotly.graph_objs as go
from cr3bp_char_quant import bodies_char
from cr3bp_fam_continuation import npc_po_fam_cr3bp, palc_po_fam_cr3bp
from cr3bp_lib_JC_calc import lib_pt_loc
from cr3bp_plot_orbits import plot_orbits
from cr3bp_PO_targeter import po_single_shooter_cr3bp

mu, dist_e_m, tstar = bodies_char("Earth", "Moon")
lib_loc = lib_pt_loc(mu)
li = lib_loc[3, :]  # 0 for L1 and  1 for L2

# From D. Grebow
ig = np.array(
    [0.497653463566241, 0.866025403784439, 0, 0.006195078418070, -0.008234243375973, 0]
)
tf_guess = 6.582664326977796

orbit_results = []

free_vars = ["x", "y", "vx", "vy", "t"]
constraints = ["x", "y", "vx"]

# Target Axial orbit using Single Shooter Variable Time setup
#        Exploits Periodicity(sym_perioid_targ set to 1)
#        Continue in 'vy' using Natural Paramter Continuaton
targeted_po_fam, targeted_po_char = npc_po_fam_cr3bp(
    mu,
    po_single_shooter_cr3bp,
    ig,
    tf_guess,
    free_vars,
    constraints,
    sym_period_targ=1,
    JCd=None,
    step_size=1e-4,
    num_fam_members=2,
    param_continue="jc",
    line_search=True,
)

"""
PALC
"""

targeted_orbit = targeted_po_fam[-1]
targeted_po_fam_updated, targeted_po_char_updated = palc_po_fam_cr3bp(
    mu,
    po_single_shooter_cr3bp,
    targeted_orbit,
    free_vars,
    constraints,
    sym_period_targ=1,
    step_size=1e-1,
    num_fam_members=30,
    line_search=True,
)
targeted_po_fam.extend(targeted_po_fam_updated)
for keys in targeted_po_char_updated.keys():
    targeted_po_char[keys].extend(targeted_po_char_updated[keys])


"""
Plot family
"""
# if targeted_po_char != None:
colourby = targeted_po_char["jc"]
colourmap = "plasma"
cb_label = "JC"
title = "EM_L4_Short_Period_to_L3_lyapunov_family"
data_trace = []
# Add L4
for i in range(5):
    data_trace.append(
        go.Scatter3d(
            x=[lib_loc[i, 0]],
            y=[lib_loc[i, 1]],
            z=[0],
            marker=dict(color="red", size=2),
        )
    )
# Add Moon
data_trace.append(
    go.Scatter3d(x=[1 - mu], y=[0], z=[0], marker=dict(color="grey", size=7))
)
# Add Earth
data_trace.append(
    go.Scatter3d(x=[-mu], y=[0], z=[0], marker=dict(color="blue", size=10))
)


plot_orbits(
    mu,
    targeted_po_fam,
    colourby,
    cb_label,
    title=title,
    data_trace=data_trace,
    save=False,
)
