# Backend Code Templates - Jinja2 Format

## JPA Entity Template

<!-- jpa_entity -->
```java
package {{ package }}.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

/**
 * {{ entity_name }} Entity
 * {% if description -%}
 * {{ description }}
 * {% endif -%}
 */
@Entity
@Table(name = "{{ table_name }}")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class {{ entity_name }} {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    {% if fields -%}
    {% for field in fields -%}
    @Column(nullable = {{ field.nullable | lower }})
    private {{ field.type }} {{ field.name }};

    {% endfor %}
    {% else -%}
    @Column(nullable = false)
    private String name;

    private String description;
    {% endif -%}

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;
}
```
<!-- /jpa_entity -->

## JPA Repository Template

<!-- jpa_repository -->
```java
package {{ package }}.repository;

import {{ package }}.entity.{{ entity_name }};
import org.springframework.data.jpa.repository.JpaRepository;
{% if custom_queries -%}
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
{% endif -%}
import org.springframework.stereotype.Repository;

@Repository
public interface {{ entity_name }}Repository extends JpaRepository<{{ entity_name }}, Long> {
    {% if custom_queries -%}
    {% for query in custom_queries -%}
    @Query("{{ query.jpql }}")
    {{ query.return_type }} {{ query.method_name }}({% for param in query.params %}@Param("{{ param.name }}") {{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %});

    {% endfor %}
    {% else -%}
    // Add custom queries here
    {% endif -%}
}
```
<!-- /jpa_repository -->

## Spring Service Template

<!-- spring_service -->
```java
package {{ package }}.service;

import {{ package }}.entity.{{ entity_name }};
import {{ package }}.repository.{{ entity_name }}Repository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class {{ entity_name }}Service {

    private final {{ entity_name }}Repository repository;

    public {{ entity_name }} save({{ entity_name }} entity) {
        log.info("Saving {{ entity_name }}: {}", entity.getId());
        return repository.save(entity);
    }

    public {{ entity_name }} findById(Long id) {
        log.info("Finding {{ entity_name }} by id: {}", id);
        return repository.findById(id).orElseThrow(() ->
            new IllegalArgumentException("{{ entity_name }} not found with id: " + id));
    }

    public List<{{ entity_name }}> findAll() {
        log.info("Finding all {{ entity_name }}");
        return repository.findAll();
    }

    public void delete(Long id) {
        log.info("Deleting {{ entity_name }} with id: {}", id);
        repository.deleteById(id);
    }

    {% if custom_methods -%}
    {% for method in custom_methods -%}
    public {{ method.return_type }} {{ method.name }}({% for param in method.params %}{{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {
        log.info("Executing {{ method.name }}");
        // TODO: Implement {{ method.name }}
        return null;
    }

    {% endfor %}
    {% endif -%}
}
```
<!-- /spring_service -->

## REST Controller Template

<!-- rest_controller -->
```java
package {{ package }}.controller;

import {{ package }}.entity.{{ entity_name }};
import {{ package }}.service.{{ entity_name }}Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/{{ endpoint_path | lower }}")
@RequiredArgsConstructor
@Slf4j
public class {{ entity_name }}Controller {

    private final {{ entity_name }}Service service;

    @PostMapping
    public ResponseEntity<{{ entity_name }}> create(@RequestBody {{ entity_name }} entity) {
        log.info("Creating new {{ entity_name }}");
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(service.save(entity));
    }

    @GetMapping("/{id}")
    public ResponseEntity<{{ entity_name }}> getById(@PathVariable Long id) {
        log.info("Getting {{ entity_name }} by id: {}", id);
        return ResponseEntity.ok(service.findById(id));
    }

    @GetMapping
    public ResponseEntity<List<{{ entity_name }}>> getAll() {
        log.info("Getting all {{ entity_name }}");
        return ResponseEntity.ok(service.findAll());
    }

    @PutMapping("/{id}")
    public ResponseEntity<{{ entity_name }}> update(@PathVariable Long id, @RequestBody {{ entity_name }} entity) {
        log.info("Updating {{ entity_name }} with id: {}", id);
        entity.setId(id);
        return ResponseEntity.ok(service.save(entity));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("Deleting {{ entity_name }} with id: {}", id);
        service.delete(id);
        return ResponseEntity.noContent().build();
    }

    {% if custom_endpoints -%}
    {% for endpoint in custom_endpoints -%}
    @{{ endpoint.method }}("{{ endpoint.path }}")
    public ResponseEntity<{{ endpoint.return_type }}> {{ endpoint.name }}({% for param in endpoint.params %}@{{ param.annotation }} {{ param.type }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {
        log.info("Executing {{ endpoint.name }}");
        // TODO: Implement {{ endpoint.name }}
        return ResponseEntity.ok(null);
    }

    {% endfor %}
    {% endif -%}
}
```
<!-- /rest_controller -->

## POM XML Template

<!-- pom_xml -->
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <groupId>{{ group_id | default('com.example') }}</groupId>
    <artifactId>{{ artifact_id }}</artifactId>
    <version>{{ version | default('1.0.0') }}</version>
    <name>{{ project_name }}</name>

    <properties>
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        {% if add_security -%}
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        {% endif -%}
        <dependency>
            <groupId>com.oracle.database.jdbc</groupId>
            <artifactId>ojdbc11</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.2.0</version>
        </dependency>
        {% if additional_dependencies -%}
        {% for dep in additional_dependencies -%}
        <dependency>
            <groupId>{{ dep.group_id }}</groupId>
            <artifactId>{{ dep.artifact_id }}</artifactId>
            {% if dep.version -%}
            <version>{{ dep.version }}</version>
            {% endif -%}
        </dependency>
        {% endfor %}
        {% endif -%}
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```
<!-- /pom_xml -->

## Application YML Template

<!-- application_yml -->
```yaml
spring:
  application:
    name: {{ project_name | lower | replace(' ', '-') }}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        use_sql_comments: true
  datasource:
    url: {{ db_url | default('jdbc:oracle:thin:@localhost:1521:xe') }}
    username: {{ db_user | default('calendar_app') }}
    password: {{ db_password | default('welcome123') }}
    driver-class-name: oracle.jdbc.OracleDriver

server:
  port: {{ server_port | default(8080) }}
  servlet:
    context-path: /api/v1

springdoc:
  swagger-ui:
    path: /swagger-ui.html
  api-docs:
    path: /v3/api-docs

logging:
  level:
    root: INFO
    {{ package }}: DEBUG
```
<!-- /application_yml -->
