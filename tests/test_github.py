import unittest
from unittest.mock import MagicMock
import yaml
from rag_dsl_generator.src.github_manager import GitHubRepoManager

# Création d'un faux objet repo pour simuler le dépôt GitHub
class DummyRepo:
    def create_file(self, path, message, content):
        # Méthode simulée qui peut simplement retourner un dictionnaire
        return {"path": path, "message": message, "content": content}

class TestGitHubRepoManager(unittest.TestCase):

    def setUp(self):
        # Utilisation d'un token fictif pour les tests
        self.token = "dummy_token"
        self.manager = GitHubRepoManager(self.token)
        self.repo = DummyRepo()

    def test_add_file_calls_repo_create_file(self):
        """
        Vérifie que add_file appelle correctement repo.create_file avec
        les bons arguments.
        """
        file_path = "test.txt"
        commit_message = "Test commit"
        content = "Hello world"
        # Remplacer la méthode create_file par un MagicMock
        self.repo.create_file = MagicMock(return_value={"path": file_path})
        self.manager.add_file(self.repo, file_path, commit_message, content)
        self.repo.create_file.assert_called_once_with(
            path=file_path,
            message=commit_message,
            content=content
        )

    def test_add_structure_file(self):
        """
        Vérifie que pour un élément de type "file" dans la structure,
        add_structure appelle add_file avec les bons paramètres.
        """
        structure = [
            {
                "name": "test.txt",
                "type": "file",
                "content": "Hello"
            }
        ]
        # Remplacer la méthode add_file pour vérifier l'appel
        self.manager.add_file = MagicMock()
        self.manager.add_structure(self.repo, structure, base_path="")
        self.manager.add_file.assert_called_once_with(
            self.repo,
            "test.txt",
            "Ajout de test.txt",
            "Hello"
        )

    def test_add_structure_directory_with_child(self):
        """
        Vérifie que pour une structure contenant un dossier avec un enfant,
        le chemin complet du fichier est bien construit.
        """
        structure = [
            {
                "name": "dir",
                "type": "directory",
                "children": [
                    {
                        "name": "sub.txt",
                        "type": "file",
                        "content": "Sub file"
                    }
                ]
            }
        ]
        self.manager.add_file = MagicMock()
        self.manager.add_structure(self.repo, structure, base_path="")
        expected_file_path = "dir/sub.txt"
        self.manager.add_file.assert_called_once_with(
            self.repo,
            expected_file_path,
            f"Ajout de {expected_file_path}",
            "Sub file"
        )

    def test_add_structure_empty_directory(self):
        """
        Vérifie que pour un dossier vide, un fichier .gitkeep est créé.
        """
        structure = [
            {
                "name": "empty_dir",
                "type": "directory",
                "children": []
            }
        ]
        self.manager.add_file = MagicMock()
        self.manager.add_structure(self.repo, structure, base_path="")
        expected_file_path = "empty_dir/.gitkeep"
        self.manager.add_file.assert_called_once_with(
            self.repo,
            expected_file_path,
            "Création du dossier empty_dir",
            ""
        )

    def test_yaml_loading(self):
        """
        Vérifie que le fichier YAML est correctement chargé et analysé.
        """
        yaml_content = """
project_name: test_project
output_dir: out
structure:
  - name: file1.txt
    type: file
    content: "Content"
"""
        config = yaml.safe_load(yaml_content)
        self.assertEqual(config.get("project_name"), "test_project")
        self.assertEqual(config.get("output_dir"), "out")
        self.assertIn("structure", config)
        structure = config.get("structure")
        self.assertEqual(len(structure), 1)
        self.assertEqual(structure[0]["name"], "file1.txt")

if __name__ == '__main__':
    unittest.main()
