package com.example.calendarapp.controller;

import com.example.calendarapp.entity.AuditLog;
import com.example.calendarapp.service.AuditLogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/auditlog")
@RequiredArgsConstructor
@Slf4j
public class AuditLogController {

    private final AuditLogService service;

    @PostMapping
    public ResponseEntity<AuditLog> create(@RequestBody AuditLog entity) {
        log.info("POST /api/v1/auditlog - Creating new AuditLog");
        try {
            AuditLog created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<AuditLog>> getAll() {
        log.info("GET /api/v1/auditlog - Fetching all AuditLog");
        List<AuditLog> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<AuditLog> getById(@PathVariable Long id) {
        log.info("GET /api/v1/auditlog/{} - Fetching AuditLog", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("AuditLog not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<AuditLog> update(
            @PathVariable Long id,
            @RequestBody AuditLog entity) {
        log.info("PUT /api/v1/auditlog/{} - Updating AuditLog", id);
        try {
            AuditLog updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/auditlog/{} - Deleting AuditLog", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }