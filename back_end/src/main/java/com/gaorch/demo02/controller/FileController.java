package com.gaorch.demo02.controller;

import com.gaorch.demo02.entity.File;
import com.gaorch.demo02.service.FileService;
import com.gaorch.demo02.utils.FileUtils;
import com.gaorch.demo02.utils.Result;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import java.io.IOException;

@RestController
@RequestMapping("/file")
public class FileController {

    @Autowired
    private FileService fileService;

    @PostMapping("/upload")
    public Result upload(MultipartHttpServletRequest request) throws IOException {
        return fileService.upload(FileUtils.parse(request));
    }

    @GetMapping("/load/{id}")
    public ResponseEntity<byte[]> load(@PathVariable Integer id) throws IOException {
        return fileService.load(id);
    }

    @DeleteMapping("/{id}")
    public Result delete(@PathVariable Integer id)
    {
        return fileService.delete(id);
    }

    @GetMapping("/list/{libId}")
    public Result list(@PathVariable Integer libId)
    {
        return fileService.list(libId);
    }

}
