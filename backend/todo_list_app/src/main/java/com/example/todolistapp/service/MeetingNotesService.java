package com.example.todolistapp.service;

import com.example.todolistapp.entity.MeetingNotes;
import com.example.todolistapp.repository.MeetingNotesRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class MeetingNotesService {

    private final MeetingNotesRepository repository;

    @Transactional
    public MeetingNotes create(MeetingNotes entity) {
        log.info("Creating new MeetingNotes: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<MeetingNotes> findById(Long id) {
        log.info("Finding MeetingNotes by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<MeetingNotes> findAll() {
        log.info("Fetching all MeetingNotes");
        return repository.findAll();
    }

    @Transactional
    public MeetingNotes update(Long id, MeetingNotes entity) {
        log.info("Updating MeetingNotes with id: {}", id);
        return repository.findById(id)
            .map(existing -> {
                if (entity.getContent() != null) {
                    existing.setContent(entity.getContent());
                }
                if (entity.getSummary() != null) {
                    existing.setSummary(entity.getSummary());
                }
                return repository.save(existing);
            })
            .orElseThrow(() -> new IllegalArgumentException("MeetingNotes not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting MeetingNotes with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("MeetingNotes not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }