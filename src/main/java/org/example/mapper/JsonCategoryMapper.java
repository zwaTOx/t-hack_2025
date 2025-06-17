package org.example.mapper;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.example.entity.Category;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class JsonCategoryMapper implements JsonMapper<Category> {
    private final ObjectMapper mapper = new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);;
    @Override
    public Category getEntity(InputStream stream) {
        Category category;
        try {
            category = mapper.readValue(stream, Category.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return category;
    }

    @Override
    public String createJson(List<Category> list) {
        String json;
        try {
            json = mapper.writeValueAsString(list);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return json;
    }
}
