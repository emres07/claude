package com.example.calendarapp.repository;

import com.example.calendarapp.entity.Meeting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * MeetingRepository
 */
@Repository
public interface MeetingRepository extends JpaRepository<Meeting, Long> {

    // TODO: Add custom query methods

}
