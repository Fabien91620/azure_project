# Azure_project

L'objectif de ce projet était de créer toute une infrastructure Azure afin de permettre à un utilisateur de se connecter depuis une interface, de pouvoir upload des images afin qu'elles soient enregistrées et tagées (via Computer vision). 
Et dans un second temps, de pouvoir venir sur cette même interface afin de chercher des images à partir de tags prédéfinis.

L'infrastructure Azure mise en place se compose des différents services suivants : 
- Ressource group
- Storage account (Dans lequel, nous avons créer un container afin de venir stocker les différentes images) 
- Une base de données Azure Mysql, pour venir y stocker les URL des images et leurs tags associés
- App service pour venir héberger et mettre en ligne notre application Streamlit
- Cognitive service afin de pouvoir utiliser l'API de computer vision 

Pour ce qui est du déploiement, nous avons tester deux possibilités, la première en utilisant git et en se basant sur la branch "main" de ce même repo et la seconde en utilisant docker.

La web app a été développée en python, avec la librairie streamlit. 
L'utilisateur peut venir upload une image et également rechercher des tags via la barre de recherche.
