# mask2shp
## 描述
Mask RCNN输出结果（即mask）转shapefile文件，这是核心代码。
看看demo就应该知道了怎么用，放在你的mask rcnn代码的文件夹里面就可以了，输入图像是带有地理坐标的tiff图像，也就是geotiff格式。

## 算法
主要方法就是:  
1. 用轮廓检测算法得到mask的边界点  
2. 将它转成写入geom对象  
3. 将图面坐标转成地理坐标  
4. 写入shapefile。  
这里尤为需要注意的是图面坐标转地理坐标的过程，涉及到一些专业领域的知识，主要是投影坐标系的参数。参加[地图投影](https://en.wikipedia.org/wiki/Map_projection)

## 最后
对代码有问题可以提出，或者联系yuhuachang@csu.edu.cn
