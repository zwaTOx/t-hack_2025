package org.example.repository;


import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;

import java.util.List;

public class TaskRepository implements Repository<Task> {
    private final Session session = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .addAnnotatedClass(Category.class)
            .buildSessionFactory().openSession();
    @Override
    public Task getById(Long id) {
        return session.get(Task.class, id);
    }

    @Override
    public List<Task> getAll() {
        return session.createQuery("from Task", Task.class).list();
    }

    @Override
    public void update(Task task) {
        Transaction transaction = session.beginTransaction();
        session.merge(task);
        transaction.commit();
    }

    @Override
    public void delete(Task task) {
        Transaction transaction = session.beginTransaction();
        session.remove(task);
        transaction.commit();
    }

    @Override
    public void save(Task task) {
        Transaction transaction = session.beginTransaction();
        session.persist(task);
        transaction.commit();
    }
    public List<Task> getByUserId(Long id) {
        Query<Task> query = session.createQuery("from Task where userId.id = :param", Task.class);
        query.setParameter(1, id);
        return query.list();
    }
}
