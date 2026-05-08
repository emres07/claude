package com.example.todolistapp.service;

import com.example.todolistapp.entity.AuditLog;
import com.example.todolistapp.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuditLogService {

    private final AuditLogRepository repository;

    @Transactional
    public AuditLog create(AuditLog entity) {
        log.info("Creating new AuditLog: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<AuditLog> findById(Long id) {
        log.info("Finding AuditLog by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<AuditLog> findAll() {
        log.info("Fetching all AuditLog");
        return repository.findAll();
    }

    @Transactional
    public AuditLog update(Long id, AuditLog entity) {
        log.info("Updating AuditLog with id: {}", id);
        return repository.findById(id)
            .map(existing -> {
                if (entity.getEntitytype() != null) {
                    existing.setEntitytype(entity.getEntitytype());
                }
                if (entity.getEntityid() != null) {
                    existing.setEntityid(entity.getEntityid());
                }
                if (entity.getOperation() != null) {
                    existing.setOperation(entity.getOperation());
                }
                if (entity.getChanges() != null) {
                    existing.setChanges(entity.getChanges());
                }
                if (entity.getUserid() != null) {
                    existing.setUserid(entity.getUserid());
                }
                return repository.save(existing);
            })
            .orElseThrow(() -> new IllegalArgumentException("AuditLog not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting AuditLog with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("AuditLog not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }