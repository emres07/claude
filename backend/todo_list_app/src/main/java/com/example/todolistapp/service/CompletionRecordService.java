package com.example.todolistapp.service;

import com.example.todolistapp.entity.CompletionRecord;
import com.example.todolistapp.repository.CompletionRecordRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class CompletionRecordService {

    private final CompletionRecordRepository repository;

    @Transactional
    public CompletionRecord create(CompletionRecord entity) {
        log.info("Creating new CompletionRecord: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<CompletionRecord> findById(Long id) {
        log.info("Finding CompletionRecord by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<CompletionRecord> findAll() {
        log.info("Fetching all CompletionRecord");
        return repository.findAll();
    }

    @Transactional
    public CompletionRecord update(Long id, CompletionRecord entity) {
        log.info("Updating CompletionRecord with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("CompletionRecord not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting CompletionRecord with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("CompletionRecord not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }