package com.gaorch.demo02.utils;

import com.gaorch.demo02.entity.File;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;

public class FileUtils {
    public static File parse(MultipartHttpServletRequest request) throws UnsupportedEncodingException {
        MultipartFile file = request.getFile("file");
        Integer libId = Integer.valueOf(request.getParameter("libId"));
        String file_name = file.getOriginalFilename();
        file_name = URLDecoder.decode(file_name, "UTF-8");

        long fileSizeInBytes = file.getSize();
        double fileSizeInKB = (double) fileSizeInBytes / (1024*1024);

        File myfile = new File();
        myfile.setFile(file);
        myfile.setLibId(libId);
        myfile.setFileName(file_name);
        myfile.setType(getFileType(file));
        myfile.setSize(fileSizeInKB);

        return myfile;
    }

    public static String getFileType(MultipartFile file) {
        String contentType = file.getContentType();
        if (contentType != null) {
            // 根据 MIME 类型映射到常见的文件扩展名
            switch (contentType) {
                case "application/pdf":
                    return "pdf";
                case "text/plain":
                    return "txt";
                case "image/jpeg":
                    return "jpg";
                case "image/png":
                    return "png";
                case "application/msword":
                case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    return "doc";
                case "application/vnd.ms-excel":
                case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    return "xls";
                case "application/vnd.ms-powerpoint":
                case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                    return "ppt";
                default:
                    return "unknown";
            }
        } else {
            return "unknown";
        }
    }
}
