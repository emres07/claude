package com.example.task.service;

import com.example.task.entity.Task;
import com.example.task.repository.TaskRepository;
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
public class TaskService {

    private final TaskRepository taskRepository;

    public List<Task> getAll() {
        log.info("Fetching all Task records");
        return taskRepository.findAll();
    }

    public Optional<Task> getById(Long id) {
        log.info("Fetching Task by id: {}", id);
        return taskRepository.findById(id);
    }

    @Transactional
    public Task create(Task task) {
        log.info("Creating new Task");
        return taskRepository.save(task);
    }

    @Transactional
    public Task update(Long id, Task task) {
        log.info("Updating Task with id: {}", id);
        task.setId(id);
        return taskRepository.save(task);
    }

    @Transactional
    public void delete(Long id) {
        log.info("Deleting Task with id: {}", id);
        taskRepository.deleteById(id);
    }
}
