package com.example.todolistapp.service;

import com.example.todolistapp.entity.Calendar;
import com.example.todolistapp.repository.CalendarRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class CalendarService {

    private final CalendarRepository repository;

    @Transactional
    public Calendar create(Calendar entity) {
        log.info("Creating new Calendar: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Calendar> findById(Long id) {
        log.info("Finding Calendar by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Calendar> findAll() {
        log.info("Fetching all Calendar");
        return repository.findAll();
    }

    @Transactional
    public Calendar update(Long id, Calendar entity) {
        log.info("Updating Calendar with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("Calendar not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Calendar with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Calendar not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }