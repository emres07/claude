package com.example.audit.controller;

import com.example.audit.entity.Audit;
import com.example.audit.service.AuditService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/v1/audit")
@RequiredArgsConstructor
public class AuditController {

    private final AuditService auditService;

    @GetMapping
    public ResponseEntity<List<Audit>> getAll() {
        List<Audit> items = auditService.getAll();
        return ResponseEntity.ok(items);
    }

    @GetMapping("/{auditId}")
    public ResponseEntity<Audit> getById(@PathVariable Long auditId) {
        Optional<Audit> item = auditService.getById(auditId);
        return item.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Audit> create(@RequestBody Audit audit) {
        Audit created = auditService.create(audit);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{auditId}")
    public ResponseEntity<Audit> update(@PathVariable Long auditId,
                                                 @RequestBody Audit audit) {
        Audit updated = auditService.update(auditId, audit);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{auditId}")
    public ResponseEntity<Void> delete(@PathVariable Long auditId) {
        auditService.delete(auditId);
        return ResponseEntity.noContent().build();
    }
}
