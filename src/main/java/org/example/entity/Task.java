package org.example.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
@Entity
@Table(name = "tasks")
@NoArgsConstructor
@AllArgsConstructor
@Data
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;
    @Column(name = "name")
    private String name;
    @Column(name = "description")
    private String description;
    @ManyToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id")
    private User userId;
    @Column(name = "deadline")
    private LocalDateTime deadline;
    @Column(name = "created_time")
    private LocalDateTime createdTime;
    @Column(name = "updated_time")
    private LocalDateTime updatedTime;
    @Column(name = "category")
    private String category;
}
