package com.example.calendarapp.repository;

import com.example.calendarapp.entity.Calendar;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

/**
 * CalendarRepository
 */
@Repository
public interface CalendarRepository extends JpaRepository<Calendar, Long> {

    // TODO: Add custom query methods

}
