package com.example.todolistapp.controller;

import com.example.todolistapp.entity.ActivityReport;
import com.example.todolistapp.service.ActivityReportService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/activityreport")
@RequiredArgsConstructor
@Slf4j
public class ActivityReportController {

    private final ActivityReportService service;

    @PostMapping
    public ResponseEntity<ActivityReport> create(@RequestBody ActivityReport entity) {
        log.info("POST /api/v1/activityreport - Creating new ActivityReport");
        try {
            ActivityReport created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<ActivityReport>> getAll() {
        log.info("GET /api/v1/activityreport - Fetching all ActivityReport");
        List<ActivityReport> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ActivityReport> getById(@PathVariable Long id) {
        log.info("GET /api/v1/activityreport/{} - Fetching ActivityReport", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("ActivityReport not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<ActivityReport> update(
            @PathVariable Long id,
            @RequestBody ActivityReport entity) {
        log.info("PUT /api/v1/activityreport/{} - Updating ActivityReport", id);
        try {
            ActivityReport updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/activityreport/{} - Deleting ActivityReport", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }