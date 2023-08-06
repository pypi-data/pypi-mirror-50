import torch


class Dataset(torch.utils.data.Dataset):
    """Characterizes a dataset for PyTorch"""
    def __init__(self, x, y):
        """Initialization"""
        self.x = torch.from_numpy(x.values).float()
        self.y = torch.from_numpy(y.values).float()

    def __len__(self):
        """Denotes the total number of samples"""
        return len(self.x)

    def __getitem__(self, index):
        """Generates one sample of data"""
        x = self.x[index]
        y = self.y[index]

        return x, y