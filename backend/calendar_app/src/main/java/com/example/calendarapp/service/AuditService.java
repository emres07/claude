package com.example.calendarapp.service;

import com.example.calendarapp.entity.audit;
import com.example.calendarapp.repository.auditRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class auditService {

    private final auditRepository repository;

    public audit save(audit entity) {
        log.info("Saving audit: {}", entity.getId());
        return repository.save(entity);
    }

    public audit findById(Long id) {
        log.info("Finding audit by id: {}", id);
        return repository.findById(id).orElseThrow(() ->
            new IllegalArgumentException("audit not found with id: " + id));
    }

    public List<audit> findAll() {
        log.info("Finding all audit");
        return repository.findAll();
    }

    public void delete(Long id) {
        log.info("Deleting audit with id: {}", id);
        repository.deleteById(id);
    }

    }