> WARNING: THIS FILE CONTAINS SOLUTIONS

# Introduction

Welcome to the beginning of your Streamlit career!
Here you will be guided through some of the very basics.
This assignment is optional for those wanting a easy landing without digging through documentation.

# Assignment 0A: Writing text
Fire up a locally hosted app with some static text fields. 
Try the following commands and see how easy it is to get different formatting.
- `st.title`
- `st.header`
- `st.text`
- `st.write`
- `st.success`
- `st.error`

To run you app type `uv run streamlit run <path_to_file.py>` in your terminal

## Solution
``` python
import streamlit as st

st.title("Title")
st.header("Header")
st.text("Text")
st.write("Write")
st.success("Success")
st.error("Error")
```


# Assignment 0B: Buttons
Fire up a locally hosted app with a button that says "Click me". Use the `st.button` command.
Bonus: Flavor up the page by executing `st.balloons()` when the button is clicked
Having fun yet?

## Solution
``` python
import streamlit as st

if st.button("Click me"):
    st.balloons()
```

# Assignment 0C: Getting input
Explore the input possibilities. 
Use a text input field (`st.text_input`) to fill in your name. 
Add a slider (`st.slider`) to fill in your age.
Write both to the app with text fields (`st.write`).

## Solution
```
import streamlit as st

name = st.text_input("Enter your name:")

if name:
    st.success(f"Welcome, {name}!")

# Slider
age = st.slider("Select your age:", 0, 100, 25)
st.write(f"You are {age} years old.")
```


# Assignment 0D: Page layout
Let's add some basic page layout.
Divide up you app in 2 columns (`st.columns(2)`).
On the left display the button you made in assignment 0B.
On the right display the text_input and slider input fields from assignment 0C.

## Solution
```
import streamlit as st


col1, col2 = st.columns(2)
with col1:
    if st.button("Click me"):
        st.balloons()
with col2:
    name = st.text_input("Enter your name:")

    if name:
        st.success(f"Welcome, {name}!")

    # Slider
    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f"You are {age} years old.")
```

# Assignment 0E: Building an app
Let's combine everything and start building your first "app".
Your instructions are:
- Add 2 columns (`st.columns(2)`). 
  - The left column must contain the button "Get Compliment". (`st.button`)
  - The right column must contain the button "Roast Hosts". (`st.button`)
- Nex add 3 columns below (`st.columns(3)`). 
  - Each column contains one of Image1.jpg, Image2.jpg, Image3.jpg found in the datasets folder (`st.image`)
  - Each column must contain a text field: 
      - datasets/text_1.py and datasets/text_2.py both contain a list called "data" with strings (NO PEAKING). 
      - When Button 1 is pressed, display a random choice of the entries of text_1 below each image. `random.choice(text_1.data)`
      - When Button 2 is pressed, display a random choice of the entries of text_2 below each image. `random.choice(text_2.data)`
- Bonus: Make the text more happy when Button 1 is pressed with `st.succes` or bad looking when Button 2 is pressed `st.error`

What were your favorite results?

## Solution
```python
import streamlit as st
import random
from datasets import text_1, text_2

kind = None

# --- Images ---
images = [
    "datasets/Image1.jpg",
    "datasets/Image2.jpg",
    "datasets/Image3.jpg",
]


# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Get Compliment 😄"):
        text = [random.choice(text_1.data) for _ in range(3)]
        kind = "Success"

with col2:
    if st.button("Roast Hosts 🔥"):
        text = [random.choice(text_2.data) for _ in range(3)]
        kind = "Failure"

st.title("Get to know the workshop hosts")

# --- Layout: 3 columns ---
cols = st.columns(3)

for i, col in enumerate(cols):
    with col:
        st.image(images[i])
        if kind == "Success":
            st.success(text[i])
        if kind == "Failure":
            st.error(text[i])
```