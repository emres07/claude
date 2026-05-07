package com.example.calendarapp.controller;

import com.example.calendarapp.entity.MeetingNotes;
import com.example.calendarapp.service.MeetingNotesService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/meetingnotes")
@RequiredArgsConstructor
@Slf4j
public class MeetingNotesController {

    private final MeetingNotesService service;

    @PostMapping
    public ResponseEntity<MeetingNotes> create(@RequestBody MeetingNotes entity) {
        log.info("POST /api/v1/meetingnotes - Creating new MeetingNotes");
        try {
            MeetingNotes created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<MeetingNotes>> getAll() {
        log.info("GET /api/v1/meetingnotes - Fetching all MeetingNotes");
        List<MeetingNotes> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<MeetingNotes> getById(@PathVariable Long id) {
        log.info("GET /api/v1/meetingnotes/{} - Fetching MeetingNotes", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("MeetingNotes not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<MeetingNotes> update(
            @PathVariable Long id,
            @RequestBody MeetingNotes entity) {
        log.info("PUT /api/v1/meetingnotes/{} - Updating MeetingNotes", id);
        try {
            MeetingNotes updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/meetingnotes/{} - Deleting MeetingNotes", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }