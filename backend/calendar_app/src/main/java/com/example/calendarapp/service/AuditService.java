package com.example.calendarapp.service;

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
 * AuditService - Implement comprehensive audit logging service to track user actions, system events, and changes. Create audit endpoints for retrieving audit logs and activity reports
 *
 * Tracks all user actions and system events for:
 * - Compliance and security audit trails
 * - Activity logging
 * - System event tracking
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    /**
     * Log an action to audit trail
     */
    @Transactional
    public void logAction(String action, String entity, Long entityId, String userId, String details) {
        AuditLog auditLog = AuditLog.builder()
            .action(action)
            .entity(entity)
            .entityId(entityId)
            .userId(userId)
            .details(details)
            .timestamp(LocalDateTime.now())
            .build();

        auditLogRepository.save(auditLog);
        log.debug("Audit logged: {} on {} with ID: {}", action, entity, entityId);
    }

    /**
     * Get audit logs for a specific entity
     */
    public List<AuditLogResponse> getAuditLogs(String entity, Integer limit) {
        return auditLogRepository.findByEntityOrderByTimestampDesc(entity)
            .stream()
            .limit(limit != null ? limit : 100)
            .map(AuditLogResponse::from)
            .toList();
    }

    /**
     * Get audit logs by user
     */
    public List<AuditLogResponse> getAuditLogsByUser(String userId) {
        return auditLogRepository.findByUserIdOrderByTimestampDesc(userId)
            .stream()
            .map(AuditLogResponse::from)
            .toList();
    }

    /**
     * Get audit logs for time period
     */
    public List<AuditLogResponse> getAuditLogsForPeriod(LocalDateTime startTime, LocalDateTime endTime) {
        return auditLogRepository.findByTimestampBetweenOrderByTimestampDesc(startTime, endTime)
            .stream()
            .map(AuditLogResponse::from)
            .toList();
    }

    /**
     * Get total audit log count
     */
    public long countAuditLogs() {
        return auditLogRepository.count();
    }
}
