package com.example.calendarapp.service;

import com.example.calendarapp.entity.ActivityReport;
import com.example.calendarapp.repository.ActivityReportRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class ActivityReportService {

    private final ActivityReportRepository repository;

    @Transactional
    public ActivityReport create(ActivityReport entity) {
        log.info("Creating new ActivityReport: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<ActivityReport> findById(Long id) {
        log.info("Finding ActivityReport by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<ActivityReport> findAll() {
        log.info("Fetching all ActivityReport");
        return repository.findAll();
    }

    @Transactional
    public ActivityReport update(Long id, ActivityReport entity) {
        log.info("Updating ActivityReport with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("ActivityReport not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting ActivityReport with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("ActivityReport not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }