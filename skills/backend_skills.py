"""Backend Skills - Java, Spring Boot, Hibernate, Maven, Clean Code."""


class BackendSkill:
    """Skills for backend development with Java, Spring Boot, Hibernate, Maven."""

    name = "backend"
    description = "Backend with Java, Spring Boot, Hibernate, Maven & Clean Code"

    FRAMEWORKS = {
        "spring_boot": "Spring Boot 3.x",
        "spring_data_jpa": "Spring Data JPA with Hibernate",
        "spring_security": "Spring Security",
    }

    TOOLS = ["Maven", "Lombok", "Mapstruct", "Validation", "AOP"]

    @staticmethod
    def generate_pom_xml(project_name: str, version: str = "1.0.0") -> str:
        """Generate Maven pom.xml for Spring Boot project."""
        group_id = project_name.lower().replace(' ', '-').replace('_', '.')
        artifact_id = project_name.lower().replace(' ', '-').replace('_', '-')
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>{version}</version>
    <packaging>jar</packaging>

    <name>{project_name}</name>
    <description>Spring Boot application</description>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>com.oracle.database.jdbc</groupId>
            <artifactId>ojdbc11</artifactId>
            <version>23.4.0.24.05</version>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- MapStruct -->
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>1.5.5.Final</version>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${{'$'}}{lombok.version}</version>
                        </path>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>1.5.5.Final</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
"""

    @staticmethod
    def generate_entity_template(entity_name: str, properties: list = None) -> str:
        """Generate JPA Entity with best practices."""
        if properties is None:
            properties = ["name", "description", "createdAt", "updatedAt"]

        pascal_case = ''.join(word.title() for word in entity_name.split('_'))
        table_name = entity_name.lower()

        props_code = """
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
"""

        for prop in properties:
            if prop not in ["id", "createdAt", "updatedAt"]:
                props_code += f"""
    @Column
    private String {prop};
"""

        return f"""package com.example.{table_name}.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "{table_name}")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class {pascal_case} {{
{props_code}

    @PrePersist
    protected void onCreate() {{
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }}

    @PreUpdate
    protected void onUpdate() {{
        updatedAt = LocalDateTime.now();
    }}
}}
"""

    @staticmethod
    def generate_repository_template(entity_name: str) -> str:
        """Generate Spring Data JPA Repository."""
        pascal_case = ''.join(word.title() for word in entity_name.split('_'))
        return f"""package com.example.{entity_name.lower()}.repository;

import com.example.{entity_name.lower()}.entity.{pascal_case};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface {pascal_case}Repository extends JpaRepository<{pascal_case}, Long> {{

    Optional<{pascal_case}> findById(Long id);

    List<{pascal_case}> findAll();

    // Add custom queries here
    @Query("SELECT e FROM {pascal_case} e WHERE e.name = :name")
    Optional<{pascal_case}> findByName(String name);
}}
"""

    @staticmethod
    def generate_service_template(entity_name: str) -> str:
        """Generate Service class with business logic."""
        pascal_case = ''.join(word.title() for word in entity_name.split('_'))
        entity_var = entity_name[0].lower() + entity_name[1:] if entity_name else 'entity'

        return f"""package com.example.{entity_name.lower()}.service;

import com.example.{entity_name.lower()}.entity.{pascal_case};
import com.example.{entity_name.lower()}.repository.{pascal_case}Repository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class {pascal_case}Service {{

    private final {pascal_case}Repository {entity_var}Repository;

    public List<{pascal_case}> getAll() {{
        log.info("Fetching all {pascal_case} records");
        return {entity_var}Repository.findAll();
    }}

    public Optional<{pascal_case}> getById(Long id) {{
        log.info("Fetching {pascal_case} by id: {{}}", id);
        return {entity_var}Repository.findById(id);
    }}

    @Transactional
    public {pascal_case} create({pascal_case} {entity_var}) {{
        log.info("Creating new {pascal_case}");
        return {entity_var}Repository.save({entity_var});
    }}

    @Transactional
    public {pascal_case} update(Long id, {pascal_case} {entity_var}) {{
        log.info("Updating {pascal_case} with id: {{}}", id);
        {entity_var}.setId(id);
        return {entity_var}Repository.save({entity_var});
    }}

    @Transactional
    public void delete(Long id) {{
        log.info("Deleting {pascal_case} with id: {{}}", id);
        {entity_var}Repository.deleteById(id);
    }}
}}
"""

    @staticmethod
    def generate_controller_template(entity_name: str) -> str:
        """Generate REST Controller with clean code."""
        pascal_case = ''.join(word.title() for word in entity_name.split('_'))
        entity_var = entity_name[0].lower() + entity_name[1:] if entity_name else 'entity'
        route = entity_name.lower().replace('_', '-')

        return f"""package com.example.{entity_name.lower()}.controller;

