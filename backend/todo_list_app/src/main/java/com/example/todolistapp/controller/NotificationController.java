package com.example.todolistapp.controller;

import com.example.todolistapp.entity.Notification;
import com.example.todolistapp.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/notification")
@RequiredArgsConstructor
@Slf4j
public class NotificationController {

    private final NotificationService service;

    @PostMapping
    public ResponseEntity<Notification> create(@RequestBody Notification entity) {
        log.info("POST /api/v1/notification - Creating new Notification");
        try {
            Notification created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Notification>> getAll() {
        log.info("GET /api/v1/notification - Fetching all Notification");
        List<Notification> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Notification> getById(@PathVariable Long id) {
        log.info("GET /api/v1/notification/{} - Fetching Notification", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("Notification not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<Notification> update(
            @PathVariable Long id,
            @RequestBody Notification entity) {
        log.info("PUT /api/v1/notification/{} - Updating Notification", id);
        try {
            Notification updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/notification/{} - Deleting Notification", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }