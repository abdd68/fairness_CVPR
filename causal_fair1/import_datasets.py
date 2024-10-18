from torch.utils.data import Dataset
from PIL import Image
import numpy as np
import os

class MimicCXRDataset(Dataset):
    def __init__(self, metadata, root_dir, transform=None):
        # self.metadata = metadata.dropna(subset=["study_id", "subject_id", "Pneumonia", "gender"]).reset_index(drop=True)
        # self.metadata = self.metadata[self.metadata["Pneumonia"] != -1].reset_index(drop=True)
        self.metadata = metadata.fillna({"Pneumonia": 0, "gender": 0}).reset_index(drop=True)
        self.metadata["Pneumonia"] = self.metadata["Pneumonia"].replace(-1, 0)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        # 获取影像文件路径
        study_id = int(self.metadata.iloc[idx]["study_id"])
        subject_id = int(self.metadata.iloc[idx]["subject_id"])

        # 构造图像文件路径，例如：root_dir/p10/p10000032/s50414267/*.jpg
        subject_folder = f"p{str(subject_id)[:2]}"
        study_folder = f"p{subject_id}/s{study_id}"
        image_path = os.path.join(self.root_dir, "files", subject_folder, study_folder)

        # 加载图像（假设图像文件夹下有 jpg 文件）
        image_files = [f for f in os.listdir(image_path) if f.endswith('.jpg')]
        image = Image.open(os.path.join(image_path, image_files[0])).convert('RGB')  # 加载第一张图像

        # 应用变换
        if self.transform:
            image = self.transform(image)

        # 提取肺炎标签和性别信息
        pneumonia_label = int(self.metadata.iloc[idx]["Pneumonia"])  # 转换为整数类型
        gender_label = np.float32(self.metadata.iloc[idx]["gender"])  # 转换为整数类型

        return image, pneumonia_label, gender_label
    