package org.example.repository;

import org.example.config.MySessionFactory;
import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;

import java.util.List;

public class UserRepository implements Repository<User>{
    private final Session session = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .addAnnotatedClass(Category.class)
            .buildSessionFactory().openSession();
    @Override
    public User getById(Long id) {
        return session.get(User.class, id);
    }

    @Override
    public List<User> getAll() {
        return session.createQuery("from User", User.class).list();
    }

    @Override
    public void update(User user) {
        Transaction transaction = session.beginTransaction();
        session.merge(user);
        transaction.commit();
    }

    @Override
    public void delete(User user) {
        Transaction transaction = session.beginTransaction();
        session.remove(user);
        transaction.commit();
    }

    @Override
    public void save(User user) {
        Transaction transaction = session.beginTransaction();
        session.persist(user);
        transaction.commit();
    }
    public Long getIdByUserName(String username) {
        Query<Long> query = session.createQuery("select id from User where username = :param", Long.class);
        query.setParameter("param", username);
        return query.list().get(0);
    }
}
