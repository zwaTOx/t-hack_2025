package org.example.repository;

import org.example.config.MySessionFactory;
import org.example.entity.Category;
import org.hibernate.Session;
import org.hibernate.Transaction;

import java.util.List;

public class CategoryRepository implements Repository<Category>
{
    private final Session session = MySessionFactory.getFactory().openSession();
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
    }

    @Override
    public void delete(Category category) {
        Transaction transaction = session.beginTransaction();
        session.remove(category);
        transaction.commit();
    }

    @Override
    public void save(Category category) {
        Transaction transaction = session.beginTransaction();
        session.persist(category);
        transaction.commit();
    }
}
