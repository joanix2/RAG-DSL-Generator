import os
import hashlib
import xml.etree.ElementTree as ET

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from src.parser import parse_xml_file
from src.build import build_infrastructure
from src.mongo import connect_to_mongo, get_or_create_collection

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config["JWT_SECRET_KEY"] = "votre_cle_secrete_pour_jwt"  # Changez cette clé pour quelque chose de sécurisé
jwt = JWTManager(app)

# Chemin par défaut pour l'infrastructure
BASE_OUTPUT_DIR = os.path.join("output")
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

# Connexion à la base MongoDB
DATABASE_NAME = "authdb"
COLLECTION_NAME = "users"
client = connect_to_mongo()
users_collection = get_or_create_collection(client, DATABASE_NAME, COLLECTION_NAME)

@app.route('/signup', methods=['POST'])
def signup():
    """
    Endpoint pour créer un nouvel utilisateur.
    """
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    # Vérifier si l'utilisateur existe déjà
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400

    # Hacher le mot de passe avant de le stocker
    hashed_password = generate_password_hash(password)

    # Insérer l'utilisateur dans la base de données
    user = {"username": username, "password": hashed_password}
    users_collection.insert_one(user)

    return jsonify({"message": "Utilisateur créé avec succès"}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint pour s'authentifier et obtenir un token JWT.
    """
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    # Vérifier si l'utilisateur existe
    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    # Vérifier le mot de passe
    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    # Créer un token JWT
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/compile', methods=['POST'])
@jwt_required()
def compile_endpoint():
    """
    Endpoint pour traiter un fichier XML envoyé directement 
    dans le body de la requête (content-type : text/xml ou application/xml).
    """
    try:

        # Récupérer l'utilisateur connecté (du JWT)
        current_user = get_jwt_identity()
        print(f"Requête effectuée par : {current_user}")

        # 1. Récupère le contenu brut de la requête
        xml_content = request.get_data(as_text=True)  # as_text=True => str, sinon bytes
        
        # 2. Créer un hash du contenu XML
        hash_value = hashlib.md5(xml_content.encode('utf-8')).hexdigest()
        
        # 3. Créer un dossier nommé avec ce hash
        output_dir = os.path.join(BASE_OUTPUT_DIR, hash_value)
        os.makedirs(output_dir, exist_ok=True)
        
        # 4. Parser l’arbre XML en mémoire (sans passer par un fichier)
        try:
            root = ET.fromstring(xml_content)
            infrastructure_path = os.path.join(output_dir, "infrastructure.yml")
            # Appelle la fonction pour traiter le fichier XML
            parse_xml_file(root, infrastructure_path)
        except ET.ParseError as e:
            return jsonify({"error": f"Erreur de parsing XML: {e}"}), 400
        
        return jsonify({
            "message": "Fichiers générés avec succès.",
            "id": hash_value,
            "output_dir": output_dir
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/build', methods=['POST'])
@jwt_required()
def build_endpoint():
    """
    Endpoint pour générer une arborescence de projet à partir d'un fichier YAML.

    Paramètres (JSON dans le body de la requête) :
        - config_file (str) : chemin vers le fichier YAML décrivant la structure du projet 
                             (par défaut : output/infrastructure.yml)
    """

    data = request.get_json(force=True)
    id = data.get('id')
    config_file = os.path.join(BASE_OUTPUT_DIR, id, "infrastructure.yml")

    try:
        # Appelle la fonction pour construire l'infrastructure
        build_infrastructure(config_file)
        return jsonify({
            "message": "Arborescence générée avec succès.",
            "config_file": config_file
        }), 200
    except FileNotFoundError:
        return jsonify({
            "error": f"Fichier introuvable : {config_file}"
        }), 404
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
@app.route('/check-mongo', methods=['GET'])
def check_mongo():
    """
    Vérifie la connexion à la base de données MongoDB.
    """
    try:
        # Test de connexion en listant les bases de données
        db_list = client.list_database_names()
        return jsonify({
            "message": "Connexion à MongoDB réussie.",
            # "databases": db_list
        }), 200
    except Exception as e:
        return jsonify({
            "message": "Impossible de se connecter à MongoDB.",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Par défaut, Flask écoute sur le port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
