package com.example.calendarapp.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.validation.annotation.Validated;
import org.springframework.data.domain.Page;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import jakarta.validation.Valid;

import com.example.calendarapp.service.UserService;
import com.example.calendarapp.dto.UserRegistrationRequest;
import com.example.calendarapp.dto.UserProfileResponse;
import com.example.calendarapp.dto.UserProfileRequest;
import com.example.calendarapp.dto.ApiResponse;

/**
 * UserController - Build comprehensive REST API controllers with proper HTTP methods, request/response handling, error responses, and integration with backend services
 *
 * REST endpoints for user management operations
 * APIs:
 * - /api/v1/
 */
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
@Slf4j
public class UserController {

    private final UserService userService;

    /**
     * Register a new user
     * POST /api/v1/users/register
     */
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<UserProfileResponse>> registerUser(
            @Valid @RequestBody UserRegistrationRequest request) {
        log.info("POST /api/v1/users/register - Registering user: {}", request.getEmail());

        UserProfileResponse response = userService.registerUser(request);

        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(ApiResponse.success("User registered successfully", response));
    }

    /**
     * Get user by ID
     * GET /api/v1/users/{id}
     */
    @GetMapping("/<built-in function id>")
    public ResponseEntity<ApiResponse<UserProfileResponse>> getUserById(@PathVariable Long id) {
        log.info("GET /api/v1/users/{} - Fetching user", id);

        UserProfileResponse response = userService.getUserById(id);

        return ResponseEntity.ok(ApiResponse.success("User retrieved successfully", response));
    }

    /**
     * Get all active users with pagination
     * GET /api/v1/users?page=0&size=20
     */
    @GetMapping
    public ResponseEntity<ApiResponse<Page<UserProfileResponse>>> getAllUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        log.info("GET /api/v1/users - Fetching all active users - page: {}, size: {}", page, size);

        Page<UserProfileResponse> users = userService.getAllActiveUsers(page, size);

        return ResponseEntity.ok(ApiResponse.success("Users retrieved successfully", users));
    }

    /**
     * Update user profile
     * PUT /api/v1/users/{id}
     */
    @PutMapping("/<built-in function id>")
    public ResponseEntity<ApiResponse<UserProfileResponse>> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserProfileRequest request) {
        log.info("PUT /api/v1/users/{} - Updating user", id);

        UserProfileResponse response = userService.updateUserProfile(id, request);

        return ResponseEntity.ok(ApiResponse.success("User updated successfully", response));
    }

    /**
     * Deactivate user account
     * DELETE /api/v1/users/{id}
     */
    @DeleteMapping("/<built-in function id>")
    public ResponseEntity<ApiResponse<Void>> deactivateUser(@PathVariable Long id) {
        log.info("DELETE /api/v1/users/{} - Deactivating user", id);

        userService.deactivateUser(id);

        return ResponseEntity.ok(ApiResponse.success("User deactivated successfully", null));
    }
}
