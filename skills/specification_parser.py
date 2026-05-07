"""Specification Parser - Extracts fields, columns, and requirements from markdown specs."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class SpecificationParser:
    """Parse subtask markdown specifications to extract implementation requirements."""

    @staticmethod
    def extract_api_endpoints(content: str) -> List[str]:
        """Extract API endpoints from specification."""
        endpoints = []
        # Look for /api/v1/... patterns
        matches = re.findall(r'/api/v\d+/\w+', content)
        endpoints.extend(matches)
        return list(set(endpoints))

    @staticmethod
    def extract_data_entities(content: str) -> List[str]:
        """Extract data entities to handle."""
        entities = []
        # Look for "Data entities to handle:" or "data_entities"
        match = re.search(r'[Dd]ata entities?.*?:([^\n]+)', content)
        if match:
            entity_str = match.group(1)
            entities = [e.strip() for e in entity_str.split(',')]
        return entities

    @staticmethod
    def extract_workflow_features(content: str) -> List[str]:
        """Extract features from workflow."""
        features = []
        # Look for "Features to implement:" or "features:"
        match = re.search(r'[Ff]eatures?.*?:([^\n]+)', content)
        if match:
            feature_str = match.group(1)
            features = [f.strip() for f in feature_str.split(',')]
        return features

    @staticmethod
    def extract_workflow_steps(content: str) -> List[str]:
        """Extract workflow steps."""
        steps = []
        # Look for "Workflow Steps:" followed by numbered items
        match = re.search(r'[Ww]orkflow [Ss]teps?:(.+?)(?=##|\Z)', content, re.DOTALL)
        if match:
            steps_text = match.group(1)
            # Find numbered lines
            step_matches = re.findall(r'\d+\.\s*(.+?)(?=\n\d+\.|\Z)', steps_text)
            steps = [s.strip() for s in step_matches]
        return steps

    @staticmethod
    def extract_technical_requirements(content: str) -> List[str]:
        """Extract technical requirements from specification."""
        requirements = []
        # Look for "## Technical Requirements" section
        match = re.search(r'## Technical Requirements(.+?)(?=##|\Z)', content, re.DOTALL)
        if match:
            req_text = match.group(1)
            # Find bullet points
            req_matches = re.findall(r'-\s*(.+)', req_text)
            requirements = [r.strip() for r in req_matches]
        return requirements

    @staticmethod
    def infer_form_fields(entity_name: str, features: List[str]) -> List[Dict[str, Any]]:
        """Infer form fields based on entity and features."""
        fields = []

        # Common field mappings by entity type
        field_templates = {
            'Meeting': [
                {'name': 'title', 'label': 'Meeting Title', 'type': 'text', 'required': True, 'input_type': 'text'},
                {'name': 'description', 'label': 'Description', 'type': 'textarea', 'required': False},
                {'name': 'startTime', 'label': 'Start Time', 'type': 'datetime', 'required': True, 'input_type': 'datetime-local'},
                {'name': 'endTime', 'label': 'End Time', 'type': 'datetime', 'required': True, 'input_type': 'datetime-local'},
                {'name': 'location', 'label': 'Location', 'type': 'text', 'required': False, 'input_type': 'text'},
            ],
            'Calendar': [
                {'name': 'name', 'label': 'Calendar Name', 'type': 'text', 'required': True, 'input_type': 'text'},
                {'name': 'description', 'label': 'Description', 'type': 'textarea', 'required': False},
            ],
            'User': [
                {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True, 'input_type': 'email'},
                {'name': 'name', 'label': 'Full Name', 'type': 'text', 'required': True, 'input_type': 'text'},
                {'name': 'password', 'label': 'Password', 'type': 'password', 'required': True, 'input_type': 'password'},
            ],
            'AuditLog': [
                {'name': 'entityType', 'label': 'Entity Type', 'type': 'text', 'required': True, 'input_type': 'text'},
                {'name': 'operation', 'label': 'Operation', 'type': 'select', 'required': True},
                {'name': 'changes', 'label': 'Changes', 'type': 'textarea', 'required': False},
            ],
            'MeetingNotes': [
                {'name': 'content', 'label': 'Notes Content', 'type': 'textarea', 'required': True},
                {'name': 'summary', 'label': 'Summary', 'type': 'textarea', 'required': False},
            ]
        }

        if entity_name in field_templates:
            fields = field_templates[entity_name]
        else:
            # Generic fields for unknown entities
            fields = [
                {'name': 'name', 'label': 'Name', 'type': 'text', 'required': True, 'input_type': 'text'},
                {'name': 'description', 'label': 'Description', 'type': 'textarea', 'required': False},
            ]

        return fields

    @staticmethod
    def infer_table_columns(entity_name: str) -> List[Dict[str, str]]:
        """Infer table columns based on entity."""
        columns_templates = {
            'Meeting': [
                {'name': 'title', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
                {'name': 'description', 'oracle_type': 'CLOB', 'constraints': ''},
                {'name': 'start_time', 'oracle_type': 'TIMESTAMP', 'constraints': 'NOT NULL'},
                {'name': 'end_time', 'oracle_type': 'TIMESTAMP', 'constraints': 'NOT NULL'},
                {'name': 'location', 'oracle_type': 'VARCHAR2(255)', 'constraints': ''},
            ],
            'Calendar': [
                {'name': 'name', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
                {'name': 'description', 'oracle_type': 'CLOB', 'constraints': ''},
            ],
            'User': [
                {'name': 'email', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL UNIQUE'},
                {'name': 'name', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
                {'name': 'password_hash', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
            ],
            'AuditLog': [
                {'name': 'entity_type', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
                {'name': 'entity_id', 'oracle_type': 'NUMBER(19)', 'constraints': ''},
                {'name': 'operation', 'oracle_type': 'VARCHAR2(50)', 'constraints': 'NOT NULL'},
                {'name': 'changes', 'oracle_type': 'CLOB', 'constraints': ''},
                {'name': 'user_id', 'oracle_type': 'VARCHAR2(255)', 'constraints': ''},
            ],
            'MeetingNotes': [
                {'name': 'content', 'oracle_type': 'CLOB', 'constraints': 'NOT NULL'},
                {'name': 'summary', 'oracle_type': 'CLOB', 'constraints': ''},
            ]
        }

        table_name = entity_name.lower()
        if entity_name in columns_templates:
            columns = columns_templates[entity_name]
        else:
            # Generic columns
            columns = [
                {'name': 'name', 'oracle_type': 'VARCHAR2(255)', 'constraints': 'NOT NULL'},
                {'name': 'description', 'oracle_type': 'CLOB', 'constraints': ''},
            ]

        return columns

    @staticmethod
    def infer_entity_fields(entity_name: str) -> List[Dict[str, Any]]:
        """Infer JPA entity fields based on entity type."""
        fields_templates = {
            'Meeting': [
                {'name': 'title', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'description', 'type': 'String', 'nullable': True, 'validation': ''},
                {'name': 'startTime', 'type': 'LocalDateTime', 'nullable': False, 'validation': 'NotNull'},
                {'name': 'endTime', 'type': 'LocalDateTime', 'nullable': False, 'validation': 'NotNull'},
                {'name': 'location', 'type': 'String', 'nullable': True, 'validation': ''},
            ],
            'Calendar': [
                {'name': 'name', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'description', 'type': 'String', 'nullable': True, 'validation': ''},
            ],
            'User': [
                {'name': 'email', 'type': 'String', 'nullable': False, 'validation': 'Email'},
                {'name': 'name', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'passwordHash', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
            ],
            'AuditLog': [
                {'name': 'entityType', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'entityId', 'type': 'Long', 'nullable': True, 'validation': ''},
                {'name': 'operation', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'changes', 'type': 'String', 'nullable': True, 'validation': ''},
                {'name': 'userId', 'type': 'String', 'nullable': True, 'validation': ''},
            ],
            'MeetingNotes': [
                {'name': 'content', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'summary', 'type': 'String', 'nullable': True, 'validation': ''},
            ]
        }

        if entity_name in fields_templates:
            return fields_templates[entity_name]
        else:
            return [
                {'name': 'name', 'type': 'String', 'nullable': False, 'validation': 'NotBlank'},
                {'name': 'description', 'type': 'String', 'nullable': True, 'validation': ''},
            ]

    @staticmethod
    def parse_subtask_file(filepath: str) -> Dict[str, Any]:
        """Parse a subtask markdown file and extract all relevant information."""
        if not Path(filepath).exists():
            return {}

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            'title': SpecificationParser._extract_title(content),
            'description': SpecificationParser._extract_description(content),
            'api_endpoints': SpecificationParser.extract_api_endpoints(content),
            'data_entities': SpecificationParser.extract_data_entities(content),
            'workflow_features': SpecificationParser.extract_workflow_features(content),
            'workflow_steps': SpecificationParser.extract_workflow_steps(content),
            'technical_requirements': SpecificationParser.extract_technical_requirements(content),
        }

    @staticmethod
    def _extract_title(content: str) -> str:
        """Extract title from markdown."""
        match = re.search(r'#\s+(.+?)(?:\n|$)', content)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_description(content: str) -> str:
        """Extract description section."""
        match = re.search(r'## Description\n(.+?)(?=##|\Z)', content, re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def infer_list_display_fields(entity_name: str) -> List[Dict[str, str]]:
        """Infer which fields to display in list/table view."""
        display_templates = {
            'Meeting': [
                {'name': 'title', 'label': 'Title'},
                {'name': 'startTime', 'label': 'Start Time'},
                {'name': 'location', 'label': 'Location'},
            ],
            'Calendar': [
                {'name': 'name', 'label': 'Name'},
            ],
            'User': [
                {'name': 'email', 'label': 'Email'},
                {'name': 'name', 'label': 'Name'},
            ],
            'AuditLog': [
                {'name': 'entityType', 'label': 'Entity'},
                {'name': 'operation', 'label': 'Operation'},
                {'name': 'timestamp', 'label': 'Time'},
            ],
            'MeetingNotes': [
                {'name': 'summary', 'label': 'Summary'},
                {'name': 'createdAt', 'label': 'Created'},
            ]
        }

        if entity_name in display_templates:
            return display_templates[entity_name]
        else:
            return [
                {'name': 'name', 'label': 'Name'},
                {'name': 'createdAt', 'label': 'Created'},
            ]
