package com.example.user.service;

import com.example.user.entity.User;
import com.example.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;

    public List<User> getAll() {
        log.info("Fetching all User records");
        return userRepository.findAll();
    }

    public Optional<User> getById(Long id) {
        log.info("Fetching User by id: {}", id);
        return userRepository.findById(id);
    }

    @Transactional
    public User create(User user) {
        log.info("Creating new User");
        return userRepository.save(user);
    }

    @Transactional
    public User update(Long id, User user) {
        log.info("Updating User with id: {}", id);
        user.setId(id);
        return userRepository.save(user);
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting User with id: {}", id);
        userRepository.deleteById(id);
    }
}
