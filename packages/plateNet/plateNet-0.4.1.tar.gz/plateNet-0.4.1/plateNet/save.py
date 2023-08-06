import json
import urllib.request
import xml.etree.cElementTree as ET

import cv2
import numpy as np
import requests
from ISR.models import RDN
from PIL import Image
from plateNet.folder import generateOutputFolder
from plateNet.tools import getTime


class Saver:

    def __init__(self, imagePath, savefolder="plates"):
        self.imagePath = imagePath
        self.savefolder = savefolder
        self.mainPath, self.filename = generateOutputFolder(imagePath, savefolder)

    def saveJSON(self, boxes, confidence):
        json_fileName = "{}/{}.json".format(self.mainPath, self.filename)
        boxes = {
            'Date': getTime(),
            'File': "{}".format(self.imagePath),
            'Confidence': confidence,
            'X': boxes[0],
            'Y': boxes[1],
            'W': boxes[2],
            'H': boxes[3]
        }
        with open(json_fileName, 'w') as json_file:
            json.dump(boxes, json_file, ensure_ascii=False, indent=4)

    def saveXML(self, boxes, confidence):
        xml_fileName = "{}/{}.xml".format(self.mainPath, self.filename)

        root = ET.Element("PlateNet")
        features = ET.SubElement(root, "features")

        ET.SubElement(features, "Date", name="detect time").text = getTime()
        ET.SubElement(features, "File", name="input image").text = self.imagePath
        ET.SubElement(features, "Confidence", name="confidence").text = str(confidence)

        position = ET.SubElement(features, "position")
        ET.SubElement(position, "X", name="x coord").text = str(boxes[0])
        ET.SubElement(position, "Y", name="y coord").text = str(boxes[1])
        ET.SubElement(position, "W", name="width").text = str(boxes[2])
        ET.SubElement(position, "H", name="height").text = str(boxes[3])

        tree = ET.ElementTree(root)
        tree.write(xml_fileName)

    def savePNG(self, img):
        if img is not None:
            imgName = "{}/{}.png".format(self.mainPath, self.filename)
            self.__ISR(img, imgName)

    def __SRGAN(self, img, name):
        headers = {
            'api-key': '851d198d-097b-4885-bc5b-20c0b86f689f',
        }

        cv2.imwrite(name, img)

        files = {
            'image': open(name, "rb"),
        }

        response = requests.post('https://api.deepai.org/api/torch-srgan', headers=headers, files=files)
        url = response.json()["output_url"]

        urllib.request.urlretrieve(url, name)

    def __ISR(self, img, name):
        height,width = img.shape[:2]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        lr_img = np.array(img)

        rdn = RDN(arch_params={'C': 6, 'D': 20, 'G': 64, 'G0': 64, 'x': 2})
        rdn.model.load_weights('plateNet-448/rdn-C6-D20-G64-G064-x2_ArtefactCancelling_epoch219.hdf5')
        # rdn.model.load_weights('app/plateNet-448/rdn-C6-D20-G64-G064-x2_ArtefactCancelling_epoch219.hdf5')

        sr_img = rdn.predict(lr_img)
        res = Image.fromarray(sr_img)
        new_height = 100
        new_width = int(new_height * width/ height)
        res = res.resize((new_width,new_height),Image.ANTIALIAS)
        res.save(name)

    # def saver(currentImg,plate,boxes):

    # savePNG(main_path,currentImg,plate)
    # saveJSON(main_path,currentImg,boxes[0])
