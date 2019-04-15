import os
import sys
import skimage.io
import coco
from mrcnn import visualize
from mrcnn import model as modellib
from tools import geo_convert as geo
from osgeo import gdal

ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR)

PRETRAINED_MODEL_PATH = os.path.join(ROOT_DIR, "data/pretrained_weights.h5")
LOGS_DIRECTORY = os.path.join(ROOT_DIR, "logs")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 5
    NUM_CLASSES = 1 + 1
    IMAGE_MAX_DIM = 320
    IMAGE_MIN_DIM = 320


config = InferenceConfig()
config.display()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model_path = PRETRAINED_MODEL_PATH
model.load_weights(model_path, by_name=True)

# 测试模型
class_names = ['BG', 'building']  # 这里只设置了一个背景值和一个建筑物，所以模型只能识别建筑物

file_name = 'D:/codes/python/BuildingDetectMaster/data/test_tiff/s32.TIF'  # 输入的tiff图像
test_image = skimage.io.imread(file_name)

predictions = model.detect([test_image] * config.BATCH_SIZE,
                           verbose=1)
p = predictions[0]

# 存储为shapefile
masks = p['masks']
save_name = 'D:/codes/python/RS_Test/a.shp'  # 输出路径
data_tiff = gdal.Open(file_name)
ref = data_tiff.GetGeoTransform()
geom = geo.create_geom_from_rcnnmask(masks, reference=ref)
geo.convert_geom_to_shp(geom, outputfile_name=save_name)

# 图像显示
visualize.display_instances(test_image, p['rois'], p['masks'], p['class_ids'],
                            class_names, p['scores'])
