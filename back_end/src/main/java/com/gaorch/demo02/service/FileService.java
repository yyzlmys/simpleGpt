package com.gaorch.demo02.service;

import com.gaorch.demo02.entity.File;
import com.gaorch.demo02.mapper.FileMapper;
import com.gaorch.demo02.mapper.LibMapper;
import com.gaorch.demo02.utils.FileUtils;
import com.gaorch.demo02.utils.Result;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
public class FileService
{
    @Autowired
    private FileMapper fileMapper;

    @Autowired
    private LibMapper libMapper;

    public Result upload(File myFile) throws IOException {
        //windows
        java.io.File folder=new java.io.File("D:\\shixun\\" + "lib" + myFile.getLibId() + "\\");

        //linux
        //java.io.File folder=new java.io.File("/root/shixun/" + "lib" + myFile.getLibId() + "/");

        if(!folder.exists())
            folder.mkdirs();
        MultipartFile file = myFile.getFile();
        myFile.setFile(null);
        myFile.setId(0);
        fileMapper.insert(myFile);

        libMapper.updateSizeById(myFile.getSize()+libMapper.selectSizeById(myFile.getLibId()), myFile.getLibId());

        file.transferTo(new java.io.File(folder, myFile.getId()+"_"+myFile.getFileName()));
        return Result.ok();
    }

    public ResponseEntity<byte[]> load(Integer id) throws IOException {
        File file = fileMapper.getById(id);

        //win
        Path filePath = Paths.get("D:\\shixun\\" + "lib" + file.getLibId() + "\\"+file.getId()+"_"+file.getFileName());

        //linux
        //Path filePath = Paths.get("/root/shixun/" + "lib" + file.getLibId() + "/"+file.getId()+"_"+file.getFileName());

        byte[] fileBytes = Files.readAllBytes(filePath);

        // 设置 HTTP 响应头,指定文件名和内容类型
        HttpHeaders headers = new HttpHeaders();
        headers.add("Cache-Control", "no-cache, no-store, must-revalidate");
        headers.add("Pragma", "no-cache");
        headers.add("Expires", "0");
        String encodedFileName = URLEncoder.encode(file.getFileName(), StandardCharsets.UTF_8.toString());
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + encodedFileName + "\"; filename*=UTF-8''" + encodedFileName);

        // 返回 ResponseEntity,包含文件字节数组和 HTTP 响应头
        return new ResponseEntity<>(fileBytes, headers, HttpStatus.OK);
    }

    public Result delete(Integer id)
    {
        File file = fileMapper.getById(id);

        //win
        Path filePath = Paths.get("D:\\shixun\\" + "lib" + file.getLibId() + "\\"+file.getId()+"_"+file.getFileName());

        //linux
        //Path filePath = Paths.get("/root/shixun/" + "lib" + file.getLibId() + "/"+file.getId()+"_"+file.getFileName());

        libMapper.updateSizeById(libMapper.selectSizeById(file.getLibId())-file.getSize(), file.getLibId());

        java.io.File f = filePath.toFile();
        f.delete();
        fileMapper.deleteById(id);
        return Result.ok();
    }

    public Result list(Integer libId)
    {
        List<File> files = fileMapper.getByLibId(libId);
        return Result.ok(files);
    }
}









