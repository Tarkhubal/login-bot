# Aide sur les configurations

## Images docker

Les images docker sont définies dans la clé "docker_images" et sont de la forme suivante :

```json
{
    "docker": "ghcr.io/parkervcp/yolks:python_3.11", // "adresse" de l'image docker
    "name": "Python", // Nom affiché de l'image docker
    "code": "python" // Code de l'image docker (utilisé par le bot, doit être unique!)
}
```

## Système de niveaux

### Assignation d'un niveau à un rôle

Vous pouvez créer un "niveau" simplement en rajoutant un rôle et en ajoutant le nom du niveau à la suite dans la clé "levels". Ces niveaux permettent d'attribuer des rôles à des membres en fonction de leur niveau (exemple un niveau "special" pour les amis de l'owner...).

Les niveaux fournies par défaut par le bot sont les suivants :

- "admins" : niveau pour les administrateurs
- "special" : niveau pour les amis de l'owner
- "premium" : niveau pour les membres premium
- "default" : niveau par défaut pour les membres

### Informations des niveaux

Les informations des niveaux sont définies dans la clé "levels_infos" et sont de la forme suivante :

```json
"premium": { // Code du niveau
    "rank": 1, // Rang du niveau : plus le rang est élevé, plus le niveau est "prestigieux"
    "name": "Premium", // Nom affiché du niveau
    "color": "0xFF0000", // Couleur du niveau
    "emoji": "👑", // Emoji du niveau
    "images": "python,java", // Liste des images docker autorisées
    "specific_perms": "0", // Permissions spécifiques du niveau
    "max_panels": 5, // Nombre maximum de panels que peut avoir un membre de ce niveau
    "description": "Niveau premium, réservé aux membres ayant souscrit à un abonnement premium." // Description du niveau
}
```

La clé "rank" permet de définir l'ordre des niveaux, par exemple le niveau par défaut a une valeur de 0, et plus le niveau est "prestigieux", plus sa valeur est élevée (par logique, un niveau "admins" aura la valeur la plus haute). Si vous modifier manuellement les rangs, veillez à ne pas mettre deux niveaux à la même valeur car cela pourrait causer des problèmes dans le fonctionnement du bot qui peuvent aller jusqu'à corrompre toutes les données enregistrées, ainsi que créer des problèmes de sécurité sur votre panel Pelican.

Les clés "name", "color", "emoji" et "description" sont assez explicites, elles permettent de définir le nom affiché du niveau, sa couleur, l'emoji qui lui est associé et une description du niveau. Elles ne servent pas au bot mais uniquement aux utilisateurs pour comprendre chaque niveau.

La clé "images" permet de définir les images docker autorisées pour ce niveau. Si vous souhaitez autoriser toutes les images, mettez la valeur à "-1". Si vous souhaitez autoriser une seule image, mettez le code de l'image (exemple : "python"). Si vous souhaitez autoriser plusieurs images, séparez les noms par une virgule (exemple : "python,java"). Si vous souhaitez autoriser aucune image, mettez la valeur à "0".

La clé "specific_perms" permet de définir des permissions spécifiques pour ce niveau. Les différentes permissions sont les suivantes :
- "manage_others" : permet de gérer les panels des personnes de niveaux inférieurs
- "manage_nodes" : permet de gérer les nodes
- "delete_others" : permet de supprimer les panels de personnes de niveaux inférieurs
- d'autres permissions seront ajoutées dans le futur

Vous pouvez combiner les permissions en les séparant par des virgules (exemple : "manage_others,manage_nodes"). Si vous ne souhaitez pas donner de permissions spécifiques, mettez la valeur à "0". Si vous souhaitez donner toutes les permissions, mettez la valeur à "-1", mais attention à ne pas donner des permissions trop importantes à des membres qui ne devraient pas les avoir, nous vous conseillons de ne pas donner de permissions spécifiques à des membres de niveaux inférieurs à "admins".

La clé "max_panels" permet de définir le nombre maximum de panels que peut avoir un membre de ce niveau. Si vous souhaitez autoriser un nombre illimité de panels pour ce niveau, mettez la valeur à "-1".

## Configurations

Le système de configurations permet de définir des configurations pour les membres en fonction de leur niveau. Les admins avec des permissions "-1" peuvent créer de nouveaux panels en outre-passant les niveaux (en gros ils peuvent créer des panels par exemple "premium" à quelqu'un qui n'est pas premium). Les configurations sont définies dans la clé "configs" et sont de la forme suivante :

```json
{
    "name": "Configuration abusée", // Nom affiché de la configuration
    "id_name": "yes",               // Code de la configuration (utilisé par le bot, doit être unique!)
    "cpu": 200,                     // CPU en pourcentage
    "disk": 4000,                   // Disque en Mo
    "ram": 4096,                    // RAM en Mo
    "swap": 0,                      // Swap en Mo
    "gived_if": "special",          // Niveau nécessaire pour obtenir cette configuration
    "node": 1                       // ID du node sur lequel cette configuration est disponible
}
```
Attention à ne surtout pas oublier de renseigner une seule des valeurs, sinon la configuration ne fonctionnera pas. Si vous souhaitez par exemple renseigner un CPU illimité, mettez la valeur à "-1". Le swap est le seul à pouvoir être définie sur 0, si vous renseigner un CPU, disque ou RAM à 0, le bot l'interprètera comme une valeur infinie.

La clé "gived_if" permet de définir quel niveau est nécessaire pour obtenir cette configuration.

## Autres configurations

"logs_channel" : ID du salon de logs
"url" : URL du panel Pelican
"api_key" : Clé API de Pelican