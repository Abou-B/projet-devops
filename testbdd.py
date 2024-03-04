# importation des bibliothèques nécessaires
import streamlit as st
import sqlite3
import pandas as pd

# Fonction pour initialiser la base de données
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            quantite INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Fonction pour ajouter un élément à l'inventaire
def ajouter_element(nom, quantite):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (nom, quantite) VALUES (?, ?)", (nom, quantite))
    conn.commit()
    conn.close()

# Fonction pour récupérer tous les éléments de l'inventaire
def afficher_inventaire():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    data = c.fetchall()
    conn.close()
    return data

# Initialiser la base de données
init_db()

# Construction de l'interface utilisateur avec Streamlit
st.title('Système de Gestion d’Inventaire')

# Formulaire d'ajout d'élément à l'inventaire
with st.form("form_inventaire", clear_on_submit=True):
    nom = st.text_input('Nom de l’élément')
    quantite = st.number_input('Quantité', min_value=0, value=1, step=1)
    submitted = st.form_submit_button('Ajouter à l’inventaire')
    if submitted and nom:  # Vérifier si le nom n'est pas vide
        ajouter_element(nom, quantite)
        st.success(f"L’élément {nom} a été ajouté avec succès !")

# Affichage de l'inventaire
st.subheader('Inventaire')
data = afficher_inventaire()

# Convertir les données en DataFrame pour une meilleure visualisation
df = pd.DataFrame(data, columns=['ID', 'Nom', 'Quantité'])
st.dataframe(df)
