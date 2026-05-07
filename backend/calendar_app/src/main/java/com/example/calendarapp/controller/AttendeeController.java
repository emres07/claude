package com.example.calendarapp.controller;

import com.example.calendarapp.entity.Attendee;
import com.example.calendarapp.service.AttendeeService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/attendee")
@RequiredArgsConstructor
@Slf4j
public class AttendeeController {

    private final AttendeeService service;

    @PostMapping
    public ResponseEntity<Attendee> create(@RequestBody Attendee entity) {
        log.info("POST /api/v1/attendee - Creating new Attendee");
        try {
            Attendee created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Attendee>> getAll() {
        log.info("GET /api/v1/attendee - Fetching all Attendee");
        List<Attendee> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Attendee> getById(@PathVariable Long id) {
        log.info("GET /api/v1/attendee/{} - Fetching Attendee", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("Attendee not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<Attendee> update(
            @PathVariable Long id,
            @RequestBody Attendee entity) {
        log.info("PUT /api/v1/attendee/{} - Updating Attendee", id);
        try {
            Attendee updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/attendee/{} - Deleting Attendee", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }