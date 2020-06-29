# mask2shp
## 用途
目标检测模型（如Mask RCNN）输出结果（即mask）转shapefile文件  
图像分割模型(如unet、inception v3)等模型的输出结果转geotiff图像

## 使用
*输入*：是带有地理坐标的tiff图像，也就是geotiff格式的图像
*输出图像*：shapefile或者geotiff

## 算法
主要方法就是:  
1. 用轮廓检测算法得到mask的边界点  
2. 将它转成写入geom对象  
3. 将图面坐标转成地理坐标  
4. 写入shapefile。  
这里尤为需要注意的是图面坐标转地理坐标的过程，涉及到一些专业领域的知识，主要是投影坐标系的参数。参加[地图投影](https://en.wikipedia.org/wiki/Map_projection)
