import posixpath
import yaml
from github import Github

class GitHubRepoManager:
    def __init__(self, token):
        """
        Initialise la connexion à GitHub avec le token d'accès.
        """
        self.g = Github(token)
        self.user = self.g.get_user()

    def create_repo(self, name, private=False, description=""):
        """
        Crée un dépôt GitHub.
        
        :param name: Nom du dépôt
        :param private: Booléen indiquant si le dépôt est privé (True) ou public (False)
        :param description: Description du dépôt
        :return: L'objet repo créé, ou None en cas d'erreur
        """
        try:
            repo = self.user.create_repo(
                name=name,
                private=private,
                description=description
            )
            print("Dépôt créé :", repo.html_url)
            return repo
        except Exception as e:
            print("Erreur lors de la création du dépôt :", e)
            return None

    def add_file(self, repo, file_path, commit_message, content):
        """
        Ajoute un fichier au dépôt spécifié.

        :param repo: Objet du dépôt obtenu via create_repo
        :param file_path: Chemin et nom du fichier à créer dans le dépôt (ex. "README.md")
        :param commit_message: Message du commit associé à l'ajout du fichier
        :param content: Contenu du fichier à ajouter
        """
        try:
            repo.create_file(path=file_path, message=commit_message, content=content)
            print(f"Fichier '{file_path}' ajouté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du fichier '{file_path}' :", e)

    def add_structure(self, repo, structure, base_path=""):
        """
        Parcourt récursivement la structure et ajoute les fichiers/dossiers dans le dépôt.
        
        :param repo: Objet du dépôt GitHub.
        :param structure: Liste d'éléments (dictionnaires) définissant la structure.
        :param base_path: Chemin de base pour la récursion.
        """
        for item in structure:
            item_type = item.get("type")
            name = item.get("name")
            if not name or not item_type:
                continue  # Ignorer les éléments mal formés

            if item_type == "directory":
                # Concaténer le chemin courant et le nom du répertoire
                new_base = posixpath.join(base_path, name) if base_path else name
                children = item.get("children", [])
                if not children:
                    # Pour un dossier vide, on peut créer un fichier .gitkeep pour marquer le dossier
                    file_path = posixpath.join(new_base, ".gitkeep")
                    self.add_file(repo, file_path, f"Création du dossier {new_base}", "")
                else:
                    # Récursion sur les enfants du dossier
                    self.add_structure(repo, children, new_base)
            elif item_type == "file":
                # Concaténer le chemin courant et le nom du fichier
                file_path = posixpath.join(base_path, name) if base_path else name
                commit_message = f"Ajout de {file_path}"
                content = item.get("content", "")
                self.add_file(repo, file_path, commit_message, content)
