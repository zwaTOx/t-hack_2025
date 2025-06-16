package org.example.controllers;

import org.example.mapper.JsonTaskMapper;
import org.example.repository.TaskRepository;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;

@WebServlet(name = "task_servlet", value = "/task_servlet")
public class TaskServlet extends HttpServlet {
    private final TaskRepository repository = new TaskRepository();
    private final JsonTaskMapper mapper = new JsonTaskMapper();
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String json = mapper.createJson(repository.getAll());
        System.out.println(json);
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        PrintWriter writer = resp.getWriter();
        writer.print(json);
        writer.flush();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        repository.save(mapper.getEntity(req.getInputStream()));
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        repository.update(mapper.getEntity(req.getInputStream()));
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        repository.delete(mapper.getEntity(req.getInputStream()));
    }

}
