#!/usr/bin/env python3
"""Verify generated CORA pages without third-party Python dependencies.

Usage: python3 scripts/verify.py dist --base-path /repository-name
The report contains source/data checks, not a claim of browser or deployed CI QA.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_CSS_SHA256 = "5f4296668cbb808319d0157b0cdd7493ddebb532078f1f8ee30cf89e96e70b5e"
REFERENCE_COMMIT = "822bb4dcef3c9e834f9c7486758ce532e05ddc63"
EXPECTED_PAGES = {
    "index.html", "about/index.html", "research/index.html", "projects/index.html",
    "publications/index.html", "people/index.html", "people/kwangki-kim/index.html",
    "teaching/index.html", "contact/index.html", "credits/index.html", "404.html",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ORIGINAL_IDENTITY = re.compile(r"clearobotics|CLeAR\s+(?:Robotics\s+)?Lab|Fridovich[-– ]Keil|utexas\.edu|UT Austin|University of Texas|kordinglab", re.I)
FORBIDDEN_ENDPOINT = re.compile(r"supabase|disqus|google-analytics\.com|googletagmanager\.com|UA-34145995|/intranet(?:/|\b)", re.I)
CSS_URL = re.compile(r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s)]+))\s*\)", re.I)


def normalized(value: str) -> str:
    return " ".join(value.split())


def normalized_doi(value: str) -> str:
    """DOI identifiers compare equally with URL prefixes, case, or URL escaping."""
    value = unquote(value).strip().casefold()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value)
    return value.strip()


def title_key(value: str) -> str:
    return re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", value).casefold())


@dataclass
class Node:
    tag: str
    attrs: dict[str, str | None] = field(default_factory=dict)
    children: list = field(default_factory=list)

    def text(self) -> str:
        if self.tag in {"script", "style"}:
            return ""
        return " ".join(child if isinstance(child, str) else child.text() for child in self.children)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()


class Document(HTMLParser):
    def __init__(self, content: str):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(content)
        self.close()
        self.nodes = list(self.root.walk())[1:]
        self.ids = [node.attrs["id"] for node in self.nodes if node.attrs.get("id")]
        self.anchors = set(self.ids) | {node.attrs["name"] for node in self.nodes if node.tag == "a" and node.attrs.get("name")}
        self.visible_text = normalized(self.root.text())

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)

    def by_id(self, identifier):
        return next((node for node in self.nodes if node.attrs.get("id") == identifier), None)

    def links(self):
        return {node.attrs["href"] for node in self.nodes if node.attrs.get("href")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", default="dist")
    parser.add_argument("--base-path", default="")
    parser.add_argument("--report", default=str(ROOT / "docs/VALIDATION.json"))
    args = parser.parse_args()
    output = Path(args.output).resolve()
    base = "/" + args.base_path.strip("/") if args.base_path.strip("/") else ""
    if base and (not re.fullmatch(r"/[A-Za-z0-9._/-]+", base) or any(part in {".", ".."} for part in base.split("/"))):
        parser.error("Invalid base path")
    errors, warnings = [], []
    counts = Counter()
    people_path = ROOT / "data/people.json"
    people_data = json.loads(people_path.read_text()) if people_path.is_file() else {}
    people_records = people_data.get("people", [])
    project_path = ROOT / "data/projects.json"
    project_data = json.loads(project_path.read_text()) if project_path.is_file() else {}
    project_records = project_data.get("projects", [])
    expected_pages = set(EXPECTED_PAGES)
    expected_pages.update(f"projects/{project['id']}/index.html" for project in project_records)
    expected_pages.update(
        f"people/{person['id']}/index.html"
        for person in people_records if person.get("category") != "alumni"
    )
    documents = {}
    origin = "https://cora-validation.invalid"
    for file in sorted(output.rglob("*.html")):
        relative = file.relative_to(output).as_posix()
        text = file.read_text(encoding="utf-8")
        doc = Document(text)
        documents[file] = doc
        if relative != "credits/index.html" and ORIGINAL_IDENTITY.search(text):
            errors.append(f"{relative}: original lab identity or destination remains")
        if FORBIDDEN_ENDPOINT.search(text):
            errors.append(f"{relative}: original authentication or analytics endpoint remains")
        duplicates = [identifier for identifier, count in Counter(doc.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{relative}: duplicate IDs {duplicates}")
        if len([node for node in doc.nodes if node.tag == "h1"]) != 1:
            errors.append(f"{relative}: expected one H1")
        titles = [node for node in doc.nodes if node.tag == "title"]
        if len(titles) != 1 or "CORA Lab" not in titles[0].text():
            errors.append(f"{relative}: missing CORA page title")
        for node in doc.nodes:
            if node.tag == "img" and not node.attrs.get("alt"):
                errors.append(f"{relative}: image missing descriptive alt text")
    found_pages = {path.relative_to(output).as_posix() for path in documents}
    if found_pages != expected_pages:
        errors.append(f"Page inventory mismatch: missing={sorted(expected_pages-found_pages)}, unexpected={sorted(found_pages-expected_pages)}")

    def check_ref(owner: Path, raw: str, kind="html"):
        if not raw:
            return
        parts = urlsplit(raw)
        if parts.scheme or parts.netloc:
            if parts.scheme.lower() in {"javascript", "file"}:
                errors.append(f"{owner.relative_to(output)}: unsupported URL {raw}")
            return
        # CSS fragments may identify a font face or an SVG filter in that file.
        if kind == "css" and raw.startswith("#"):
            return
        page_url = origin + base + "/" + owner.relative_to(output).as_posix()
        resolved = urlsplit(urljoin(page_url, raw))
        path = unquote(resolved.path)
        if base and path != base and not path.startswith(base + "/"):
            errors.append(f"{owner.relative_to(output)}: URL escapes base path: {raw}")
            return
        target = (output / path[len(base):].lstrip("/")).resolve()
        if target != output and output not in target.parents:
            errors.append(f"{owner.relative_to(output)}: URL escapes output: {raw}")
            return
        if target.is_dir():
            target = target / "index.html"
        elif not target.exists() and target.suffix == "" and target.with_suffix(".html").exists():
            target = target.with_suffix(".html")
        counts[f"{kind}_local_references"] += 1
        if not target.is_file():
            errors.append(f"{owner.relative_to(output)}: missing local target {raw}")
        elif resolved.fragment and target in documents:
            counts["html_fragment_references"] += 1
            fragment = unquote(resolved.fragment)
            if fragment not in documents[target].anchors and fragment not in {"top"} and not fragment.startswith(":~:text="):
                errors.append(f"{owner.relative_to(output)}: missing anchor {raw}")

    for file, doc in documents.items():
        for node in doc.nodes:
            for attr in ("href", "src", "poster"):
                if node.attrs.get(attr):
                    check_ref(file, node.attrs[attr])
            if node.tag == "object" and node.attrs.get("data"):
                check_ref(file, node.attrs["data"])
            if node.attrs.get("style"):
                for match in CSS_URL.finditer(node.attrs["style"]):
                    check_ref(file, next(value for value in match.groups() if value is not None), "css")
            if node.tag == "style":
                for match in CSS_URL.finditer("".join(child for child in node.children if isinstance(child, str))):
                    check_ref(file, next(value for value in match.groups() if value is not None), "css")
    for file in sorted(output.rglob("*.css")):
        # Archival, unreferenced upstream CSS intentionally retains its old URLs.
        # Runtime pages load the relocated stylesheets in vendor/css instead.
        if file.is_relative_to(output / "vendor/provenance"):
            counts["archival_css_files_excluded"] += 1
            continue
        text = re.sub(r"/\*.*?\*/", "", file.read_text(encoding="utf-8"), flags=re.S)
        for match in CSS_URL.finditer(text):
            check_ref(file, next(value for value in match.groups() if value is not None), "css")
    for file in list((output / "assets").glob("*.js")) + list((output / "vendor/js").glob("*.js")):
        if FORBIDDEN_ENDPOINT.search(file.read_text(encoding="utf-8")):
            errors.append(f"{file.relative_to(output)}: original authentication or analytics endpoint remains")

    facts = json.loads((ROOT / "data/verified-facts.json").read_text())
    content = json.loads((ROOT / "data/content.json").read_text())
    publication_path = ROOT / "data/publications.json"
    publication_source = "data/publications.json" if publication_path.is_file() else "data/verified-facts.json"
    publication_records = json.loads(publication_path.read_text())["records"] if publication_path.is_file() else facts["publications"]
    expanded_publications = publication_path.is_file()

    def doc_for(route):
        return documents.get(output / route)

    def expect_text(route, value, label):
        counts["data_text_checks"] += 1
        doc = doc_for(route)
        if not doc or normalized(str(value)) not in doc.visible_text:
            errors.append(f"{route}: rendered data missing: {label}")

    def expect_link(route, url):
        counts["data_link_checks"] += 1
        doc = doc_for(route)
        if not doc or url not in doc.links():
            errors.append(f"{route}: data link missing: {url}")

    projects_doc = doc_for("projects/index.html")
    project_nodes = [node for node in projects_doc.nodes if node.attrs.get("data-project-id")] if projects_doc else []
    if not project_records or len(project_nodes) != len(project_records):
        errors.append(f"Project count mismatch or empty collection: source={len(project_records)}, rendered={len(project_nodes)}")
    project_ids = [project.get("id") for project in project_records]
    if len(set(project_ids)) != len(project_ids):
        errors.append("Duplicate project IDs")
    if [node.attrs.get("data-project-id") for node in project_nodes] != project_ids:
        errors.append("Project section order differs from source data")
    for field in ("intro_en", "intro_ko"):
        if not project_data.get(field):
            errors.append(f"Projects source is missing {field}")
        else:
            expect_text("projects/index.html", project_data[field], "Projects " + field)
    for project in project_records:
        identifier = project.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier):
            errors.append(f"Invalid project ID: {identifier!r}")
        section = projects_doc.by_id(identifier) if projects_doc else None
        if section not in project_nodes:
            errors.append(f"Projects: missing section anchor {identifier}")
            continue
        detail_route = f"projects/{identifier}/index.html"
        detail_url = base + f"/projects/{identifier}/"
        section_links = {node.attrs.get("href") for node in section.walk() if node.tag == "a"}
        if detail_url not in section_links:
            errors.append(f"Project {identifier}: missing link from overview card to detail")
        expect_link("projects/index.html", base + "/projects/#" + identifier)
        expect_link(detail_route, base + "/projects/#" + identifier)
        expect_text("projects/index.html", project.get("short_label", ""), "Project jump label " + identifier)
        detail_doc = doc_for(detail_route)
        detail = next((n for n in detail_doc.nodes if n.attrs.get("data-project-detail") == identifier), None) if detail_doc else None
        if detail is None:
            errors.append(f"Project {identifier}: missing detail page or article")
            continue
        overview_values = [project.get(field) for field in ("program_label", "category", "title_en", "title_ko", "overview_en", "overview_ko")]
        detail_values = overview_values + list(project.get("focus", []))
        detail_values += [item.get(field) for item in project.get("metadata", []) for field in ("label", "value")]
        if project.get("scope_ko"):
            detail_values.append(project["scope_ko"])
        for node, label, values in ((section, "summary", overview_values), (detail, "detail", detail_values)):
            text = normalized(node.text())
            for value in values:
                counts["project_text_checks"] += 1
                if not value or normalized(str(value)) not in text:
                    errors.append(f"Project {identifier}: {label} is missing {value!r}")
        detail_links = {(node.attrs.get("href"), normalized(node.text())) for node in detail.walk() if node.tag == "a"}
        for item in project.get("links", []) + project.get("related_links", []):
            url = item["url"]
            url = base + url if url.startswith("/") else url
            counts["project_link_checks"] += 1
            if (url, normalized(item["label"])) not in detail_links:
                errors.append(f"Project {identifier}: missing labeled link {url}")
    expect_link("index.html", base + "/projects/")
    for file, doc in documents.items():
        navigation = next((node for node in doc.nodes if node.tag == "nav" and node.attrs.get("aria-label") == "Main navigation"), None)
        project_nav = [node for node in navigation.walk() if node.tag == "a" and node.attrs.get("href") == base + "/projects/"] if navigation else []
        counts["project_navigation_checks"] += 1
        if len(project_nav) != 1 or normalized(project_nav[0].text()) != "Projects":
            errors.append(f"{file.relative_to(output)}: Projects navigation link missing or duplicated")
        elif file.is_relative_to(output / "projects") and project_nav[0].attrs.get("aria-current") != "page":
            errors.append(f"{file.relative_to(output)}: Projects navigation lacks its active-page marker")

    papers_doc = doc_for("publications/index.html")
    paper_nodes = [node for node in papers_doc.nodes if "paper" in (node.attrs.get("class") or "").split()] if papers_doc else []
    if not publication_records or len(paper_nodes) != len(publication_records):
        errors.append(f"Publication count mismatch or empty collection: data={len(publication_records)}, rendered={len(paper_nodes)}")
    record_ids, record_dois, record_titles = {}, {}, {}
    known_years, known_types = set(), set()
    undated_count = 0
    for paper in publication_records:
        identifier = paper.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]*", identifier):
            errors.append(f"Publication has invalid or missing ID: {identifier!r}")
        if identifier in record_ids:
            errors.append(f"Duplicate publication ID: {identifier!r}")
        record_ids[identifier] = paper
        title = paper.get("title")
        if not isinstance(title, str) or not normalized(title):
            errors.append(f"Publication {identifier}: missing title")
        if not isinstance(paper.get("authors"), str):
            errors.append(f"Publication {identifier}: authors must be a string; use an empty string if unavailable")
        year = paper.get("year")
        if year is None:
            undated_count += 1
        elif not isinstance(year, int) or isinstance(year, bool) or year < 1000 or year > 9999:
            errors.append(f"Publication {identifier}: year must be an integer or null")
        else:
            known_years.add(year)
        if isinstance(title, str):
            key = (title_key(title), year)
            if key in record_titles:
                errors.append(f"Duplicate title/year: {identifier!r} and {record_titles[key]!r}")
            record_titles[key] = identifier
        doi = normalized_doi(paper.get("doi") or "")
        if doi:
            if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
                errors.append(f"Publication {identifier}: invalid DOI {paper['doi']!r}")
            if doi in record_dois:
                errors.append(f"Duplicate DOI: {identifier!r} and {record_dois[doi]!r}: {doi}")
            record_dois[doi] = identifier
        paper_type = paper.get("type")
        if expanded_publications and (not isinstance(paper_type, str) or not normalized(paper_type)):
            errors.append(f"Publication {identifier}: missing publication type")
        elif paper_type:
            known_types.add(paper_type)
        node = papers_doc.by_id(identifier) if papers_doc else None
        if node is None or node not in paper_nodes:
            errors.append(f"publications/index.html: missing paper ID {identifier}")
            continue
        paper_text = normalized(node.text())
        if re.search(r"\b(?:None|null|undefined|NaN)\b", paper_text):
            errors.append(f"Publication {identifier}: missing-value placeholder rendered")
        for field in ("title", "authors", "year", "venue", "volume", "issue", "pages", "article"):
            if paper.get(field) not in (None, ""):
                counts["data_text_checks"] += 1
                if normalized(str(paper[field])) not in paper_text:
                    errors.append(f"Publication {identifier}: missing rendered {field}")
        valid_year_values = {str(year)} if year is not None else {"", "undated"}
        if node.attrs.get("data-year") not in valid_year_values:
            errors.append(f"Publication {identifier}: incorrect year filter attribute")
        if expanded_publications:
            counts["data_text_checks"] += 1
            if paper_type and normalized(paper_type) not in paper_text:
                errors.append(f"Publication {identifier}: missing visible type label")
            if node.attrs.get("data-type") != paper_type:
                errors.append(f"Publication {identifier}: incorrect type filter attribute")
        links = {child.attrs["href"] for child in node.walk() if child.attrs.get("href")}
        rendered_dois = {normalized_doi(url) for url in links if urlsplit(url).netloc.casefold() in {"doi.org", "dx.doi.org"}}
        if rendered_dois != ({doi} if doi else set()):
            errors.append(f"Publication {identifier}: DOI links do not match source DOI")
        expected_links = [paper[key] for key in ("preprint", "code") if paper.get(key)]
        if not doi and paper.get("url"):
            expected_links.append(paper["url"])
        for url in expected_links:
            counts["data_link_checks"] += 1
            if url not in links:
                errors.append(f"Publication {identifier}: missing link {url}")
        if not paper.get("source") and not paper.get("provenance"):
            errors.append(f"Publication {identifier}: missing provenance")
    rendered_ids = {node.attrs.get("id") for node in paper_nodes}
    if rendered_ids != set(record_ids):
        errors.append("Rendered publication IDs differ from source collection")
    groups = [node for node in papers_doc.nodes if "paper-group" in (node.attrs.get("class") or "").split()] if papers_doc else []
    group_order, grouped_ids = [], []
    for group in groups:
        members = [node for node in group.walk() if "paper" in (node.attrs.get("class") or "").split()]
        member_years = {record_ids[node.attrs["id"]].get("year") for node in members if node.attrs.get("id") in record_ids}
        grouped_ids.extend(node.attrs.get("id") for node in members)
        headings = [node for node in group.walk() if node.tag in {"h2", "h3"}]
        label = normalized(headings[0].text()) if headings else ""
        if len(member_years) != 1:
            errors.append(f"Publication group {label!r}: empty or mixed years")
            continue
        year = next(iter(member_years))
        group_order.append(year)
        if year is None and not re.search(r"undated|(?:year|date)\s+(?:not (?:available|specified)|unavailable|unknown)", label, re.I):
            errors.append("Undated publications must be grouped under an explicit undated heading")
        elif year is not None and not re.search(rf"\b{year}\b", label):
            errors.append(f"Publication group heading does not match year {year}")
    expected_order = sorted(known_years, reverse=True) + ([None] if undated_count else [])
    if group_order != expected_order or Counter(grouped_ids) != Counter(node.attrs.get("id") for node in paper_nodes):
        errors.append("Publication groups must contain every paper once, ordered newest first with undated records last")
    year_select = papers_doc.by_id("paper-year") if papers_doc else None
    year_options = {node.attrs.get("value", normalized(node.text())) for node in year_select.walk() if node.tag == "option"} if year_select else set()
    expected_year_options = {""} | {str(year) for year in known_years}
    if undated_count:
        expected_year_options.add("undated")
    if year_options != expected_year_options:
        errors.append("Year filter options do not match known years and undated records")
    if expanded_publications:
        type_select = papers_doc.by_id("paper-type") if papers_doc else None
        type_options = {node.attrs.get("value", normalized(node.text())) for node in type_select.walk() if node.tag == "option"} if type_select else set()
        if type_options != {""} | known_types:
            errors.append("Type filter options do not match publication types")
    for item in facts["news"]:
        for key in ("date", "title", "text"):
            expect_text("index.html", item[key], "news " + key)
        expect_link("index.html", item["url"])
    for route in ("index.html", "about/index.html"):
        expect_text(route, content["mission"], "mission")
    for paragraph in content["approach"]:
        expect_text("about/index.html", paragraph, "research approach")
    profile_ids = {}
    for person in people_records:
        name = person.get("research_name_ko")
        if name and person.get("category") != "alumni":
            if name in profile_ids:
                errors.append(f"Research name {name!r} corresponds to multiple profiles")
            profile_ids[name] = person["id"]

    home_doc = doc_for("index.html")
    home_topics = [n for n in home_doc.nodes if n.attrs.get("data-research-id")] if home_doc else []
    if [n.attrs["data-research-id"] for n in home_topics] != [area["id"] for area in content["research"]]:
        errors.append("Home research topic IDs or order differ from the source")
    research_doc = doc_for("research/index.html")
    for area in content["research"]:
        identifier = area["id"]
        names = area.get("participants", [])
        expected_links = []
        for label in names:
            name = label[1:-1] if label.startswith("(") and label.endswith(")") else label
            if name in profile_ids:
                profile_id = profile_ids[name]
                expected_links.append((label, base + f"/people/{profile_id}/"))
                expect_link(f"people/{profile_id}/index.html", base + "/research/#" + identifier)
        home_topic = next((n for n in home_topics if n.attrs["data-research-id"] == identifier), None)
        detail_topic = research_doc.by_id(identifier) if research_doc else None
        for route, topic in (("index.html", home_topic), ("research/index.html", detail_topic)):
            groups = [n for n in topic.walk() if "research-participants" in (n.attrs.get("class") or "").split()] if topic else []
            if not names and not groups:
                continue
            if not topic or len(groups) != 1:
                errors.append(f"{route}: missing or duplicate participant list for {identifier}")
                continue
            row = groups[0]
            # HTMLParser splits a name from its following comma at a closing link.
            # Drop whitespace around commas after joining the descendant text nodes.
            visible = re.sub(r"\s*,\s*", ", ", normalized(row.text()))
            if visible != "참여연구원 " + ", ".join(names):
                errors.append(f"{route}: names, parentheses or order differ for {identifier}")
            links = [(normalized(n.text()), n.attrs.get("href")) for n in row.walk() if n.tag == "a"]
            if links != expected_links:
                errors.append(f"{route}: participant profile links differ for {identifier}")
            counts["research_roster_checks"] += 1
        for key in ("title", "body"):
            expect_text("research/index.html", area[key], area["id"] + " " + key)
        for topic in area["topics"]:
            expect_text("research/index.html", topic, area["id"] + " topic")
        for item in area["links"]:
            expect_link("research/index.html", item["url"])
        if area.get("image"):
            expect_text("research/index.html", area["caption"], "image caption")
            expect_link("research/index.html", area["image_source"])
    for course in content["courses"]:
        for key in ("title", "description"):
            expect_text("teaching/index.html", course[key], "course " + key)
        for topic in course["topics"]:
            expect_text("teaching/index.html", topic, "course topic")
    for resource in content["resources"]:
        for key in ("name", "description"):
            expect_text("teaching/index.html", resource[key], "resource " + key)
        expect_link("teaching/index.html", resource["url"])
    pi = facts["pi"]
    for field in ("name", "title", "department", "email"):
        expect_text("people/kwangki-kim/index.html", pi[field], "PI " + field)
    expect_text("people/index.html", pi["name"], "PI name")
    expect_link("contact/index.html", "mailto:" + pi["email"])
    expect_link("about/index.html", facts["project"]["source"])
    expect_link("publications/index.html", facts["lab"]["scholar"])
    people_categories = Counter(person.get("category") for person in people_records)
    people_doc = doc_for("people/index.html")
    people_nodes = [node for node in people_doc.nodes if node.attrs.get("data-person-id")] if people_doc else []
    if people_path.is_file():
        if not people_records:
            errors.append("People source collection is empty")
        category_keys = [category["key"] for category in people_data.get("categories", [])]
        if len(category_keys) != len(set(category_keys)):
            errors.append("Duplicate People category definitions")
        unknown_categories = set(people_categories) - set(category_keys)
        if unknown_categories:
            errors.append(f"Unknown People categories: {sorted(unknown_categories)}")
        source_person_ids = [person.get("id") for person in people_records]
        rendered_person_ids = [node.attrs.get("data-person-id") for node in people_nodes]
        if len(source_person_ids) != len(set(source_person_ids)):
            errors.append("Duplicate People source IDs")
        if Counter(rendered_person_ids) != Counter(source_person_ids):
            errors.append("People listing must contain every source member exactly once")
        groups = [node for node in people_doc.nodes if node.attrs.get("data-people-category")] if people_doc else []
        rendered_categories = [node.attrs["data-people-category"] for node in groups]
        expected_categories = [key for key in category_keys if people_categories[key]]
        if rendered_categories != expected_categories:
            errors.append("People groups must follow source order and omit empty categories")
        for group in groups:
            key = group.attrs["data-people-category"]
            members = [node.attrs["data-person-id"] for node in group.walk() if node.attrs.get("data-person-id")]
            expected_members = [person["id"] for person in people_records if person.get("category") == key]
            if members != expected_members:
                errors.append(f"People category {key!r}: members or source order differ")
        for person in people_records:
            identifier = person.get("id")
            if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
                errors.append(f"Invalid People ID: {identifier!r}")
            display_name = person.get("display_name") or person.get("title")
            card = next((node for node in people_nodes if node.attrs.get("data-person-id") == identifier), None)
            if card is None:
                continue
            card_text = normalized(card.text())
            counts["people_text_checks"] += 1
            if not display_name or normalized(display_name) not in card_text:
                errors.append(f"People {identifier}: name missing from listing")
            if person.get("category") == "alumni":
                continue
            route = f"people/{identifier}/index.html"
            expect_text(route, display_name, f"People {identifier} name")
            role = (person.get("position") or "").strip() or person.get("role")
            for key, value in (("role", role), ("email", person.get("email"))):
                if value:
                    counts["people_text_checks"] += 1
                    if normalized(value) not in card_text:
                        errors.append(f"People {identifier}: {key} missing from listing")
                    expect_text(route, value, f"People {identifier} {key}")
            card_links = {node.attrs["href"] for node in card.walk() if node.attrs.get("href")}
            if base + f"/people/{identifier}/" not in card_links:
                errors.append(f"People {identifier}: missing profile link")
            if person.get("email"):
                email_url = "mailto:" + person["email"]
                if email_url not in card_links:
                    errors.append(f"People {identifier}: missing listing email link")
                expect_link(route, email_url)
            image_url = base + person["image"]
            card_images = {node.attrs.get("src") for node in card.walk() if node.tag == "img"}
            profile_doc = doc_for(route)
            profile_images = {node.attrs.get("src") for node in profile_doc.nodes if node.tag == "img"} if profile_doc else set()
            counts["people_portrait_checks"] += 2
            if image_url not in card_images or image_url not in profile_images:
                errors.append(f"People {identifier}: source portrait missing from listing or profile")
            for degree in person.get("education", []):
                for key, value in degree.items():
                    if value:
                        expect_text(route, value, f"People {identifier} education {key}")
            for interest in person.get("research_interests", []):
                expect_text(route, interest, f"People {identifier} research interest")
            for publication in person.get("selected_publications", []):
                for key in ("authors", "title", "journal"):
                    if publication.get(key):
                        expect_text(route, publication[key], f"People {identifier} publication {key}")
                for key in ("paper", "link"):
                    if publication.get(key):
                        expect_link(route, publication[key])
    portrait = output / "assets/kwangki-kim.png"
    portrait_valid = portrait.is_file() and portrait.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    if not portrait_valid:
        errors.append("Missing or invalid PI portrait PNG")
    source_css = ROOT / "assets/style.css"
    built_css = output / "assets/style.css"
    css_hash = hashlib.sha256(source_css.read_bytes()).hexdigest()
    css_identical = css_hash == REFERENCE_CSS_SHA256 and built_css.is_file() and built_css.read_bytes() == source_css.read_bytes()
    if not css_identical:
        errors.append("Original template CSS no longer matches reference snapshot bytes")
    for source in (ROOT / "assets").rglob("*"):
        if source.is_file():
            target = output / source.relative_to(ROOT)
            if not target.is_file() or target.read_bytes() != source.read_bytes():
                errors.append(f"Asset copy differs: {source.relative_to(ROOT)}")
            else:
                counts["assets_byte_identical"] += 1
    if not (output / ".nojekyll").is_file():
        errors.append("Missing .nojekyll deployment marker")
    current_sources = (ROOT / "docs/CONTENT_SOURCES.md").read_text(encoding="utf-8")
    if "style.css" not in current_sources or REFERENCE_COMMIT not in current_sources:
        errors.append("Content provenance does not identify retained CSS/source commit")
    prior = ROOT / "docs/PRIOR_CONTENT_SOURCES.md"
    if prior.exists() and not re.search(r"historical|archive|prior|이전|과거", prior.read_text(encoding="utf-8")[:700], re.I):
        warnings.append("PRIOR_CONTENT_SOURCES.md needs a clear historical label; its old template/content descriptions differ from this build.")
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_path": base,
        "output": str(output),
        "html_pages": len(documents),
        "rendered_publications": len(paper_nodes),
        "publication_source": publication_source,
        "source_publications": len(publication_records),
        "publication_year_groups": expected_order,
        "undated_publications": undated_count,
        "publication_types": sorted(known_types),
        "source_people": len(people_records),
        "rendered_people": len(people_nodes),
        "people_categories": dict(people_categories),
        "people_profile_pages": sum(person.get("category") != "alumni" for person in people_records),
        "research_topics": len(content["research"]),
        "research_assignments": sum(len(area.get("participants", [])) for area in content["research"]),
        "project_detail_pages": sum(f"projects/{identifier}/index.html" in found_pages for identifier in project_ids),
        "source_projects": len(project_records),
        "rendered_projects": len(project_nodes),
        "checks": dict(counts),
        "pi_portrait_valid_png": portrait_valid,
        "original_css_byte_identical": css_identical,
        "original_css_sha256": css_hash,
        "reference_commit": REFERENCE_COMMIT,
        "original_lab_identity_allowed_only_on_credits": True,
        "documentation_review": "Current CONTENT_SOURCES.md identifies the retained template and content sources. People data and portraits are supplied by the attached CORA repository; names, membership categories, and profile facts are not inferred.",
        "limits": ["External link availability and factual claims are not reverified by this script.", "Browser interactions and GitHub Actions execution require separate validation."],
        "warnings": warnings,
        "errors": errors,
        "passed": not errors,
    }
    report = Path(args.report).resolve()
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
