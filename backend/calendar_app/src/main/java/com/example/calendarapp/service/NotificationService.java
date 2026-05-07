package com.example.calendarapp.service;

import com.example.calendarapp.entity.Notification;
import com.example.calendarapp.repository.NotificationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final NotificationRepository repository;

    @Transactional
    public Notification create(Notification entity) {
        log.info("Creating new Notification: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Notification> findById(Long id) {
        log.info("Finding Notification by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Notification> findAll() {
        log.info("Fetching all Notification");
        return repository.findAll();
    }

    @Transactional
    public Notification update(Long id, Notification entity) {
        log.info("Updating Notification with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("Notification not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Notification with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Notification not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }