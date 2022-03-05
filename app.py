import streamlit as st

from src.story import STORY
import src.logic as lg
from src.simulation import Simulation
from src.simulation_unknown_best import Simulation_unknown_best
import pandas as pd

st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png")


# SIDEBAR
# No sidebar to begin. We fix the parameters first, then provide a sandbox later.


# MAIN PAGE
st.title("The Allegory of the Avocados (Working Title)")
st.write("""
Here is the link to our 
[Google Doc](https://docs.google.com/document/d/1CA9NXp8I9b6ds16khcJLrY1ZL7ZBABK6KRu9SvBL5JI/edit?usp=sharing) 
where we're developing and commenting on the story.""")


st.subheader("Welcome to [Town Name]")
for paragraph in STORY["introduction"]:
    st.write(paragraph)


st.subheader("Let’s Play Guac God")
for paragraph in STORY["Guac God"]:
    st.write(paragraph)

st.text("Objectively, how do the guacs measure up, relative to each other?")
guac_df = lg.objective_ratings()


st.subheader("1. Everybody Tries all the Guacs")
num_townspeople, st_dev = lg.simulation_parameters()
sim1 = Simulation(guac_df, num_townspeople, st_dev)
# start = st.button("Simulate")
# if start:
sim1.simulate()

# if sim.results_df is not None:
st.text("Let's see what the townspeople thought!")
chosen_method = lg.tally_votes(sim1, key="sim1")
lg.declare_a_winner(sim1, chosen_method)


st.markdown("---")
st.subheader("2. Not enough guac to go around")
# num_townspeople, st_dev = lg.simulation_parameters()
guac_limit = st.slider("How many guacs do we limit people to?",
    value=3, min_value=1, max_value=20)
sim2 = Simulation(guac_df, num_townspeople, st_dev, limit=guac_limit)
sim2.simulate()
st.text("Let's see what the townspeople thought!")
chosen_method = lg.tally_votes(sim2, key="sim2")
lg.declare_a_winner(sim2, chosen_method)



# st.subheader("A Fair Voting Process")
# for paragraph in STORY["Voting"]:
#     st.write(paragraph)


st.markdown("---")
st.subheader("3. Different Types of Voters")
# for paragraph in STORY["Voter Types"]:
#     st.write(paragraph)

perc_pepe, perc_fra, _ = lg.types_of_voters()
print(perc_pepe, perc_fra)
sim3 = Simulation(guac_df, num_townspeople, st_dev, limit=guac_limit, perc_pepe=perc_pepe, perc_fra=perc_fra)
sim3.simulate()
chosen_method = lg.tally_votes(sim3, key="sim3")
lg.declare_a_winner(sim3, chosen_method)



## FRA WIP BELOW
num_guacs = 20
# Allow abstinence?
st.subheader("What if We Don't Know Whose Guac is Best?")
for paragraph in STORY["Unknown Best"]:
    st.write(paragraph)



st.subheader("1. Everybody Tries all the Guacs, Everyone is Fair, All Guacs are Relatively Good")
num_townspeople = lg.num_people_slider()
sensitive_tastebuds = True
sim_fra1 = Simulation_unknown_best(num_townspeople, num_guacs, num_guacs, sensitive_tastebuds)
sim_fra1.simulate()

chosen_method = lg.tally_votes(sim_fra1, key="sim_fra1")
#the winner computed with the condocert method is the same as the avocado getting the most votes


st.subheader("2. Everyone Tries Only Some Guacs, Everyone is Fair, All Guacs are Relatively Good")
st.text("How much can we fraction guacs before we loose the winner?")
num_guac_per_person = lg.num_guac_per_person_slider()
sim_fra2 = Simulation_unknown_best(num_townspeople, num_guacs, num_guac_per_person)
sim_fra2.simulate(sim_fra1.results_df)
chosen_method = lg.tally_votes(sim_fra2, key="sim_fra2")


st.subheader("3. Everyone Tries Only Some Guacs, Everyone is Fair, Some Guacs have Better Ingredients than Others")
st.text("How much can we fraction guacs before we loose the winner?")
sim_fra3 = Simulation_unknown_best(num_townspeople, num_guacs, num_guac_per_person)
sim_fra3.simulate(sim_fra1.results_df)
chosen_method = lg.tally_votes(sim_fra3, key="sim_fra3")
