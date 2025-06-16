package org.example.repository;

import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;

import java.util.List;

public class CategoryRepository implements Repository<Category>
{
    private final Session session = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .buildSessionFactory().openSession();
    @Override
    public Category getById(Long id) {
        return session.get(Category.class, id);
    }

    @Override
    public List<Category> getAll() {
        return session.createQuery("from Category", Category.class).list();
    }

    @Override
    public void update(Category category) {
        Transaction transaction = session.beginTransaction();
        session.merge(category);
        transaction.commit();
        session.flush();
    }

    @Override
    public void delete(Category category) {
        Transaction transaction = session.beginTransaction();
        session.remove(category);
        transaction.commit();
        session.flush();
    }

    @Override
    public void save(Category category) {
        Transaction transaction = session.beginTransaction();
        session.persist(category);
        transaction.commit();
        session.flush();
    }
}
