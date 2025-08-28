import os
import csv
import live2d.v3 as live2d
import pygame
import cv2
import logging
from pygame.locals import *
from OpenGL.GL import *
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger("live2d")



class EmoModel:
    def __init__(self, model_path):
        logger.debug(f"New EmoModel object with model path {model_path}")
        if os.path.exists(model_path):
            self.model_path = model_path
        else:
            logger.warning(f"Model path {model_path} not found")
            self.model_path = "emotion_data.csv"
        self.model = []
        for row in csv.DictReader(open(self.model_path)):
            self.model.append(row)
        self.emotion_list = []
        for count in range(len(self.model)):
            self.emotion_list.append(self.model[count]["emotion"])

    def get_emo(self, emotion):
        return_data = []
        index = self.emotion_list.index(emotion)
        # 修复：正确遍历字典项
        for key, value in self.model[index].items():
            if key != "emotion":
                return_data.append(float(value))  # 转换为浮点数
        if len(return_data) > 0:
            logger.debug(f"Get emotion {emotion}:{return_data}")
            return return_data
        else:
            logger.warning(f"Get emotion {emotion} failed")
            return self.get_emo(self.emotion_list[0])


class ActionModel:
    def __init__(self, model_path):
        logger.debug(f"New ActionModel object with model path {model_path}")
        if os.path.exists(model_path):
            self.model_path = model_path
        else:
            logger.warning(f"Model path {model_path} not found")
            self.model_path = "action_data.csv"
        self.model = []
        for row in csv.DictReader(open(self.model_path)):
            self.model.append(row)
        self.action_list = []
        for count in range(len(self.model)):
            self.action_list.append(self.model[count]["action"])

    def get_action(self, action):
        return_data = []
        index = self.action_list.index(action)
        # 修复：正确遍历字典项
        for key, value in self.model[index].items():
            if key != "action":
                return_data.append(float(value))  # 转换为浮点数
        if len(return_data) > 0:
            logger.debug(f"Get action {action}:{return_data}")
            return return_data
        else:
            logger.warning(f"Get action {action} failed")
            return self.get_action(self.action_list[0])


