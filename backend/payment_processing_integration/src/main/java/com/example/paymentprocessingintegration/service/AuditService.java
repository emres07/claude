package com.example.audit.service;

import com.example.audit.entity.Audit;
import com.example.audit.repository.AuditRepository;
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
public class AuditService {

    private final AuditRepository auditRepository;

    public List<Audit> getAll() {
        log.info("Fetching all Audit records");
        return auditRepository.findAll();
    }

    public Optional<Audit> getById(Long id) {
        log.info("Fetching Audit by id: {}", id);
        return auditRepository.findById(id);
    }

    @Transactional
    public Audit create(Audit audit) {
        log.info("Creating new Audit");
        return auditRepository.save(audit);
    }

    @Transactional
    public Audit update(Long id, Audit audit) {
        log.info("Updating Audit with id: {}", id);
        audit.setId(id);
        return auditRepository.save(audit);
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Audit with id: {}", id);
        auditRepository.deleteById(id);
    }
}
