package com.example.calendarapp.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.example.calendarapp.entity.User;
import com.example.calendarapp.repository.UserRepository;
import com.example.calendarapp.dto.UserRegistrationRequest;
import com.example.calendarapp.dto.UserProfileResponse;
import com.example.calendarapp.dto.UserProfileRequest;
import com.example.calendarapp.exception.UserAlreadyExistsException;
import com.example.calendarapp.exception.UserNotFoundException;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * UserService - Create User JPA entity with all fields, UserRepository for database operations, and UserService for business logic including registration, profile updates, and user lookup
 *
 * Provides business logic for user management operations including:
 * - User registration and profile management
 * - User lookup and filtering
 * - User activation/deactivation
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    /**
     * Register a new user
     * Validates email uniqueness and encrypts password
     */
    @Transactional
    public UserProfileResponse registerUser(UserRegistrationRequest request) {
        log.info("Registering new user with email: {}", request.getEmail());

        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UserAlreadyExistsException("Email already registered: " + request.getEmail());
        }

        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .phoneNumber(request.getPhoneNumber())
            .active(true)
            .build();

        User savedUser = userRepository.save(user);
        log.info("User registered successfully with ID: {}", savedUser.getId());

        return UserProfileResponse.from(savedUser);
    }

    /**
     * Get user by ID
     */
    public UserProfileResponse getUserById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));
        return UserProfileResponse.from(user);
    }

    /**
     * Get user by email
     */
    public UserProfileResponse getUserByEmail(String email) {
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new UserNotFoundException("User not found with email: " + email));
        return UserProfileResponse.from(user);
    }

    /**
     * Update user profile
     */
    @Transactional
    public UserProfileResponse updateUserProfile(Long id, UserProfileRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));

        if (request.getName() != null) {
            user.setName(request.getName());
        }
        if (request.getPhoneNumber() != null) {
            user.setPhoneNumber(request.getPhoneNumber());
        }

        User updatedUser = userRepository.save(user);
        log.info("User profile updated for ID: {}", id);

        return UserProfileResponse.from(updatedUser);
    }

    /**
     * Get all active users with pagination
     */
    public Page<UserProfileResponse> getAllActiveUsers(int page, int size) {
        return userRepository.findByActiveTrue(PageRequest.of(page, size))
            .map(UserProfileResponse::from);
    }

    /**
     * Deactivate user account
     */
    @Transactional
    public void deactivateUser(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));

        user.setActive(false);
        userRepository.save(user);
        log.info("User deactivated with ID: {}", id);
    }

    /**
     * Record user last login time
     */
    @Transactional
    public void recordLastLogin(Long userId) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found"));

        user.setLastLoginAt(LocalDateTime.now());
        userRepository.save(user);
        log.debug("Last login recorded for user ID: {}", userId);
    }

    /**
     * Verify user password
     */
    public boolean verifyPassword(Long userId, String rawPassword) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found"));

        return passwordEncoder.matches(rawPassword, user.getPasswordHash());
    }
}