class Live2d:
    def __init__(self, width=800, height=800, cam_id=-1, l2d_model=None, bg_color=(0, 0, 0), l2d_design_w=None,
                 l2d_design_h=None, emo_model_path="emotion_data.csv", act_model_path="action_data.csv"):
        self.emotion = "neutral"
        self.action = "idle"
        self.running = False
        if not l2d_design_h:
            self.l2d_design_w = width
        else:
            self.l2d_design_w = l2d_design_w
        if not l2d_design_w:
            self.l2d_design_h = height
        else:
            self.l2d_design_h = l2d_design_h
        logger.debug("New Live2d object")
        self.l2d_model_path = l2d_model  # 保存模型路径
        self.cam_id = cam_id
        self.bg_color = bg_color

        pygame.init()
        live2d.init()
        self.display = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        logger.info("Live2d initialized")
        self.emotion_model = EmoModel(emo_model_path)
        logger.info('Emotion Model loaded')
        self.emos = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3,
                     'sad': 4, 'surprise': 5, 'neutral': 6}
        self.action_model = ActionModel(act_model_path)
        logger.info('Action Model loaded')
        self.actions = {"hello": 0, "nod": 1, "shake": 2, "wave": 3, "idle": 4}

        # 初始化Live2D模型
        if l2d_model and os.path.isfile(l2d_model):
            if live2d.LIVE2D_VERSION == 3:
                try:
                    live2d.glInit()
                except AttributeError:
                    logger.warning("glInit failed, trying glewInit...")
                    live2d.glewInit()
            self.model = live2d.LAppModel()
            self.model.LoadModelJson(l2d_model)
            self.model.SetAutoBreathEnable(True)
            self.model.SetAutoBlinkEnable(True)
            logger.info(f"Live2D model loaded: {l2d_model}")
        else:
            self.model = None
            logger.warning("No Live2D model loaded")

        self.running = True
        logger.info("Camera initialized")
        if self.cam_id >= 0:
            self.cam = cv2.VideoCapture(cam_id)
            if not self.cam.isOpened():
                logger.error(f"Camera {cam_id} not found")
                return
            logger.info(f"Using camera {cam_id}")
        elif self.cam_id == -1:
            logger.info("Auto find camera")
            cam_list = list_cameras()
            if not cam_list:
                logger.error("Camera not found")
                self.cam_id = -2
                return
            self.cam = cv2.VideoCapture(list_cameras()[0])
            if not self.cam.isOpened():
                logger.error(f"Camera {list_cameras()[0]} not found")
                return
            logger.info(f"Using camera {list_cameras()[0]}")
        elif self.cam_id == -2:
            pass

    def update(self):
        logger.debug("Update")
        # 处理事件
        if self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

            if self.cam_id >= -1:
                self.update_camera()
            elif self.cam_id == -2:
                self.update_background()
            self.update_l2d()
            pygame.display.flip()

            if not self.running:
                logger.info("Stopped")
        else:
            logger.debug("Don't init")

    def init(self):
        self.running = True

    def update_background(self):
        """绘制纯色背景"""
        glClearColor(self.bg_color[0] / 255.0, self.bg_color[1] / 255.0, self.bg_color[2] / 255.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def update_camera(self):
        ret, frame = self.cam.read()
        if not ret:
            logger.warning("Camera read failed")
            return

        # 转成 RGB 并垂直翻转
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 0)

        h, w = frame.shape[:2]
        win_w, win_h = self.display.get_size()

        # 计算缩放比例（保持比例）
        scale = max(win_w / w, win_h / h)
        new_w, new_h = int(w * scale), int(h * scale)

        # 缩放画面
        frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # 计算裁剪区域（居中）
        x = (new_w - win_w) // 2
        y = (new_h - win_h) // 2
        frame = frame[y:y + win_h, x:x + win_w]

        # 确保尺寸正确
        frame = cv2.resize(frame, (win_w, win_h))

        # OpenGL 显示
        glEnable(GL_TEXTURE_2D)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, win_w, win_h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, win_w, 0, win_h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(win_w, 0)
        glTexCoord2f(1, 1)
        glVertex2f(win_w, win_h)
        glTexCoord2f(0, 1)
        glVertex2f(0, win_h)
        glEnd()

        glDeleteTextures([texture_id])

    def update_l2d(self):
        if not self.model:
            return

        win_w, win_h = self.display.get_size()
        design_w, design_h = self.l2d_design_w, self.l2d_design_h

        # 计算居中位置（保持比例，不拉伸）
        scale = min(win_w / design_w, win_h / design_h)
        view_w, view_h = int(design_w * scale), int(design_h * scale)
        offset_x = (win_w - view_w) // 2
        offset_y = (win_h - view_h) // 2

        glViewport(offset_x, offset_y, view_w, view_h)

        live2d.clearBuffer()
        self.model.SetOffset(0, -2)
        self.model.SetScale(3)

        self.model.Update()
        self.model.Draw()

    def set_emotion(self, emo):
        if emo not in self.emos:
            return
        if not self.model:
            logger.warning("No Live2D model loaded")
            return
        params = self.emotion_model.get_emo(emo)
        # Live2D 官方参数范围
        self.model.SetParameterValue('ParamEyeLOpen', params[0])
        self.model.SetParameterValue('ParamEyeROpen', params[1])
        self.model.SetParameterValue('ParamEyeLSmile', params[2])
        self.model.SetParameterValue('ParamEyeRSmile', params[3])
        self.model.SetParameterValue('ParamBrowLY', params[4])
        self.model.SetParameterValue('ParamBrowLX', params[5])
        self.model.SetParameterValue('ParamBrowRY', params[6])
        self.model.SetParameterValue('ParamBrowRX', params[7])
        self.model.SetParameterValue('ParamMouthOpenY', params[8])
        self.model.SetParameterValue('ParamMouthForm', params[9])
        self.model.SetParameterValue('ParamHeadZ', params[10])
        self.model.SetParameterValue('ParamHeadX', params[11])
        self.model.SetParameterValue('ParamHeadY', params[12])
        logger.debug(f'Emotion {emo} applied')

    def set_action(self, action):
        if action not in self.actions:
            logger.warning(f"Action {action} not found")
            return
        if not self.model:
            logger.warning("No Live2D model loaded")
            return
        params = self.action_model.get_action(action)
        self.model.SetParameterValue('ParamAngleX', params[0] * 30)
        self.model.SetParameterValue('ParamAngleY', params[1] * 30)
        self.model.SetParameterValue('ParamAngleZ', params[2] * 30)
        self.model.SetParameterValue('ParamBodyAngleX', params[3] * 10)
        self.model.SetParameterValue('ParamBodyAngleY', params[4] * 10)
        self.model.SetParameterValue('ParamBodyAngleZ', params[5] * 10)
        self.model.SetParameterValue("ParamArmLA", params[6] * 30)
        self.model.SetParameterValue("ParamArmRA", params[7] * 30)
        self.model.SetParameterValue("ParamArmLB", params[8] * 30)
        self.model.SetParameterValue("ParamArmRB", params[9] * 30)
        self.model.SetParameterValue("ParamHandL", params[10] * 10)
        self.model.SetParameterValue("ParamHandR", params[11] * 10)
        logger.debug(f'Action {action} applied')

    def load_lip_sync_data(self, wav_file_path):
        """
        加载WAV文件用于唇形同步
        :param wav_file_path: WAV文件路径
        """
        try:
            if os.path.exists(wav_file_path):
                # 使用WavHandler处理WAV文件
                self.lip_sync_index = 0
                self.lip_sync_enabled = True
                logger.info(f"Lip sync data loaded from {wav_file_path}")
                return True
            else:
                logger.warning(f"WAV file not found: {wav_file_path}")
                return False
        except Exception as e:
            logger.error(f"Error loading lip sync data: {e}")
            return False

    def stop_lip_sync(self):
        """
        停止唇形同步
        """
        self.lip_sync_enabled = False
        self.lip_sync_data = None
        self.lip_sync_index = 0
        # 重置口型参数
        if self.model:
            self.model.SetParameterValue(self.lip_sync_param, 0.0)
        logger.info("Lip sync stopped")

    def set_lip_sync_param(self, param_name):
        """
        设置唇形同步参数名称
        :param param_name: 参数名称
        """
        self.lip_sync_param = param_name
        logger.debug(f"Lip sync parameter set to {param_name}")



def list_cameras():
    """列出所有可用的摄像头"""
    index = 0
    cam_list = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            cam_list.append(index)
        index += 1
    if len(cam_list) == 0:
        return False
    return cam_list


if __name__ == "__main__":
    import time, random

    a = Live2d(l2d_model=r"D:\live2d\youmanyou_vts\youmanyou.model3.json")
    a.init()
    emo_list = ["happy", "angry", "disgust", "fear", "neutral", "sad", "surprise"]
    while a.running:
        a.set_action("hello")
        a.set_emotion(emo_list[random.randint(0, len(emo_list) - 1)])
        for x in range(0, 100):
            a.update()
            time.sleep(0.01)