import com.example.{entity_name.lower()}.entity.{pascal_case};
import com.example.{entity_name.lower()}.service.{pascal_case}Service;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/v1/{route}")
@RequiredArgsConstructor
public class {pascal_case}Controller {{

    private final {pascal_case}Service {entity_var}Service;

    @GetMapping
    public ResponseEntity<List<{pascal_case}>> getAll() {{
        List<{pascal_case}> items = {entity_var}Service.getAll();
        return ResponseEntity.ok(items);
    }}

    @GetMapping("/{{{entity_var}Id}}")
    public ResponseEntity<{pascal_case}> getById(@PathVariable Long {entity_var}Id) {{
        Optional<{pascal_case}> item = {entity_var}Service.getById({entity_var}Id);
        return item.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }}

    @PostMapping
    public ResponseEntity<{pascal_case}> create(@RequestBody {pascal_case} {entity_var}) {{
        {pascal_case} created = {entity_var}Service.create({entity_var});
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }}

    @PutMapping("/{{{entity_var}Id}}")
    public ResponseEntity<{pascal_case}> update(@PathVariable Long {entity_var}Id,
                                                 @RequestBody {pascal_case} {entity_var}) {{
        {pascal_case} updated = {entity_var}Service.update({entity_var}Id, {entity_var});
        return ResponseEntity.ok(updated);
    }}

    @DeleteMapping("/{{{entity_var}Id}}")
    public ResponseEntity<Void> delete(@PathVariable Long {entity_var}Id) {{
        {entity_var}Service.delete({entity_var}Id);
        return ResponseEntity.noContent().build();
    }}
}}
"""

    @staticmethod
    def generate_application_yml(db_url: str = "jdbc:oracle:thin:@localhost:1521:xe") -> str:
        """Generate application.yml configuration."""
        return f"""spring:
  application:
    name: backend-application

  datasource:
    url: {db_url}
    username: ${{DB_USER:todo}}
    password: ${{DB_PASSWORD:welcome123}}
    driver-class-name: oracle.jdbc.OracleDriver

  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.dialect.OracleDialect
        jdbc:
          batch_size: 10
        order_inserts: true
        order_updates: true
    show-sql: false
    open-in-view: false

  security:
    user:
      name: admin
      password: admin

server:
  port: 8080
  servlet:
    context-path: /api

logging:
  level:
    root: INFO
    com.example: DEBUG
  pattern:
    console: "%d{{yyyy-MM-dd HH:mm:ss}} - %msg%n"
"""

    @staticmethod
    def get_clean_code_principles() -> list:
        """Get clean code best practices."""
        return [
            "Single Responsibility Principle (SRP)",
            "Open/Closed Principle",
            "Liskov Substitution Principle",
            "Interface Segregation Principle",
            "Dependency Inversion Principle",
            "DRY (Don't Repeat Yourself)",
            "YAGNI (You Aren't Gonna Need It)",
            "KISS (Keep It Simple, Stupid)",
        ]

    @staticmethod
    def generate_pom_maven_setup() -> str:
        """Generate setup script for Maven."""
        return """#!/bin/bash

echo "🚀 Backend Maven Setup Script"
echo "============================="

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | head -1)
echo "✓ Java version: $JAVA_VERSION"

# Check Maven
MVN_VERSION=$(mvn -v | head -1)
echo "✓ Maven version: $MVN_VERSION"

# Install dependencies
echo ""
echo "📦 Installing Maven dependencies..."
mvn clean install

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p src/main/java/com/example
mkdir -p src/main/resources
mkdir -p src/test/java/com/example
mkdir -p target

echo "✓ Directories created"

# Initialize git
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial backend setup"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "  mvn clean compile - Compile the project"
echo "  mvn spring-boot:run - Run the application"
echo "  mvn test          - Run tests"
"""
