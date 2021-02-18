from PIL import Image
import pyocr
import pyocr.builders
import cv2
import numpy as np

def render_doc_text(file_path):

    # ツール取得
    pyocr.tesseract.TESSERACT_CMD = 'C:/Users/hi_tu/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # 画像取得
    img = cv2.imread(file_path, 0)
    # 必要に応じて画像処理 線を消す
    ret, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
    img = cv2.bitwise_not(img)
    label = cv2.connectedComponentsWithStats(img)
    data = np.delete(label[2], 0, 0)
    new_image = np.zeros((img.shape[0], img.shape[1]))+255
    for i in range(label[0]-1):
        if 0 < data[i][4] < 1000:
            new_image = np.where(label[1] == i+1, 0, new_image)

    # ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    cv2.imwrite('sample_edited.png', new_image)
    img = Image.fromarray(new_image)

    # OCR
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img, lang="jpn", builder=builder)

    # 結果から空白文字削除
    data_list = [text for text in result.split('\n') if text.strip()]
    data_list

    return data_list
