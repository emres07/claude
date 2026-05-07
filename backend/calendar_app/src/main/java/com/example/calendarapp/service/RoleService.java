package com.example.calendarapp.service;

import com.example.calendarapp.entity.Role;
import com.example.calendarapp.repository.RoleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class RoleService {

    private final RoleRepository repository;

    @Transactional
    public Role create(Role entity) {
        log.info("Creating new Role: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Role> findById(Long id) {
        log.info("Finding Role by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Role> findAll() {
        log.info("Fetching all Role");
        return repository.findAll();
    }

    @Transactional
    public Role update(Long id, Role entity) {
        log.info("Updating Role with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("Role not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Role with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Role not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }