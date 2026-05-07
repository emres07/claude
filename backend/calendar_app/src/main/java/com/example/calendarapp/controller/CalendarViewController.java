package com.example.calendarapp.controller;

import com.example.calendarapp.entity.CalendarView;
import com.example.calendarapp.service.CalendarViewService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/calendarview")
@RequiredArgsConstructor
@Slf4j
public class CalendarViewController {

    private final CalendarViewService service;

    @PostMapping
    public ResponseEntity<CalendarView> create(@RequestBody CalendarView entity) {
        log.info("POST /api/v1/calendarview - Creating new CalendarView");
        try {
            CalendarView created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<CalendarView>> getAll() {
        log.info("GET /api/v1/calendarview - Fetching all CalendarView");
        List<CalendarView> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<CalendarView> getById(@PathVariable Long id) {
        log.info("GET /api/v1/calendarview/{} - Fetching CalendarView", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("CalendarView not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<CalendarView> update(
            @PathVariable Long id,
            @RequestBody CalendarView entity) {
        log.info("PUT /api/v1/calendarview/{} - Updating CalendarView", id);
        try {
            CalendarView updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/calendarview/{} - Deleting CalendarView", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }