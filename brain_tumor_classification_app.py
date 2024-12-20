# -*- coding: utf-8 -*-
"""brain_tumor_classification_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18_txTDSOAalm0Hl6MzBudlZCnWiHRh3q
"""

import streamlit as st
from joblib import load
import numpy as np
from PIL import Image

# Load the model
model = load('brain_tumor_classification_model.joblib')

# Streamlit app
st.title('Brain Tumor Classification')
uploaded_file = st.file_uploader("Upload an MRI image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image using PIL
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded MRI Image.', use_column_width=True)

    # Preprocess the image
    try:
        # Convert to RGB (if grayscale or other mode)
        img = img.convert('RGB')
        
        # Resize to match the model's expected input shape
        img = img.resize((150, 150))
        
        # Convert the image to a NumPy array and normalize pixel values
        img_array = np.array(img) / 255.0  # Normalize to range [0, 1]
        
        # Add batch dimension to make the shape (1, 150, 150, 3)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Ensure the input shape is correct
        st.write("Processed image shape:", img_array.shape)

        # Make predictions using the model
        result = model.predict(img_array)
        class_names = ['glioma tumor', 'meningioma tumor', 'no tumor', 'pituitary tumor']
        predicted_class = class_names[np.argmax(result[0])]
        st.write('Prediction:', predicted_class)
    except Exception as e:
        st.error(f"Error during prediction: {e}")
