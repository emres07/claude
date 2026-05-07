package com.example.calendarapp.controller;

import com.example.calendarapp.entity.CompletionRecord;
import com.example.calendarapp.service.CompletionRecordService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/completionrecord")
@RequiredArgsConstructor
@Slf4j
public class CompletionRecordController {

    private final CompletionRecordService service;

    @PostMapping
    public ResponseEntity<CompletionRecord> create(@RequestBody CompletionRecord entity) {
        log.info("POST /api/v1/completionrecord - Creating new CompletionRecord");
        try {
            CompletionRecord created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<CompletionRecord>> getAll() {
        log.info("GET /api/v1/completionrecord - Fetching all CompletionRecord");
        List<CompletionRecord> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<CompletionRecord> getById(@PathVariable Long id) {
        log.info("GET /api/v1/completionrecord/{} - Fetching CompletionRecord", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("CompletionRecord not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<CompletionRecord> update(
            @PathVariable Long id,
            @RequestBody CompletionRecord entity) {
        log.info("PUT /api/v1/completionrecord/{} - Updating CompletionRecord", id);
        try {
            CompletionRecord updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/completionrecord/{} - Deleting CompletionRecord", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }