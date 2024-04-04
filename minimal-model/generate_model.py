import cobra

# Make a new model
model = cobra.Model("segre_minimal_model")

# Create internal (c compartment) metabolites
glc = cobra.Metabolite("GLC", name="GLC", compartment="c")
pyr = cobra.Metabolite("PYR", name="PYR", compartment="c")
co2 = cobra.Metabolite("CO2", name="CO2", compartment="c")
o2 = cobra.Metabolite("O2", name="O2", compartment="c")
atp = cobra.Metabolite("ATP", name="ATP", compartment="c")
adp = cobra.Metabolite("ADP", name="ADP", compartment="c")
met_a = cobra.Metabolite("A", name="A", compartment="c")
met_b = cobra.Metabolite("B", name="B", compartment="c")
met_biomass = cobra.Metabolite("BIOMASS", name="BIOMASS", compartment="c")

# Create external metabolites (e compartment)
glc_e = cobra.Metabolite("GLC_e", name="GLC_e", compartment="e")
pyr_e = cobra.Metabolite("PYR_e", name="PYR_e", compartment="e")
co2_e = cobra.Metabolite("CO2_e", name="CO2_e", compartment="e")
o2_e = cobra.Metabolite("O2_e", name="O2_e", compartment="e")
met_a_e = cobra.Metabolite("A_e", name="A_e", compartment="e")
met_b_e = cobra.Metabolite("B_e", name="B_e", compartment="e")

# Add metabolites to model
model.add_metabolites(
    [
        glc,
        glc_e,
        pyr,
        pyr_e,
        co2,
        co2_e,
        o2,
        o2_e,
        atp,
        adp,
        met_a,
        met_a_e,
        met_b,
        met_b_e,
        met_biomass,
    ]
)

# Add boundary reactions
# TODO: Constrain uptakes
model.add_boundary(glc_e, type="exchange", reaction_id="EX_GLC", lb=-10, ub=1000)
model.add_boundary(pyr_e, type="exchange", reaction_id="EX_PYR", lb=0, ub=1000)
model.add_boundary(o2_e, type="exchange", reaction_id="EX_O2", lb=-1000, ub=1000)
model.add_boundary(co2_e, type="exchange", reaction_id="EX_CO2", lb=-0, ub=1000)
model.add_boundary(met_a_e, type="exchange", reaction_id="EX_A", lb=0, ub=1000)
model.add_boundary(met_b_e, type="exchange", reaction_id="EX_B", lb=0, ub=1000)
model.add_boundary(met_biomass, type="demand", reaction_id="EX_BIOMASS", lb=0, ub=1000)

# Create internal reactions
# Glucose transport
v_glc = cobra.Reaction("V_GLC", name="GLC uptake", lower_bound=0, upper_bound=1000)
v_glc.add_metabolites({glc_e: -1, glc: 1})

# Pyruvate transport
v_pyr = cobra.Reaction("V_PYR", name="PYR release", lower_bound=0, upper_bound=1000)
v_pyr.add_metabolites({pyr: -1, pyr_e: 1})

# Oxygen transport
v_o2 = cobra.Reaction("V_O2", name="O2 uptake", lower_bound=0, upper_bound=1000)
v_o2.add_metabolites({o2_e: -1, o2: 1})

# Carbon dioxide transport
v_co2 = cobra.Reaction("V_CO2", name="CO2 release", lower_bound=0, upper_bound=1000)
v_co2.add_metabolites({co2: -1, co2_e: 1})

# Metabolite A transport
v_a = cobra.Reaction("V_A", name="A release", lower_bound=0, upper_bound=1000)
v_a.add_metabolites({met_a: -1, met_a_e: 1})

# Metabolite B transport
v_b = cobra.Reaction("V_B", name="B release", lower_bound=0, upper_bound=1000)
v_b.add_metabolites({met_b: -1, met_b_e: 1})

# V1 (GLC --> A)
v1 = cobra.Reaction("V_GLC-to-A", name="GLC to A", lower_bound=0, upper_bound=1000)
v1.add_metabolites({glc: -1, met_a: 1, atp: -3, adp: 3})

# V2 (GLC --> PYR)
v2 = cobra.Reaction("V_GLC-to-PYR", name="GLC to PYR", lower_bound=0, upper_bound=1000)
v2.add_metabolites({glc: -1, pyr: 2, atp: 2, adp: -2})

# V3 (PYR --> CO2)
v3 = cobra.Reaction("V_PYR-to-CO2", name="PYR to CO2", lower_bound=0, upper_bound=1000)
v3.add_metabolites({pyr: -1, co2: 3, adp: -10, atp: 10, o2: -1})

# V4 (PYR --> B)
v4 = cobra.Reaction("V_PYR-to-B", name="PYR to B", lower_bound=0, upper_bound=1000)
v4.add_metabolites({pyr: -1, met_b: 1, atp: -6, adp: 6})

# Vm (ATP Maintenance)
vm = cobra.Reaction("V_m", name="ATP Maintenance", lower_bound=1, upper_bound=1000)
vm.add_metabolites({atp: -1, adp: 1})

# Vgro (Growth)
vgro = cobra.Reaction("V_BIOMASS", name="Growth", lower_bound=-1000, upper_bound=1000)
vgro.add_metabolites({met_a: -1, met_b: -1, met_biomass: 1})

# Add reactions to model
model.add_reactions([v_glc, v_pyr, v_o2, v_co2, v_a, v_b, v1, v2, v3, v4, vm, vgro])

# Set the objective
model.objective = vgro

# Save model
cobra.io.write_sbml_model(model, "minimal-model/segre_minimal_model.xml")
cobra.io.save_json_model(model, "minimal-model/segre_minimal_model.json")
