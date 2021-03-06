J'ai fait quelques modifications sur le python existant en gardant les mêmes fonctionnalités. J'explique les fonctionnalités souhaitées par la suite.

# Ce que j'ai fait
## Backend
#### booking/models.py
* Ajout de deux signaux pour automatiquement set l'attribut *disponibility* des instances de Car à *True* ou *False* en fonction de la création ou suppression d'une instance de Booking.

#### booking/views.py
* Suppression de get_cars (voir car/models.py)
* Suppression de set_car_disponibility (opération automatique avec les signaux)
* transformation de la vue *new* en CBV. 
  * Pas indispensable mais plus lisible avec la séparation get/post. 
  * Dans cette vue, j'ai utilisé datetime.utcnow() pour être certain que les dates soient homogènes. Le frontend se chargera de l'affichage à la bonne timezone via des filtres par exemple.
  * Ajout de messages personnalisés pour alerter l'utilisateur des erreurs possibles (plus aucune voiture disponible par exemple).

car/models.py
* Ajout d'un Manager pour obtenir le queryset des instances de Car où disponibility = 1.

## Frontend
#### booking/base.html
* Affichage des messages d'erreurs

# Idées d'améliorations à fournir
* Ajout d'une interface de login pour les *transporteurs*. Ceux ci auraient la possibilité d'accepter des réservations. Il faudrait donc ajouter une NullFK vers un transporteur_id sur Booking.
* Sur la classe Car, ajout d'attributs supplémentaires (*nb_seats* pour le nombre de places, FK sur transporteur_id si on envisage qu'un transporteur peut détenir un parc de plusieurs voitures...).
* Éventuellement, on pourrait avoir des sous classes de Car identifiant le type de navette (grande, petite, luxe, économique etc.)
* Il faudrait ajouter des BooleanField (*active*, *canceled*, *ended*) sur Booking. 
  * Une instance de Booking pourrait se trouver dans ces 3 états.
  * Possibilité de consulter sa réservation en cours, ses réservations terminées (avec affichage du trajet), ses reservations en attente.
  * D'un point de vue backend, cela nécéssite l'ajout de différentes vues (*cancel_booking* du côté utilisateur, *accept_booking* du côté transporteur etc.)
* Interface de paiement ou liaison du compte Padam à un compte bancaire avec débit automatique dès qu'une instance de Booking passe de *active* à *ended*.
* Possibilité de contacter le service client via l'application.
* Possibilité de demander un nouveau mot de passe.
* Possibilité de modifier ses informations personnelles.
* Possibilité d'accéder aux informations des transporteurs, de donner des notes...
* Géolocalisation en direct de la navette pendant le trajet.
  
