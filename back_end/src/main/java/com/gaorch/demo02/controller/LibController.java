package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.Lib;
import com.gaorch.demo02.service.LibService;
import com.gaorch.demo02.utils.FileUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.servlet.resource.ResourceUrlEncodingFilter;

import java.io.IOException;

@RestController
@RequestMapping("/lib")
public class LibController {
    @Autowired
    private LibService libService;


    @PostMapping("")
    public Result create(@RequestBody Lib lib) {
        return libService.create(lib);
    }

    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id)
    {
        return libService.delete(id);
    }

    @GetMapping("")
    public Result list()
    {
        return libService.list();
    }

    @GetMapping("/get/{id}")
    public Result get(@PathVariable Integer id)
    {
        return libService.get(id);
    }
}
