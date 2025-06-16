package org.example.repository;

import org.example.config.MySessionFactory;
import org.example.entity.Task;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.query.Query;

import java.util.List;

public class TaskRepository implements Repository<Task> {
    private final Session session = MySessionFactory.getFactory().openSession();
    @Override
    public Task getById(Long id) {
        Query<Task> query = session.createQuery("from Task where id = :param", Task.class);
        query.setParameter(1, id);
        return query.getSingleResult();
    }

    @Override
    public List<Task> getAll() {
        return session.createQuery("from Task ", Task.class).list();
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
