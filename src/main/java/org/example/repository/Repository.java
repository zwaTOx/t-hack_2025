package org.example.repository;

import java.util.List;

public interface Repository<T>{
    T getById(Long id);
    List<T> getAll();
    void update(T t);
    void delete(T t);
    void save(T t);
}
