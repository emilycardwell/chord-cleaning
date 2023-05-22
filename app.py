import streamlit as st
import requests
import base64
import numpy as np
import mingus.containers as mc
from mingus.midi import midi_file_out
from pretty_midi import PrettyMIDI
from IPython.display import Audio


# Background Image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('pics/vintage-2721099_1280_2.jpeg')

# Title
new_title = '<p style="font-family:sans-serif; color:Black; font-size: 42px;">Chord Progression Prediction</p>'
st.markdown(new_title, unsafe_allow_html=True)

# Input chords
new_text = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">Input 1 - 12 chords</p>'
st.markdown(new_text, unsafe_allow_html=True)
a = st.text_input("Input 1-12 chords", 'C, Dm, G7', label_visibility="collapsed")
b = a.replace(' ', '')
song = f'{b}'

# select number of chords to predict
new_text1 = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">Select a number of predicted chords.</p>'
st.markdown(new_text1, unsafe_allow_html=True)
n_chords = st.selectbox('Select a number of predicted chords.', np.arange(1, 13, 1, 'int'), index=3, label_visibility="collapsed")

# randomness slider
new_text2 = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">Pick the level of randomness (1 returns common chords, 10 returns more "interesting" chords).</p>'
st.markdown(new_text2, unsafe_allow_html=True)
randomness = st.slider('Pick the level of randomness.', 1, 10, 3, label_visibility="collapsed")
'''
---
'''
# call API
@st.cache(suppress_st_warning=True)
def call_api(song, n_chords, randomness):
    url = 'https://chords-progression-prediction-1-zkfrzn26zq-ew.a.run.app/predict'
    parameters = {'song': song, 'n_chords': n_chords, 'randomness': randomness}

    try:
        response = requests.get(url, params=parameters).json()
    except:
        response = 'Input Error, try again'

    return response

if st.button('Get your prediction'):
    new_text3 = '<p style="font-family:sans-serif; color:Red; font-size: 24px;">New chord progression:</p>'
    st.markdown(new_text3, unsafe_allow_html=True)
    new_text4 = f'<p style="font-family:sans-serif; color:Black; font-size: 20px;">{call_api(song, n_chords, randomness)["predicted_chord"]}</p>'
    st.markdown(new_text4, unsafe_allow_html=True)



# track = mc.Track().from_chords(new_text4, 1)
# midi_data = midi_file_out.MidiFile.get_midi_data()
# music = PrettyMIDI(midi_file=midi_data)

# sound2 = "soundfont_lib/YDP-GrandPiano-20160804.sf2"
# waveform = music.fluidsynth(44100.0, sound2)

# audio_file = Audio(waveform, rate=44100)
# audio_file
