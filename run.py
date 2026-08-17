import json
import logging
from pathlib import Path
from src.discovery.extractors import EcosystemIngestor
from src.processing.resolution import DataProcessor
from src.mapping.relationships import RelationshipEngine
from src.utils.schemas import BaseEntity, SourceInfo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting AI Orbit Ingestion Pipeline...")
    ingestor = EcosystemIngestor()
    processor = DataProcessor()
    entities = []

    # 1. Seed Known AI Companies (Needed for relationship mapping)
    companies = [
        {"name": "OpenAI", "desc": "AI research and deployment company behind ChatGPT and GPT-4.", "url": "https://openai.com"},
        {"name": "Anthropic", "desc": "AI safety and research company behind Claude.", "url": "https://anthropic.com"},
        {"name": "Meta", "desc": "Tech company developing Llama open-weight models.", "url": "https://meta.com"},
        {"name": "Google", "desc": "Develops Gemini and AI technology platforms.", "url": "https://google.com"},
        {"name": "Hugging Face", "desc": "Platform for sharing AI models, datasets, and apps.", "url": "https://huggingface.co"}
    ]
    for comp in companies:
        entities.append(BaseEntity(
            entity_type="Companies",
            name=comp["name"],
            description=comp["desc"],
            url=comp["url"],
            categories=["AI Research"],
            source=SourceInfo(name="Official Site", url=comp["url"]),
            metadata={"founding_year": 2015, "industry_sector": "AI Research", "headquarters": "USA"}
        ))

    # 2. Ingest GitHub Repositories (~100 items)
    logging.info("Fetching GitHub Repositories...")
    for repo in ingestor.fetch_github_repos(query="topic:ai", limit=100):
        entities.append(BaseEntity(
            entity_type="Repositories",
            name=processor.resolve_entity_name(repo["name"]),
            description=processor.sanitize_text(repo.get("description", "")),
            url=processor.normalize_url(repo["html_url"]),
            categories=[repo.get("language") or "Python"],
            source=SourceInfo(name="GitHub API", url="https://api.github.com"),
            metadata={"stars": repo.get("stargazers_count", 0), "provider": repo.get("owner", {}).get("login", "")}
        ))

    # 3. Ingest MCP Servers (~50 items)
    logging.info("Fetching MCP Servers...")
    for mcp in ingestor.fetch_mcp_servers(limit=50):
        entities.append(BaseEntity(
            entity_type="MCP",
            name=processor.resolve_entity_name(mcp["name"]),
            description=processor.sanitize_text(mcp.get("description", "")),
            url=processor.normalize_url(mcp["html_url"]),
            categories=["MCP Server"],
            source=SourceInfo(name="GitHub MCP API", url="https://api.github.com"),
            metadata={"integrates_with": "GitHub", "runtime_requirements": "Node/Python"}
        ))

    # 4. Ingest Hugging Face Models (~80 items)
    logging.info("Fetching Hugging Face Models...")
    for model in ingestor.fetch_huggingface_models(limit=80):
        model_id = model.get("id", "unknown")
        provider = model_id.split("/")[0] if "/" in model_id else "Community"
        entities.append(BaseEntity(
            entity_type="Models",
            name=processor.resolve_entity_name(model_id),
            description=f"Hugging Face model {model_id}",
            url=f"https://huggingface.co/{model_id}",
            categories=model.get("tags", [])[:3],
            source=SourceInfo(name="Hugging Face API", url="https://huggingface.co"),
            metadata={"license": "apache-2.0", "modalities": ["text-generation"], "provider": provider}
        ))

    # 5. Ingest News/RSS (~50 items)
    logging.info("Fetching AI News RSS Feeds...")
    for article in ingestor.fetch_rss_news()[:50]:
        entities.append(BaseEntity(
            entity_type="News",
            name=processor.resolve_entity_name(article.get("title", "AI Announcement")),
            description=processor.sanitize_text(article.get("summary", "")),
            url=processor.normalize_url(article.get("link", "")),
            categories=["Industry News"],
            source=SourceInfo(name="TechCrunch AI RSS", url="https://techcrunch.com"),
            metadata={}
        ))

    # 6. Extract Ecosystem Relationships
    logging.info("Building cross-entity relationships...")
    relationships = RelationshipEngine.build_relationships(entities)

    # 7. Export Data
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "entities.json", "w", encoding="utf-8") as f:
        json.dump([e.model_dump() for e in entities], f, indent=2)

    with open(output_dir / "relationships.json", "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in relationships], f, indent=2)

    logging.info(f"Pipeline complete: Exported {len(entities)} entities and {len(relationships)} relationships to 'data/'.")

if __name__ == "__main__":
    main()