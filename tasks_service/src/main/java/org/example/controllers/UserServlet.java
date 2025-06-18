package org.example.controllers;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.example.entity.User;
import org.example.mapper.JsonMapper;
import org.example.mapper.JsonUserMapper;
import org.example.repository.UserRepository;

@WebServlet(name = "user_servlet", value = "/user_servlet")
public class UserServlet extends HttpServlet {
    private final UserRepository repository = new UserRepository();
    JsonMapper<User> mapper = new JsonUserMapper();
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        User user;
        user = mapper.getEntity(req.getInputStream());
        repository.save(user);
    }
}
