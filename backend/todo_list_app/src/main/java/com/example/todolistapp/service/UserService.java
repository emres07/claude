package com.example.todolistapp.service;

import com.example.todolistapp.entity.User;
import com.example.todolistapp.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository repository;

    @Transactional
    public User create(User entity) {
        log.info("Creating new User: {}", entity);
        if (entity.getName() == null || entity.getName().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        return repository.save(entity);
    }

    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        log.info("Finding User by id: {}", id);
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("Invalid ID provided");
        }
        return repository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<User> findAll() {
        log.info("Fetching all User");
        return repository.findAll();
    }

    @Transactional
    public User update(Long id, User entity) {
        log.info("Updating User with id: {}", id);
        return repository.findById(id)
            .map(existing -> {
                if (entity.getEmail() != null) {
                    existing.setEmail(entity.getEmail());
                }
                if (entity.getName() != null) {
                    existing.setName(entity.getName());
                }
                if (entity.getPasswordhash() != null) {
                    existing.setPasswordhash(entity.getPasswordhash());
                }
                return repository.save(existing);
            })
            .orElseThrow(() -> new IllegalArgumentException("User not found with id: " + id));
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting User with id: {}", id);
        if (!repository.existsById(id)) {
            throw new IllegalArgumentException("User not found with id: " + id);
        }
        repository.deleteById(id);
    }

    }