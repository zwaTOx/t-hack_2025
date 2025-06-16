package org.example.mapper;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.example.entity.Task;
import org.example.repository.TaskRepository;


import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class JsonTaskMapper implements JsonMapper<Task>{
    private final ObjectMapper mapper = new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);;
    @Override
    public Task getEntity(InputStream stream) {
        Task task;
        try {
             task = mapper.readValue(stream, Task.class);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return task;
    }

    @Override
    public String createJson(List<Task> list) {
        String json;
        try {
            json = mapper.writeValueAsString(list);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return json;
    }

}
