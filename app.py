import streamlit as st
from transformers import pipeline
import pickle
import streamlit as st
import pandas
import numpy as np
import sklearn
import joblib
import scipy
from gmail_send import EmailSender
from product_recommender import BookRecommender




#--------------------- Instanciamos artefactos y funcion para recomendar productos

# Ejemplo de uso
model = 'artifacts/model.pkl'
book_names = 'artifacts/book_name.pkl'
final_rating = 'artifacts/final_rating.pkl'
book_pivot = 'artifacts/book_pivot.pkl'
book_recommender = BookRecommender(model, book_names, final_rating, book_pivot)
book_list = pickle.load(open(book_names, 'rb'))
#--------------------- Instanciamos artefactos y funcion para recomendar productos

# Load model for sentiment analysis using Hugging Face 
classifier = pipeline("sentiment-analysis")


#-------------------------------------------------------- START THE APP

# user data for email automation according to sentiment analysis results
customer_info = {
 "first_name" : "Diego",
 "last_name" : "Cotacio",
 "correo": "diego.cotacio44@gmail.com",
 "current_RFM": 545
}

#----------------------------------------------------------------

# Title of the page
st.title("Reseña del producto")

# Name of the product according to a list
selected_book = st.selectbox(
    "Type or select a book from the dropdown",
    book_list)

# Comments of the user related to the producto selected
user_input = st.text_input("Ingrese su comentario")

# It a UI botom but also a trigger to generate a sentiment analisis, producto recomendation and send an email
if st.button("Comentar"):
    # Realizar el análisis de sentimiento
    result = classifier(user_input)[0]
    label = result["label"]
    
    # Mostrar el mensaje correspondiente según el valor de la etiqueta
    if label == "POSITIVE":

        # Si es positivo creamos recomendaciones nuevas y ofrecemos descuento para proxima compra
        recommend_list = book_recommender.recommend_book1(selected_book)

        formatted_list = "\n".join(["* " + book for book in recommend_list])
        
        # Email input
        username = customer_info["first_name"]
        body = f"Hola {username}, gracias por tu review!\nTe obsequiamos un bono de 10% para tu proximo libro\nEstas son algunas referencias que las personas recomiendan:\n\n{formatted_list}"
        sender_email = "diego.cotacio44@gmail.com"
        sender_password = 'yuskldopcttjljxk'
        receiver_email = customer_info["correo"]
        subject = 'ABC te agradece por tu review, esto te gustara ..'

        # email sender
        email_sender = EmailSender(sender_email, sender_password)
        email_sender.send_email(receiver_email, subject, body)

        st.write("Gracias por tu review! una sorpresa llegara a tu correo c:")



    elif label == "NEGATIVE":

        # Si es positivo creamos recomendaciones nuevas y ofrecemos descuento para proxima compra
        recommend_list = book_recommender.recommend_book1(selected_book)

        formatted_list = "\n".join(["* " + book for book in recommend_list])
        
        # Email input
        username = customer_info["first_name"]
        body = f" Hola {username} lamentamos tu experiencia con nuestro libro :c \n Te queremos compensar con un descuento de 20% para tu proxima compra\nSi estas interesado en algun libro, tal vez estos te puedan interesar:\n\n{formatted_list}"
        sender_email = 'diego.cotacio44@gmail.com'
        sender_password = 'yuskldopcttjljxk' #variable de entorno
        receiver_email = customer_info["correo"]
        subject = 'Te compensamos con un bono..'
        
        # email sender
        email_sender = EmailSender(sender_email, sender_password)
        email_sender.send_email(receiver_email, subject, body)
        
        st.write("te queremos compensar por tu mala experiencia, revisa tu correo c:")


