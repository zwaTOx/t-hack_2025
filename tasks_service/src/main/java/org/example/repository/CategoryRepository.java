package org.example.repository;

import org.example.entity.Category;
import org.example.entity.Task;
import org.example.entity.User;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;

import java.util.List;

public class CategoryRepository implements Repository<Category>
{
    private final Session session = new Configuration()
            .addAnnotatedClass(Task.class)
            .addAnnotatedClass(User.class)
            .addAnnotatedClass(Category.class)
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
    public List<Category> getByUserId(Long id) {
        Query<Category> query = session.createQuery("from Category where userId.id = :param", Category.class);
        query.setParameter("param", id);
        return query.list();
    }
    public void deleteByName(String name, Long userId) {
        Transaction transaction = session.beginTransaction();
        Query query = session.createQuery("delete from Category where name = :name and userId.id = :id");
        query.setParameter("name", name);
        query.setParameter("id", userId);
        query.executeUpdate();
        transaction.commit();
    }
}
