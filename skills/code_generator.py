"""
Dynamic Code Generator - Generates code based on subtask descriptions
Reads subtask specifications and creates implementation code on-the-fly
"""

import re
from pathlib import Path
from typing import Dict, List, Any


class DynamicCodeGenerator:
    """Generates code dynamically from subtask descriptions without static templates."""

    @staticmethod
    def parse_subtask(subtask_path: str) -> Dict[str, Any]:
        """Parse subtask MD file and extract specification."""
        if not Path(subtask_path).exists():
            return {}

        with open(subtask_path, 'r', encoding='utf-8') as f:
            content = f.read()

        spec = {
            "title": DynamicCodeGenerator._extract_value(content, "^# (.+)$"),
            "description": DynamicCodeGenerator._extract_value(content, "## Description\n(.+?)(?=\n##|$)"),
            "apis": DynamicCodeGenerator._extract_list(content, "## APIs to Implement"),
            "tables": DynamicCodeGenerator._extract_list(content, "## Database Schemas"),
            "components": DynamicCodeGenerator._extract_list(content, "## Components to Build"),
            "pages": DynamicCodeGenerator._extract_list(content, "## Pages to Create"),
        }
        return spec

    @staticmethod
    def _extract_value(content: str, pattern: str) -> str:
        """Extract single value from content using regex."""
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_list(content: str, header: str) -> List[str]:
        """Extract list items from section."""
        pattern = f"{header}\n(.+?)(?=\n##|$)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if not match:
            return []
        items = re.findall(r"^- (.+)$", match.group(1), re.MULTILINE)
        return [item.strip() for item in items]

    @staticmethod
    def generate_java_entity(spec: Dict[str, Any], entity_name: str = "Entity") -> str:
        """Generate Java JPA entity from description."""
        description = spec.get("description", "").lower()
        tables = spec.get("tables", [])

        # Extract table name or use default
        table_name = tables[0].lower().replace(" table", "").replace(" ", "_") if tables else "entity"

        # Determine entity fields based on description
        fields = []
        field_types = []

        if "user" in description or "email" in description:
            fields.extend(["id", "email", "name", "password_hash", "active", "created_at", "updated_at"])
            field_types = ["Long", "String", "String", "String", "Boolean", "LocalDateTime", "LocalDateTime"]
        elif "audit" in description:
            fields.extend(["id", "action", "entity", "entity_id", "user_id", "timestamp", "details"])
            field_types = ["Long", "String", "String", "Long", "String", "LocalDateTime", "String"]
        else:
            fields.extend(["id", "name", "description", "created_at", "updated_at"])
            field_types = ["Long", "String", "String", "LocalDateTime", "LocalDateTime"]

        # Generate field declarations
        field_declarations = "\n    ".join([
            f"private {field_types[i]} {fields[i]};"
            for i in range(len(fields))
        ])

        return f'''package com.example.calendarapp.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

/**
 * {entity_name} Entity
 * {spec.get('description', 'Entity')}
 */
@Entity
@Table(name = "{table_name}")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class {entity_name} {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    {field_declarations}

    @PrePersist
    protected void onCreate() {{
        if (this.created_at == null) {{
            this.created_at = LocalDateTime.now();
        }}
        if (this.updated_at == null) {{
            this.updated_at = LocalDateTime.now();
        }}
    }}

    @PreUpdate
    protected void onUpdate() {{
        this.updated_at = LocalDateTime.now();
    }}
}}
'''

    @staticmethod
    def generate_java_service(spec: Dict[str, Any], service_name: str = "Service") -> str:
        """Generate Java service from description."""
        description = spec.get("description", "")

        methods = []
        if "user" in description.lower():
            methods = ["register", "getById", "getByEmail", "update", "delete", "list"]
        elif "audit" in description.lower():
            methods = ["logAction", "getAuditLogs", "getByUser", "getByPeriod"]
        else:
            methods = ["create", "read", "update", "delete", "list"]

        method_declarations = "\n\n    ".join([
            f'''/**
     * {method} operation
     */
    public void {method}() {{
        // TODO: Implement {method}
    }}'''
            for method in methods
        ])

        return f'''package com.example.calendarapp.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {service_name}
 * {description}
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class {service_name} {{

    {method_declarations}
}}
'''

    @staticmethod
    def generate_java_controller(spec: Dict[str, Any], controller_name: str = "Controller") -> str:
        """Generate Java REST controller from description."""
        apis = spec.get("apis", [])
        description = spec.get("description", "")

        base_path = apis[0] if apis else "/api/v1/resource"

        endpoints = []
        if "user" in description.lower():
            endpoints = [
                ('POST', '/register', 'Register new user'),
                ('GET', '/{id}', 'Get user by ID'),
                ('GET', '', 'Get all users'),
                ('PUT', '/{id}', 'Update user'),
                ('DELETE', '/{id}', 'Delete user'),
            ]
        elif "audit" in description.lower():
            endpoints = [
                ('GET', '/logs', 'Get audit logs'),
                ('GET', '/by-user/{userId}', 'Get logs by user'),
                ('GET', '/by-entity/{entity}', 'Get logs by entity'),
            ]
        else:
            endpoints = [
                ('POST', '', 'Create resource'),
                ('GET', '/{id}', 'Get resource'),
                ('GET', '', 'List resources'),
                ('PUT', '/{id}', 'Update resource'),
                ('DELETE', '/{id}', 'Delete resource'),
            ]

        endpoint_methods = "\n\n    ".join([
            f'''/**
     * {ep[2]}
     * {ep[0]} {base_path}{ep[1]}
     */
    @{ep[0]}Mapping("{ep[1]}")
    public ResponseEntity<?> {ep[2].lower().replace(' ', '_')}() {{
        // TODO: Implement {ep[2]}
        return ResponseEntity.ok().build();
    }}'''
            for ep in endpoints
        ])

        return f'''package com.example.calendarapp.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/**
 * {controller_name}
 * {description}
 */
@RestController
@RequestMapping("{base_path}")
@RequiredArgsConstructor
@Slf4j
public class {controller_name} {{

    {endpoint_methods}
}}
'''

    @staticmethod
    def generate_react_component(spec: Dict[str, Any], component_name: str = "Component") -> str:
        """Generate React component from description."""
        description = spec.get("description", "").lower()

        if "login" in description:
            return f'''import React, {{ useState }} from 'react';

interface {component_name}Props {{
  onSuccess?: () => void;
}}

const {component_name}: React.FC<{component_name}Props> = ({{ onSuccess }}) => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setLoading(true);
    try {{
      // TODO: Implement {component_name} logic
      onSuccess?.();
    }} catch (err: any) {{
      setError(err.message || 'Error occurred');
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="form-container">
      <h2>{component_name}</h2>
      {{error && <div className="error">{{error}}</div>}}
      <form onSubmit={{handleSubmit}}>
        {{/* TODO: Add form fields */}}
        <button type="submit" disabled={{loading}}>
          {{loading ? 'Loading...' : 'Submit'}}
        </button>
      </form>
    </div>
  );
}};

export default {component_name};
'''
        else:
            return f'''import React, {{ useEffect, useState }} from 'react';

interface {component_name}Props {{
  // TODO: Add props
}}

const {component_name}: React.FC<{component_name}Props> = (props) => {{
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {{
    // TODO: Fetch data
  }}, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">{{error}}</div>;

  return (
    <div className="component">
      <h2>{component_name}</h2>
      {{/* TODO: Render {component_name} content */}}
    </div>
  );
}};

export default {component_name};
'''

    @staticmethod
    def generate_sql_migration(spec: Dict[str, Any], version: int, table_name: str = "table") -> str:
        """Generate SQL migration from description."""
        description = spec.get("description", "").lower()

        if "user" in description:
            return f'''-- V{version:03d}_create_users_table.sql
-- {spec.get('description', 'Users table')}

CREATE TABLE {table_name} (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR2(255) NOT NULL UNIQUE,
    name VARCHAR2(100) NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    active NUMBER(1) DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_{table_name}_email ON {table_name}(email);
CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at);

COMMIT;
'''
        elif "audit" in description:
            return f'''-- V{version:03d}_create_audit_logs_table.sql
-- {spec.get('description', 'Audit logs table')}

CREATE TABLE {table_name} (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    action VARCHAR2(50) NOT NULL,
    entity VARCHAR2(100) NOT NULL,
    entity_id NUMBER(19),
    user_id VARCHAR2(255),
    details CLOB,
    timestamp TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_{table_name}_entity ON {table_name}(entity);
CREATE INDEX idx_{table_name}_user ON {table_name}(user_id);
CREATE INDEX idx_{table_name}_time ON {table_name}(timestamp);

COMMIT;
'''
        else:
            return f'''-- V{version:03d}_create_{table_name}_table.sql
-- {spec.get('description', 'Table creation')}

CREATE TABLE {table_name} (
    id NUMBER(19) PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR2(255) NOT NULL,
    description CLOB,
    created_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT SYSTIMESTAMP
);

CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at);

COMMIT;
'''
