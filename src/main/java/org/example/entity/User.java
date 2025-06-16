package org.example.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;
    @Column(name = "username")
    private String username;
    @Column(name = "chat_id")
    private Long chatId;
    public User() {

    }
    public User(Long id, String username, Long chatId) {
        this.id = id;
        this.username = username;
        this.chatId = chatId;
    }

    @Override
    public String toString() {
        return "User(" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", chatId=" + chatId +
                ')';
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Long getChatId() {
        return chatId;
    }

    public void setChatId(Long chatId) {
        this.chatId = chatId;
    }
}
