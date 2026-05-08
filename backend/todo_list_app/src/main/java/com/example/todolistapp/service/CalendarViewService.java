package com.example.todolistapp.service;

import com.example.todolistapp.entity.CalendarView;
import com.example.todolistapp.repository.CalendarViewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class CalendarViewService {

    private final CalendarViewRepository repository;

    @Transactional
    public CalendarView create(CalendarView entity) {
        log.info("Creating new CalendarView: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<CalendarView> findById(Long id) {
        log.info("Finding CalendarView by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<CalendarView> findAll() {
        log.info("Fetching all CalendarView");
        return repository.findAll();
    }

    @Transactional
    public CalendarView update(Long id, CalendarView entity) {
        log.info("Updating CalendarView with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("CalendarView not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting CalendarView with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("CalendarView not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }