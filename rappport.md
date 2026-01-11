# SAÉ S3.C2 – Réduction d’étoiles en astrophotographie

## Auteurs
- Cuvelier Armand
- Sow Jordan
- Vannoorenberghe Nolan;  

## Objectif du projet
Ce projet a été réalisé dans le cadre de la SAÉ S3.C2 (BUT2).  
L’objectif est de développer un outil permettant de **réduire la taille apparente des étoiles** sur des images astronomiques au format FITS, afin de mieux faire ressortir les structures diffuses comme les nébuleuses et les galaxies.

## Méthode
Une première approche a utilisé une **érosion morphologique** sur toute l’image. Cette méthode réduit la taille des étoiles mais dégrade les détails de l’arrière-plan.  
Une approche améliorée applique un **masque d’étoiles**, ce qui permet de limiter le traitement uniquement aux zones contenant des étoiles et de mieux préserver le fond.
Pour obtenir ce masque, nous avons utilisé **une API d’astrométrie** qui permet de détecter automatiquement les étoiles dans l’image, garantissant ainsi un masque plus précis.

## Résultats
Les étoiles apparaissent moins dominantes et les structures de fond sont plus lisibles.  
Les résultats dépendent des paramètres choisis et nécessitent des ajustements selon l’image.
Nous disposons également d'une interface graphique permettant de changer un fichier FITS et de régler lesparamétres de réduction en temps réel.

## Difficultés rencontrées
- Manque de connaissances initiales sur l’utilisation des API.  
- Problèmes lors du traitement des images couleur.  
- Bugs liés à l’envoi de traitements via une API (gestion des jobs).  
- Réglage des paramètres parfois complexe et long.
