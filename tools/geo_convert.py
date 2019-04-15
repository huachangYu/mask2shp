"""
将mask rcnn转成shapefile的一些函数
"""

from osgeo import ogr, gdal, osr
import cv2
import numpy as np


def create_geom():
    """用于测试，生成一个wkt"""
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    polygon.AddGeometry(ring)
    multipolygon.AddGeometry(polygon)
    polygon1 = ogr.Geometry(ogr.wkbPolygon)
    ring1 = ogr.Geometry(ogr.wkbLinearRing)
    ring1.AddPoint(1214704.933941905, 641092.8288590391)
    ring1.AddPoint(1228580.428455506, 682719.3123998424)
    ring1.AddPoint(1218405.0658121984, 721108.1805541387)
    ring1.AddPoint(1214704.933941905, 641092.8288590391)
    polygon1.AddGeometry(ring1)
    multipolygon.AddGeometry(polygon1)
    return multipolygon


def reference_of_tiff(input_tiff_path):
    """
    获取给定tiff图像的地理坐标系和投影坐标系
    :param input_tiff_path: tiff图像的路径
    :return: 投影坐标系，地理坐标系
    """
    tiff_data = gdal.Open(input_tiff_path)
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(tiff_data.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs


def convert_geom_to_shp(input_geo, outputfile_name='untitled.shp', geo_type='multipolygon', spatialref=None):
    """
    仅支持multipolygon类型转shapefile
    :param spatialref: 空间参考坐标系，osr.SpatialReference()类型
    :param outputfile_name: 输出文件的名字
    :param input_geo: wkt格式的polygon
    :return: 
    """
    if spatialref is None:
        spatialref = osr.SpatialReference()
        spatialref.ImportFromEPSG(4326)
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if geo_type == 'multipolygon':
        geometry_count = input_geo.GetGeometryCount()
        output_shpfile = driver.CreateDataSource(outputfile_name)
        dstlayer = output_shpfile.CreateLayer("layer", spatialref, geom_type=ogr.wkbMultiPolygon)
        for i in range(geometry_count):
            polygon = input_geo.GetGeometryRef(i)
            feature = ogr.Feature(dstlayer.GetLayerDefn())
            feature.SetGeometry(polygon)
            dstlayer.CreateFeature(feature)
            # feature.Destroy()
            # output_shpfile.Destroy()


def convert_xy_from_img_to_geo(x, y, reference=None):
    """
    将图上坐标转成地理坐标或者投影坐标
    :param x: 计算机中的x,应该是列
    :param y: 计算机中的y，应该是行
    :param reference: GDAL的六参数，可以通过dataset.GetGeoTransform()获取，
    		这里的dataset = gdal.Open(file_name) file_name表示tif格式图片的路径，带坐标的tiff格式
    :return: 
    """
    row = y
    col = x
    px = reference[0] + col * reference[1] + row * reference[2]
    py = reference[3] + col * reference[4] + row * reference[5]
    return px, py


def create_geom_from_rcnnmask(masks, reference=None):
    num_masks = masks.shape[-1]
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for i_mask in range(num_masks):
        mask = 255 * masks[:, :, i_mask]
        gray = mask.astype(np.uint8)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for index in range(0, len(contours)):
            polygon.Empty()
            ring.Empty()
            contour = contours[index]
            for i in range(contour.shape[0]):
                x, y = 1.0 * contour[i, 0, 0], 1.0 * contour[i, 0, 1]
                x, y = convert_xy_from_img_to_geo(x, y, reference)
                ring.AddPoint(x, y)
            ring.CloseRings()
            if ring.GetPointCount() > 4:  # 这个消除了一个bug
                polygon.AddGeometry(ring)
                multipolygon.AddGeometry(polygon)
    return multipolygon


"""if __name__ == '__main__':
    poly = create_geom()
    print(poly.ExportToWkt())
    print(poly.GetGeometryCount())
    print(poly.GetGeometryRef(1))
    tiff_path = 'D:/codes/python/RS_Test/test.tif'
    prosrs, geosrs = reference_of_tiff(tiff_path)
    convert_geom_to_shp(poly, spatialref=geosrs)
"""
