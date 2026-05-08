package com.example.todolistapp.controller;

import com.example.todolistapp.entity.TimeSlot;
import com.example.todolistapp.service.TimeSlotService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/timeslot")
@RequiredArgsConstructor
@Slf4j
public class TimeSlotController {

    private final TimeSlotService service;

    @PostMapping
    public ResponseEntity<TimeSlot> create(@RequestBody TimeSlot entity) {
        log.info("POST /api/v1/timeslot - Creating new TimeSlot");
        try {
            TimeSlot created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<TimeSlot>> getAll() {
        log.info("GET /api/v1/timeslot - Fetching all TimeSlot");
        List<TimeSlot> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TimeSlot> getById(@PathVariable Long id) {
        log.info("GET /api/v1/timeslot/{} - Fetching TimeSlot", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("TimeSlot not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<TimeSlot> update(
            @PathVariable Long id,
            @RequestBody TimeSlot entity) {
        log.info("PUT /api/v1/timeslot/{} - Updating TimeSlot", id);
        try {
            TimeSlot updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/timeslot/{} - Deleting TimeSlot", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }