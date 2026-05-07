package com.example.task.repository;

import com.example.task.entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    Optional<Task> findById(Long id);

    List<Task> findAll();

    // Add custom queries here
    @Query("SELECT e FROM Task e WHERE e.name = :name")
    Optional<Task> findByName(String name);
}
