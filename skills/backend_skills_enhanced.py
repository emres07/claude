"""
Enhanced Backend Skills - Reads subtask READMEs and generates detailed implementation code.

Parses subtask specifications from README files and generates production-ready:
- JPA entities with validation and lifecycle hooks
- Service classes with business logic
- Controllers with REST endpoints
- DTOs for requests/responses
- Exception handlers
- Security configuration
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class EnhancedBackendSkill:
    """Generates detailed backend code based on subtask specifications."""

    @staticmethod
    def parse_readme(readme_path: str) -> Dict[str, Any]:
        """Parse subtask MD file and extract specifications."""
        if not Path(readme_path).exists():
            return {}

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        spec = {
            "title": EnhancedBackendSkill._extract_title(content),
            "description": EnhancedBackendSkill._extract_section(content, "## Description"),
            "apis": EnhancedBackendSkill._extract_list(content, "## APIs to Implement"),
            "tables": EnhancedBackendSkill._extract_list(content, "## Database Schemas"),
            "databases": EnhancedBackendSkill._extract_list(content, "## Database Schemas"),
        }
        return spec

    @staticmethod
    def _extract_title(content: str) -> str:
        """Extract title from README."""
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_section(content: str, section_header: str) -> str:
        """Extract section content from README."""
        pattern = f"{section_header}\n(.+?)(?=\n###|$)"
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _extract_list(content: str, section_header: str) -> List[str]:
        """Extract list items from README section."""
        section = EnhancedBackendSkill._extract_section(content, section_header)
        items = re.findall(r"^- (.+)$", section, re.MULTILINE)
        return [item.strip() for item in items]

    @staticmethod
    def generate_user_entity_from_spec(spec: Dict[str, Any]) -> str:
        """Generate User entity based on specification."""
        entity_name = "User"
        tables = spec.get("tables", []) + spec.get("databases", [])

        return f'''package com.example.calendarapp.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;
import com.example.calendarapp.entity.enums.UserRole;

/**
 * User Entity
 * {spec.get('description', 'User management entity')}
 */
@Entity
@Table(name = "users", indexes = {{
    @Index(name = "idx_users_email", columnList = "email", unique = true),
    @Index(name = "idx_users_created_at", columnList = "created_at"),
    @Index(name = "idx_users_updated_at", columnList = "updated_at")
}})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false)
    private String passwordHash;

    @Column(length = 255)
    private String phoneNumber;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserRole role;

    @Column(nullable = false)
    private Boolean active = true;

    @Column
    private LocalDateTime lastLoginAt;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @Version
    @Column(nullable = false)
    private Long version;

    @PrePersist
    protected void onCreate() {{
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (active == null) {{
            active = true;
        }}
    }}

    @PreUpdate
    protected void onUpdate() {{
        updatedAt = LocalDateTime.now();
    }}

    @PostLoad
    public void postLoad() {{
        if (version == null) {{
            version = 0L;
        }}
    }}
}}
'''

    @staticmethod
    def generate_user_service_from_spec(spec: Dict[str, Any]) -> str:
        """Generate UserService based on specification."""
        apis = spec.get("apis", [])
        description = spec.get("description", "User management")

        return f'''package com.example.calendarapp.service;

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
 * UserService - {description}
 *
 * Provides business logic for user management operations including:
 * - User registration and profile management
 * - User lookup and filtering
 * - User activation/deactivation
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {{

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    /**
     * Register a new user
     * Validates email uniqueness and encrypts password
     */
    @Transactional
    public UserProfileResponse registerUser(UserRegistrationRequest request) {{
        log.info("Registering new user with email: {{}}", request.getEmail());

        if (userRepository.existsByEmail(request.getEmail())) {{
            throw new UserAlreadyExistsException("Email already registered: " + request.getEmail());
        }}

        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .phoneNumber(request.getPhoneNumber())
            .active(true)
            .build();

        User savedUser = userRepository.save(user);
        log.info("User registered successfully with ID: {{}}", savedUser.getId());

        return UserProfileResponse.from(savedUser);
    }}

    /**
     * Get user by ID
     */
    public UserProfileResponse getUserById(Long id) {{
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));
        return UserProfileResponse.from(user);
    }}

    /**
     * Get user by email
     */
    public UserProfileResponse getUserByEmail(String email) {{
        User user = userRepository.findByEmail(email)
            .orElseThrow(() -> new UserNotFoundException("User not found with email: " + email));
        return UserProfileResponse.from(user);
    }}

    /**
     * Update user profile
     */
    @Transactional
    public UserProfileResponse updateUserProfile(Long id, UserProfileRequest request) {{
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));

        if (request.getName() != null) {{
            user.setName(request.getName());
        }}
        if (request.getPhoneNumber() != null) {{
            user.setPhoneNumber(request.getPhoneNumber());
        }}

        User updatedUser = userRepository.save(user);
        log.info("User profile updated for ID: {{}}", id);

        return UserProfileResponse.from(updatedUser);
    }}

    /**
     * Get all active users with pagination
     */
    public Page<UserProfileResponse> getAllActiveUsers(int page, int size) {{
        return userRepository.findByActiveTrue(PageRequest.of(page, size))
            .map(UserProfileResponse::from);
    }}

    /**
     * Deactivate user account
     */
    @Transactional
    public void deactivateUser(Long id) {{
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found with ID: " + id));

        user.setActive(false);
        userRepository.save(user);
        log.info("User deactivated with ID: {{}}", id);
    }}

    /**
     * Record user last login time
     */
    @Transactional
    public void recordLastLogin(Long userId) {{
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found"));

        user.setLastLoginAt(LocalDateTime.now());
        userRepository.save(user);
        log.debug("Last login recorded for user ID: {{}}", userId);
    }}

    /**
     * Verify user password
     */
    public boolean verifyPassword(Long userId, String rawPassword) {{
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException("User not found"));

        return passwordEncoder.matches(rawPassword, user.getPasswordHash());
    }}
}}
'''

    @staticmethod
    def generate_user_controller_from_spec(spec: Dict[str, Any]) -> str:
        """Generate UserController based on specification."""
        apis = spec.get("apis", [])
        description = spec.get("description", "User management")

        return f'''package com.example.calendarapp.controller;

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
 * UserController - {description}
 *
 * REST endpoints for user management operations
 * APIs:
{chr(10).join([f' * - {api}' for api in apis[:5]])}
 */
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
@Slf4j
public class UserController {{

    private final UserService userService;

    /**
     * Register a new user
     * POST /api/v1/users/register
     */
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<UserProfileResponse>> registerUser(
            @Valid @RequestBody UserRegistrationRequest request) {{
        log.info("POST /api/v1/users/register - Registering user: {{}}", request.getEmail());

        UserProfileResponse response = userService.registerUser(request);

        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(ApiResponse.success("User registered successfully", response));
    }}

    /**
     * Get user by ID
     * GET /api/v1/users/{{id}}
     */
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<UserProfileResponse>> getUserById(@PathVariable Long id) {{
        log.info("GET /api/v1/users/{{}} - Fetching user", id);

        UserProfileResponse response = userService.getUserById(id);

        return ResponseEntity.ok(ApiResponse.success("User retrieved successfully", response));
    }}

    /**
     * Get all active users with pagination
     * GET /api/v1/users?page=0&size=20
     */
    @GetMapping
    public ResponseEntity<ApiResponse<Page<UserProfileResponse>>> getAllUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {{
        log.info("GET /api/v1/users - Fetching all active users - page: {{}}, size: {{}}", page, size);

        Page<UserProfileResponse> users = userService.getAllActiveUsers(page, size);

        return ResponseEntity.ok(ApiResponse.success("Users retrieved successfully", users));
    }}

    /**
     * Update user profile
     * PUT /api/v1/users/{{id}}
     */
    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<UserProfileResponse>> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserProfileRequest request) {{
        log.info("PUT /api/v1/users/{{}} - Updating user", id);

        UserProfileResponse response = userService.updateUserProfile(id, request);

        return ResponseEntity.ok(ApiResponse.success("User updated successfully", response));
    }}

    /**
     * Deactivate user account
     * DELETE /api/v1/users/{{id}}
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deactivateUser(@PathVariable Long id) {{
        log.info("DELETE /api/v1/users/{{}} - Deactivating user", id);

        userService.deactivateUser(id);

        return ResponseEntity.ok(ApiResponse.success("User deactivated successfully", null));
    }}
}}
'''

    @staticmethod
    def generate_audit_service_from_spec(spec: Dict[str, Any]) -> str:
        """Generate AuditService based on specification."""
        description = spec.get("description", "Audit logging")

        return f'''package com.example.calendarapp.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import com.example.calendarapp.entity.AuditLog;
import com.example.calendarapp.repository.AuditLogRepository;
import com.example.calendarapp.dto.AuditLogResponse;

import java.time.LocalDateTime;
import java.util.List;

/**
 * AuditService - {description}
 *
 * Tracks all user actions and system events for:
 * - Compliance and security audit trails
 * - Activity logging
 * - System event tracking
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class AuditService {{

    private final AuditLogRepository auditLogRepository;

    /**
     * Log an action to audit trail
     */
    @Transactional
    public void logAction(String action, String entity, Long entityId, String userId, String details) {{
        AuditLog auditLog = AuditLog.builder()
            .action(action)
            .entity(entity)
            .entityId(entityId)
            .userId(userId)
            .details(details)
            .timestamp(LocalDateTime.now())
            .build();

        auditLogRepository.save(auditLog);
        log.debug("Audit logged: {{}} on {{}} with ID: {{}}", action, entity, entityId);
    }}

    /**
     * Get audit logs for a specific entity
     */
    public List<AuditLogResponse> getAuditLogs(String entity, Integer limit) {{
        return auditLogRepository.findByEntityOrderByTimestampDesc(entity)
            .stream()
            .limit(limit != null ? limit : 100)
            .map(AuditLogResponse::from)
            .toList();
    }}

    /**
     * Get audit logs by user
     */
    public List<AuditLogResponse> getAuditLogsByUser(String userId) {{
        return auditLogRepository.findByUserIdOrderByTimestampDesc(userId)
            .stream()
            .map(AuditLogResponse::from)
            .toList();
    }}

    /**
     * Get audit logs for time period
     */
    public List<AuditLogResponse> getAuditLogsForPeriod(LocalDateTime startTime, LocalDateTime endTime) {{
        return auditLogRepository.findByTimestampBetweenOrderByTimestampDesc(startTime, endTime)
            .stream()
            .map(AuditLogResponse::from)
            .toList();
    }}

    /**
     * Get total audit log count
     */
    public long countAuditLogs() {{
        return auditLogRepository.count();
    }}
}}
'''

    @staticmethod
    def generate_jwt_util_from_spec(spec: Dict[str, Any]) -> str:
        """Generate JWT utility based on specification."""
        return '''package com.example.calendarapp.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;

import java.security.Key;
import java.util.Date;

/**
 * JwtTokenProvider - JWT token generation and validation
 *
 * Handles JWT token lifecycle:
 * - Token generation with expiration
 * - Token validation and parsing
 * - Claims extraction
 */
@Component
@Slf4j
public class JwtTokenProvider {

    @Value("${jwt.secret:your-secret-key-change-in-production}")
    private String jwtSecret;

    @Value("${jwt.expiration:86400000}")
    private long jwtExpirationMs;

    /**
     * Generate access token (default 24 hours)
     */
    public String generateToken(String email, String userId) {
        return createToken(email, userId, jwtExpirationMs);
    }

    /**
     * Generate refresh token (7 days)
     */
    public String generateRefreshToken(String email, String userId) {
        return createToken(email, userId, jwtExpirationMs * 7);
    }

    /**
     * Create JWT token with custom expiration
     */
    private String createToken(String email, String userId, long expirationTime) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expirationTime);

        Key key = Keys.hmacShaKeyFor(jwtSecret.getBytes());

        return Jwts.builder()
            .setSubject(email)
            .claim("userId", userId)
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(key, SignatureAlgorithm.HS512)
            .compact();
    }

    /**
     * Extract email from token
     */
    public String getEmailFromToken(String token) {
        Key key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parserBuilder()
            .setSigningKey(key)
            .build()
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }

    /**
     * Extract userId from token
     */
    public String getUserIdFromToken(String token) {
        Key key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
        return Jwts.parserBuilder()
            .setSigningKey(key)
            .build()
            .parseClaimsJws(token)
            .getBody()
            .get("userId", String.class);
    }

    /**
     * Validate JWT token signature and expiration
     */
    public boolean validateToken(String token) {
        try {
            Key key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            log.error("JWT validation error: {}", e.getMessage());
            return false;
        }
    }

    /**
     * Check if token is expired
     */
    public boolean isTokenExpired(String token) {
        try {
            Key key = Keys.hmacShaKeyFor(jwtSecret.getBytes());
            Date expiration = Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getExpiration();

            return expiration.before(new Date());
        } catch (JwtException e) {
            return true;
        }
    }
}
'''
