package com.example.audit.repository;

import com.example.audit.entity.Audit;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface AuditRepository extends JpaRepository<Audit, Long> {

    Optional<Audit> findById(Long id);

    List<Audit> findAll();

    // Add custom queries here
    @Query("SELECT e FROM Audit e WHERE e.name = :name")
    Optional<Audit> findByName(String name);
}
