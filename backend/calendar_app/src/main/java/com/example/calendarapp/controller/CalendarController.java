package com.example.calendarapp.controller;

import com.example.calendarapp.entity.Calendar;
import com.example.calendarapp.service.CalendarService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/calendar")
@RequiredArgsConstructor
@Slf4j
public class CalendarController {

    private final CalendarService service;

    @PostMapping
    public ResponseEntity<Calendar> create(@RequestBody Calendar entity) {
        log.info("POST /api/v1/calendar - Creating new Calendar");
        try {
            Calendar created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Calendar>> getAll() {
        log.info("GET /api/v1/calendar - Fetching all Calendar");
        List<Calendar> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Calendar> getById(@PathVariable Long id) {
        log.info("GET /api/v1/calendar/{} - Fetching Calendar", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("Calendar not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<Calendar> update(
            @PathVariable Long id,
            @RequestBody Calendar entity) {
        log.info("PUT /api/v1/calendar/{} - Updating Calendar", id);
        try {
            Calendar updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/calendar/{} - Deleting Calendar", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }