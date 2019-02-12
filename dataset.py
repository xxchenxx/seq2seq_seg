from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
from glob import glob 
import os.path as osp

default_transforms = transforms.Compose([
    transforms.Resize((256,448)),
    transforms.ToTensor()
])

class YoutubeDataset(Dataset):

    def __init__(self, seq_len=5, split="train", base_dir='/raid/sunfangwen/wzh/youtube/', transforms = default_transforms):

        self.dir_list = open(split + "_dir.txt").readlines()
        self.base_dir = base_dir
        self.pathset = []
        self.transforms = transforms
        for a in self.dir_list:
            j, m = a.replace("\n", "").split(' ')
            full_path_j = osp.join(self.base_dir, j, "*.png")
            full_path_m = osp.join(self.base_dir, m, "*.jpg")
            m_path = sorted(glob(full_path_m))
            j_path = sorted(glob(full_path_j))
            for i in range(len(m_path) - seq_len + 1):
                self.pathset.append((j_path[i:i + seq_len], m_path[i:i + seq_len]))

    def __getitem__(self, idx):

        j_path, m_path = self.pathset[idx]
        j = []
        m = []
        for jp in j_path:
            img = Image.open(jp)
            img = self.transforms(img)
            j.append(img)
        for mp in m_path:
            img = Image.open(mp)
            img = self.transforms(img)
            m.append(img)
        return j, m

    def __len__(self):
        return len(self.pathset)


if __name__ == '__main__':
    dataset = YoutubeDataset()
    print(len(dataset))
    for (j,m) in dataset:
        print(j.shape)
        break