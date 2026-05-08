package com.example.todolistapp.controller;

import com.example.todolistapp.entity.Token;
import com.example.todolistapp.service.TokenService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/v1/token")
@RequiredArgsConstructor
@Slf4j
public class TokenController {

    private final TokenService service;

    @PostMapping
    public ResponseEntity<Token> create(@RequestBody Token entity) {
        log.info("POST /api/v1/token - Creating new Token");
        try {
            Token created = service.create(entity);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        } catch (IllegalArgumentException e) {
            log.warn("Validation error: {}", e.getMessage());
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping
    public ResponseEntity<List<Token>> getAll() {
        log.info("GET /api/v1/token - Fetching all Token");
        List<Token> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Token> getById(@PathVariable Long id) {
        log.info("GET /api/v1/token/{} - Fetching Token", id);
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> {
                log.warn("Token not found with id: {}", id);
                return ResponseEntity.notFound().build();
            });
    }

    @PutMapping("/{id}")
    public ResponseEntity<Token> update(
            @PathVariable Long id,
            @RequestBody Token entity) {
        log.info("PUT /api/v1/token/{} - Updating Token", id);
        try {
            Token updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (IllegalArgumentException e) {
            log.warn("Update failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("DELETE /api/v1/token/{} - Deleting Token", id);
        try {
            service.delete(id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException e) {
            log.warn("Delete failed: {}", e.getMessage());
            return ResponseEntity.notFound().build();
        }
    }

    }