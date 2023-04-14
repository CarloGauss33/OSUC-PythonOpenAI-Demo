import os
import sys
import cv2

class CameraManager:
    def __init__(self, storage_folder_path="captures", camera_id=0) -> None:
        self.storage_folder_path = storage_folder_path
        self.camera_id = camera_id
        self.camera = cv2.VideoCapture(self.camera_id)
        self.find_or_create_storage_folder()

    def find_or_create_storage_folder(self):
        if not os.path.exists(self.storage_folder_path):
            os.mkdir(self.storage_folder_path)

    def take_picture(self, file_name="capture.jpg"):
        ret, frame = self.camera.read()
        cv2.imwrite(os.path.join(self.storage_folder_path, file_name), frame)
        return os.path.join(self.storage_folder_path, file_name)

    def take_video(self, video_duration_seconds=5, file_name="capture.mp4"):
        # Este codigo da lo mismo. Esta verboso porque no me dio el tiempo :sad:

        camera_frame_rate = self.camera.get(cv2.CAP_PROP_FPS)
        video_frame_rate = 20
        video_frame_size = (int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_file_path = os.path.join(self.storage_folder_path, file_name)
        video_writer = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*"mp4v"), video_frame_rate, video_frame_size)
        for i in range(int(camera_frame_rate * video_duration_seconds)):
            ret, frame = self.camera.read()
            video_writer.write(frame)
        video_writer.release()
        return

    def list_images(self):
        return os.listdir(self.storage_folder_path)

    def list_videos(self):
        return os.listdir(self.storage_folder_path)

    def release_camera(self):
        self.camera.release()
        cv2.destroyAllWindows()
        return