package org.example.mapper;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.entity.User;

import java.io.InputStream;
import java.util.List;

public class JsonUserMapper implements JsonMapper<User>{
    private final ObjectMapper mapper = new ObjectMapper();
    @Override
    public User getEntity(InputStream stream) {
        User user;
        try {
            user = mapper.readValue(stream, User.class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return user;
    }

    @Override
    public String createJson(List<User> list) {
        return "";
    }
}
