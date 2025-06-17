package org.example.config;

import lombok.Getter;
import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class MySessionFactory {
    public static final SessionFactory factory = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .addAnnotatedClass(Category.class)
            .buildSessionFactory();
}
