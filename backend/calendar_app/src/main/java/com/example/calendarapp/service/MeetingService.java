package com.example.calendarapp.service;

import com.example.calendarapp.entity.Meeting;
import com.example.calendarapp.repository.MeetingRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class MeetingService {

    private final MeetingRepository repository;

    @Transactional
    public Meeting create(Meeting entity) {
        log.info("Creating new Meeting: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Meeting> findById(Long id) {
        log.info("Finding Meeting by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Meeting> findAll() {
        log.info("Fetching all Meeting");
        return repository.findAll();
    }

    @Transactional
    public Meeting update(Long id, Meeting entity) {
        log.info("Updating Meeting with id: {}", id);
        return repository.findById(id)
            .map(existing -> {
                if (entity.getTitle() != null) {
                    existing.setTitle(entity.getTitle());
                }
                if (entity.getDescription() != null) {
                    existing.setDescription(entity.getDescription());
                }
                if (entity.getStarttime() != null) {
                    existing.setStarttime(entity.getStarttime());
                }
                if (entity.getEndtime() != null) {
                    existing.setEndtime(entity.getEndtime());
                }
                if (entity.getLocation() != null) {
                    existing.setLocation(entity.getLocation());
                }
                return repository.save(existing);
            })
            .orElseThrow(() -> new IllegalArgumentException("Meeting not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Meeting with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Meeting not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }