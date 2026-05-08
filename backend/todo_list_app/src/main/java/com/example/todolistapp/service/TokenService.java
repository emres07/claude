package com.example.todolistapp.service;

import com.example.todolistapp.entity.Token;
import com.example.todolistapp.repository.TokenRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class TokenService {

    private final TokenRepository repository;

    @Transactional
    public Token create(Token entity) {
        log.info("Creating new Token: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<Token> findById(Long id) {
        log.info("Finding Token by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Token> findAll() {
        log.info("Fetching all Token");
        return repository.findAll();
    }

    @Transactional
    public Token update(Long id, Token entity) {
        log.info("Updating Token with id: {}", id);
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
            .orElseThrow(() -> new IllegalArgumentException("Token not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Token with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("Token not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }