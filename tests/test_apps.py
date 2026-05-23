"""Validation du fichier data/apps.yaml."""
from pathlib import Path

import pytest
import yaml

APPS_YAML = Path(__file__).parent.parent / "data" / "apps.yaml"
VALID_STATUSES = {"live", "dev", "hidden"}
REQUIRED_FIELDS = {
    "id",
    "name",
    "name_en",
    "description",
    "description_en",
    "url",
    "category",
    "category_en",
    "status",
}


@pytest.fixture(scope="module")
def apps_data():
    with open(APPS_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_yaml_loads(apps_data):
    """Le fichier YAML se charge sans erreur."""
    assert apps_data is not None
    assert "apps" in apps_data
    assert "categories_fr" in apps_data
    assert "categories_en" in apps_data


def test_categories_balanced(apps_data):
    """categories_fr et categories_en ont le même nombre d'entrées."""
    assert len(apps_data["categories_fr"]) == len(apps_data["categories_en"])


def test_apps_not_empty(apps_data):
    assert len(apps_data["apps"]) > 0


def test_required_fields(apps_data):
    """Chaque app a les champs obligatoires."""
    for app in apps_data["apps"]:
        missing = REQUIRED_FIELDS - set(app.keys())
        assert not missing, f"App {app.get('id', '?')} - champs manquants : {missing}"


def test_status_enum(apps_data):
    """Tous les statuts sont dans l'enum autorisé (live | dev | hidden)."""
    for app in apps_data["apps"]:
        assert app["status"] in VALID_STATUSES, (
            f"App {app['id']} - statut invalide : {app['status']!r}"
        )


def test_unique_ids(apps_data):
    """Tous les IDs sont uniques."""
    ids = [app["id"] for app in apps_data["apps"]]
    duplicates = [i for i in ids if ids.count(i) > 1]
    assert len(ids) == len(set(ids)), f"IDs dupliqués : {duplicates}"


def test_category_references_known(apps_data):
    """Chaque app référence une catégorie définie dans categories_fr/en."""
    known_fr = set(apps_data["categories_fr"])
    known_en = set(apps_data["categories_en"])
    for app in apps_data["apps"]:
        assert app["category"] in known_fr, (
            f"App {app['id']} - catégorie FR inconnue : {app['category']!r}"
        )
        assert app["category_en"] in known_en, (
            f"App {app['id']} - catégorie EN inconnue : {app['category_en']!r}"
        )


def test_urls_not_empty(apps_data):
    """Tous les URLs sont non vides."""
    for app in apps_data["apps"]:
        assert app.get("url", "").strip(), f"App {app['id']} - URL vide."
