package org.example.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.mapper.JsonTaskMapper;
import org.example.repository.TaskRepository;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

@WebServlet(name = "task_category", value = "/task_category")
public class TaskCategory extends HttpServlet {
    private final TaskRepository taskRepository = new TaskRepository();
    private final JsonTaskMapper mapper = new JsonTaskMapper();
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String name = req.getHeader("name");
        byte[] decodedBytes = Base64.getDecoder().decode(name);
        name = new String(decodedBytes, StandardCharsets.UTF_8);
        String json = mapper.createJson(taskRepository.getByCategory(name, Long.valueOf(req.getHeader("user_id"))));
        System.out.println(json);
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        PrintWriter writer = resp.getWriter();
        writer.print(json);
        writer.flush();
    }
}
