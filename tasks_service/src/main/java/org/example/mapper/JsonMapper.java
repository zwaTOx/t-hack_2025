package org.example.mapper;

import java.io.InputStream;
import java.util.List;

public interface JsonMapper<T> {
    T getEntity(InputStream stream);
    String createJson(List<T> list);
}
