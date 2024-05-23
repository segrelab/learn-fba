import cobra

# Make a new model
model = cobra.Model("three_reaction_model")

# Create internal (c compartment) metabolites
c_met = cobra.Metabolite("C_c", name="C", compartment="c")
n_met = cobra.Metabolite("N_c", name="N", compartment="c")
biomass_met = cobra.Metabolite("BIOMASS", name="BIOMASS", compartment="c")

# Create external metabolites (e compartment)
c_met_e = cobra.Metabolite("C_e", name="C_e", compartment="e")
n_met_e = cobra.Metabolite("N_e", name="N_e", compartment="e")

# Add metabolites to model
model.add_metabolites(
    [
        c_met,
        c_met_e,
        n_met,
        n_met_e,
        biomass_met,
    ]
)

# Add boundary reactions
model.add_boundary(c_met_e, type="exchange", reaction_id="EX_C", lb=-10, ub=0)
model.add_boundary(n_met_e, type="exchange", reaction_id="EX_N", lb=-1000, ub=1000)
model.add_boundary(biomass_met, type="demand", reaction_id="EX_BIOMASS", lb=0, ub=1000)

# Create internal reactions
# Glucose transport
v_c = cobra.Reaction("V_C", name="C uptake", lower_bound=0, upper_bound=10)
v_c.add_metabolites({c_met_e: -1, c_met: 1})

# Nitrogen transport
v_n = cobra.Reaction("V_N", name="N uptake", lower_bound=0, upper_bound=1000)
v_n.add_metabolites({n_met_e: -1, n_met: 1})

# Biomass production
v_biomass = cobra.Reaction("V_BIOMASS", name="Biomass production", lower_bound=0, upper_bound=1000)
v_biomass.add_metabolites({c_met: -10, n_met: -1, biomass_met: 1})

# Add reactions to model
model.add_reactions([v_c, v_n, v_biomass])

# Set the objective
model.objective = v_biomass

# Save model
cobra.io.write_sbml_model(model, "3rxn-model/3rxn-model.xml")
cobra.io.save_json_model(model, "3rxn-model/3rxn-model.json")
