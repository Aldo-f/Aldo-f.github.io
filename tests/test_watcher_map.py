"""Every known app repo must have an explicit destination mapping."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "documentation_watcher"))
import watcher  # noqa: E402


def test_all_dev_app_repos_are_mapped():
    dev = Path.home() / "dev"
    repos = {p.name for p in dev.iterdir()
             if p.is_dir() and p.name.startswith("06-apps-")
             and "-legacy" not in p.name}
    mapped = set(watcher.REPO_DEST_MAP)
    missing = repos - mapped
    assert not missing, f"Repos without destination mapping: {sorted(missing)}"


def test_every_destination_is_absolute():
    for repo, dests in watcher.REPO_DEST_MAP.items():
        assert dests, f"{repo} maps to empty destination list"
        for d in dests:
            assert Path(d).is_absolute(), f"{repo} -> {d} not absolute"


def test_bundle_receives_passive_income_docs():
    """Integration: a doc change lands in BOTH site mirror and bundle."""
    dests = watcher.REPO_DEST_MAP["06-apps-passive-income"]
    bundle_dest = [d for d in dests if "okf-home-lab" in d]
    assert bundle_dest, "passive-income must mirror into OKF bundle"


def test_letspeppol_is_bundle_only():
    """letspeppol is NOT Aldo's app: agent knowledge only, never published."""
    dests = watcher.REPO_DEST_MAP["06-apps-letspeppol"]
    site = [d for d in dests if "aldo-f-github-io" in d]
    bundle = [d for d in dests if "okf-home-lab" in d]
    assert bundle and not site, "letspeppol must map to OKF bundle only"


def test_neo_brutalist_publishes_and_mirrors():
    """Aldo's own app: published on the site AND mirrored into the bundle."""
    dests = watcher.REPO_DEST_MAP["06-apps-neo-brutalist-home"]
    site = [d for d in dests if "aldo-f-github-io" in d]
    bundle = [d for d in dests if "okf-home-lab" in d]
    assert site and bundle, "neo-brutalist-home needs both site and bundle destinations"
