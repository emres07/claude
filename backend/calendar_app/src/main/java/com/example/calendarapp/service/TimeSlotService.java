package com.example.calendarapp.service;

import com.example.calendarapp.entity.TimeSlot;
import com.example.calendarapp.repository.TimeSlotRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class TimeSlotService {

    private final TimeSlotRepository repository;

    @Transactional
    public TimeSlot create(TimeSlot entity) {
        log.info("Creating new TimeSlot: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<TimeSlot> findById(Long id) {
        log.info("Finding TimeSlot by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<TimeSlot> findAll() {
        log.info("Fetching all TimeSlot");
        return repository.findAll();
    }

    @Transactional
    public TimeSlot update(Long id, TimeSlot entity) {
        log.info("Updating TimeSlot with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("TimeSlot not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting TimeSlot with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("TimeSlot not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }