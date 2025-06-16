package org.example.config;

import lombok.Getter;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class MySessionFactory {
    @Getter
    private static final SessionFactory factory = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .buildSessionFactory();
}
