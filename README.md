# RAG-DSL-Generator

### Commande Docker pour créer un conteneur MongoDB

Vous pouvez exécuter la commande suivante pour lancer un conteneur MongoDB :

```bash
docker run -d --name mongodb-container \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo
```

#### Explications :

- `-d` : Lance le conteneur en arrière-plan (mode détaché).
- `--name mongodb-container` : Nomme le conteneur.
- `-p 27017:27017` : Expose le port 27017 (le port par défaut de MongoDB) du conteneur sur l'hôte.
- `-e MONGO_INITDB_ROOT_USERNAME=admin` : Définit l'utilisateur administrateur.
- `-e MONGO_INITDB_ROOT_PASSWORD=password` : Définit le mot de passe administrateur.
- `mongo` : Utilise l'image officielle MongoDB.

---

# Source
DSL parser :
https://github.com/textX/textX
https://github.com/davydany/data_transformer
