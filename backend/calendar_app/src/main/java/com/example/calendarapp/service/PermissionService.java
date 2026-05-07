package com.example.calendarapp.service;

import com.example.calendarapp.entity.Permission;
import com.example.calendarapp.repository.PermissionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class PermissionService {

    private final PermissionRepository repository;

    @Transactional
    public Permission create(Permission entity) {
        log.info("Creating new Permission: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Permission> findById(Long id) {
        log.info("Finding Permission by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Permission> findAll() {
        log.info("Fetching all Permission");
        return repository.findAll();
    }

    @Transactional
    public Permission update(Long id, Permission entity) {
        log.info("Updating Permission with id: {}", id);
        return repository.findById(id)
            .map(existing -> {
                if (entity.getName() != null) {
                    existing.setName(entity.getName());
                }
                if (entity.getDescription() != null) {
                    existing.setDescription(entity.getDescription());
                }
                return repository.save(existing);
            })
            .orElseThrow(() -> new IllegalArgumentException("Permission not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Permission with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Permission not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }