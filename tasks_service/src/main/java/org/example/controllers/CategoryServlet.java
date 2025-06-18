package org.example.controllers;

import org.example.entity.Category;
import org.example.mapper.JsonCategoryMapper;
import org.example.repository.CategoryRepository;
import org.example.repository.UserRepository;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@WebServlet(name = "category_servlet", value = "/category_servlet")
public class CategoryServlet extends HttpServlet {
    private final CategoryRepository repository = new CategoryRepository();
    private final UserRepository userRepository = new UserRepository();
    private final JsonCategoryMapper mapper = new JsonCategoryMapper();
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String json = mapper.createJson(repository.getByUserId(userRepository.getIdByUserName(req.getHeader("user_id"))));
        System.out.println(json);
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        PrintWriter writer = resp.getWriter();
        writer.print(json);
        writer.flush();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Category category;
        category = mapper.getEntity(req.getInputStream());
        category.setUserId(userRepository.getById(userRepository.getIdByUserName(req.getHeader("user_id"))));
        repository.save(category);
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String name = req.getHeader("name");
        byte[] decodedBytes = Base64.getDecoder().decode(name);
        name = new String(decodedBytes, StandardCharsets.UTF_8);
        repository.deleteByName(name, userRepository.getIdByUserName(req.getHeader("user_id")));
    }
}
