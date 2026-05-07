package com.example.calendarapp.controller;

import com.example.calendarapp.entity.Meeting;
import com.example.calendarapp.service.MeetingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/meeting")
@RequiredArgsConstructor
@Slf4j
public class MeetingController {

    private final MeetingService service;

    @PostMapping
    public ResponseEntity<Meeting> create(@RequestBody Meeting entity) {
        log.info("POST /api/v1/meeting - Creating new Meeting");
        try {
            Meeting created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Meeting>> getAll() {
        log.info("GET /api/v1/meeting - Fetching all Meeting");
        List<Meeting> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Meeting> getById(@PathVariable Long id) {
        log.info("GET /api/v1/meeting/{} - Fetching Meeting", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("Meeting not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<Meeting> update(
            @PathVariable Long id,
            @RequestBody Meeting entity) {
        log.info("PUT /api/v1/meeting/{} - Updating Meeting", id);
        try {
            Meeting updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/meeting/{} - Deleting Meeting", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }