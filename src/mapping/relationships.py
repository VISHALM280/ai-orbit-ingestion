from typing import List
from src.utils.schemas import BaseEntity, Relationship

class RelationshipEngine:
    @staticmethod
    def build_relationships(entities: List[BaseEntity]) -> List[Relationship]:
        relationships = []
        
        # Build lookup table of company entities by lowercased name
        company_lookup = {
            entity.name.lower(): entity.id 
            for entity in entities 
            if entity.entity_type == "Companies"
        }

        for entity in entities:
            if entity.entity_type == "Companies":
                continue

            # Extract fields to check for company references
            provider = str(entity.metadata.get("provider", "")).lower() if entity.metadata else ""
            name_lower = entity.name.lower()
            desc_lower = entity.description.lower()

            for company_name, company_id in company_lookup.items():
                # Link entities referencing a known company
                if company_name in provider or company_name in name_lower or company_name in desc_lower:
                    rel_type = "MAINTAINED_BY" if entity.entity_type in ["Models", "Repositories", "MCP"] else "MENTIONS"
                    relationships.append(
                        Relationship(
                            source_id=entity.id,
                            target_id=company_id,
                            relationship_type=rel_type
                        )
                    )

        return relationships