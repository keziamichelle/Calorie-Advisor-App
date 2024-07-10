import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import os
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are an expert nutritionist. Caculate the calories of each food item in the image in the format :
1. Item 1 - no of calories 
2. Item 2 - no of calories
----
----
Please mention if the food is healthy or not and the percentage split ratio of carbohydrates, proteins, fats, fibers, sugar and other required things in our diet."""

def get_response(prompt,image ):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([prompt, image[0]])
    return response.text
def input_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts

    else:
        raise FileNotFoundError("No File Uploaded")
st.title("Calorie Advisor App")
uploaded_file=st.file_uploader("Choose an Image: ", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
submit=st.button("Information about Total Calories")

if submit:
    image_data=input_setup(uploaded_file)
    response1=get_response(prompt, image_data)
    st.header("Here is your personalised nutrition information: ")
    st.write(response1)