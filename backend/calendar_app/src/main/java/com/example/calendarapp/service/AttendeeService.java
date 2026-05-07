package com.example.calendarapp.service;

import com.example.calendarapp.entity.Attendee;
import com.example.calendarapp.repository.AttendeeRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class AttendeeService {

    private final AttendeeRepository repository;

    @Transactional
    public Attendee create(Attendee entity) {
        log.info("Creating new Attendee: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Attendee> findById(Long id) {
        log.info("Finding Attendee by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Attendee> findAll() {
        log.info("Fetching all Attendee");
        return repository.findAll();
    }

    @Transactional
    public Attendee update(Long id, Attendee entity) {
        log.info("Updating Attendee with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("Attendee not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Attendee with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Attendee not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }