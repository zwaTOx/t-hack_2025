package org.example;


import liquibase.Contexts;
import liquibase.LabelExpression;
import liquibase.Liquibase;
import liquibase.Scope;
import liquibase.database.Database;
import liquibase.database.DatabaseFactory;
import liquibase.database.jvm.JdbcConnection;
import liquibase.resource.ClassLoaderResourceAccessor;
import org.example.config.MySessionFactory;
import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;

import java.sql.Connection;
import java.sql.DriverManager;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

public class App
{
    public static void main( String[] args ) throws Exception
    {
        User user = new User();
        user.setChatId(1L);
        user.setUsername("xelliks");
        Category category = new Category();
        category.setUserId(user);
        category.setColor("red");
        category.setDescription("Очень важно");
        category.setName("Пиздец как важно");
        Task task = new Task();
        task.setUserId(user);
        task.setCategory(category);
        task.setUpdatedTime(LocalDateTime.now());
        task.setDeadline(LocalDateTime.now());
        task.setDescription("Если не сделаю, я пидор");
        task.setName("Сделать доки");
        Session session = MySessionFactory.factory.openSession();
        Transaction transaction = session.beginTransaction();
        session.persist(user);
        session.persist(category);
        session.persist(task);
        transaction.commit();
    }
}
