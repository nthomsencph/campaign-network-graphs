import streamlit as st

from src.viz import create_cast_plot

st.sidebar.title("Bridgelands")
st.sidebar.subheader(
    "A network of characters in the D&D campaign Bridgelands by Adnan Akçay"
)


fig = create_cast_plot()
# iplot(fig, filename = 'campaign')

st.plotly_chart(fig)
