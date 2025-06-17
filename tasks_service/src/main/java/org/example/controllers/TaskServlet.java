package org.example.controllers;

import liquibase.Contexts;
import liquibase.LabelExpression;
import liquibase.Liquibase;
import liquibase.Scope;
import liquibase.database.Database;
import liquibase.database.DatabaseFactory;
import liquibase.database.jvm.JdbcConnection;
import liquibase.resource.ClassLoaderResourceAccessor;
import org.example.entity.Task;
import org.example.mapper.JsonTaskMapper;
import org.example.repository.CategoryRepository;
import org.example.repository.TaskRepository;
import org.example.repository.UserRepository;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

@WebServlet(name = "task_servlet", value = "/task_servlet")
public class TaskServlet extends HttpServlet {
    private final TaskRepository taskRepository = new TaskRepository();
    private final UserRepository userRepository = new UserRepository();
    private final CategoryRepository categoryRepository = new CategoryRepository();
    private final JsonTaskMapper mapper = new JsonTaskMapper();
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String json = mapper.createJson(taskRepository.getByUserId(Long.valueOf(req.getHeader("user_id"))));
        System.out.println(json);
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
        PrintWriter writer = resp.getWriter();
        writer.print(json);
        writer.flush();
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Task entity = mapper.getEntity(req.getInputStream());
        entity.setCategory(categoryRepository.getById(Long.valueOf(req.getHeader("category_id"))));
        entity.setUserId(userRepository.getById(Long.valueOf(req.getHeader("user_id"))));
        taskRepository.save(entity);
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        taskRepository.update(mapper.getEntity(req.getInputStream()));
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String name = req.getHeader("name");
        byte[] decodedBytes = Base64.getDecoder().decode(name);
        name = new String(decodedBytes, StandardCharsets.UTF_8);
        taskRepository.deleteByName(name, Long.valueOf(req.getHeader("user_id")));
    }

//    @Override
//    public void init() throws ServletException {
//        Map<String, Object> config = new HashMap<>();
//        try { Connection connection = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres",
//                "postgres", "password");
//            Scope.child(config, () -> {
//                Database database = DatabaseFactory
//                        .getInstance().findCorrectDatabaseImplementation(new JdbcConnection(connection));
//
//                Liquibase liquibase = new liquibase.Liquibase("liquibase/changelog.yml", new ClassLoaderResourceAccessor(), database);
//                liquibase.update(new Contexts(), new LabelExpression());
//            });
//            connection.close();
//        } catch (Exception e) {
//            throw new RuntimeException(e);
//        }
//    }
}
