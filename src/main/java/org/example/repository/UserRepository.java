package org.example.repository;

import org.example.config.MySessionFactory;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.query.Query;

import java.util.List;

public class UserRepository implements Repository<User>{
    private final Session session = MySessionFactory.getFactory().openSession();
    @Override
    public User getById(Long id) {
        Query<User> query = session.createQuery("from User where id = :param", User.class);
        query.setParameter(1, id);
        return query.getSingleResult();
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
}
