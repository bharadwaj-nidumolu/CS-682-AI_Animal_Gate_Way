import os

import torch
import torchvision
import os
import shutil
import random
from sklearn.metrics import classification_report, f1_score

class PrepareData():

    def __init__(self):
        self. keywords = ['Abyssinian', 'Bengal', 'Birman', 'Bombay',
        'British Shorthair', 'Egyptian Mau', 'Maine Coon', 'Persian',
        'Ragdoll', 'Russian Blue', 'Siamese', 'Sphynx']


    def removeDogData(self):

        directory_path = 'images'
        all_files = os.listdir(directory_path)
        filtered_files = [file for file in all_files if any(keyword.lower() in file.lower() for keyword in self.keywords)]

        for file in all_files:
            if file not in filtered_files:
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)

    def cleanTrainTestNameFile(self, file_path):

        with open(file_path, 'r') as file:
            lines = file.readlines()

        filtered_lines = [line for line in lines if any(keyword.lower() in line.lower() for keyword in self.keywords)]

        with open(file_path, 'w') as file:
            file.writelines(filtered_lines)

    def trainTestSplitBasedOnFile(self):

        image_folder = 'images'

        test_file_path = 'test.txt'
        eval_file_path = 'trainval.txt'

        train_folder = 'train'
        test_folder = 'test'
        eval_folder = 'eval'

        for folder in [train_folder, test_folder, eval_folder]:
            os.makedirs(folder, exist_ok=True)

        train_ratio = 0.7
        test_ratio = 0.15
        val_ratio = 0.15



        # Iterate through each class
        for cat_class in self.keywords:
            # Get the list of images for the current class
            class_images = [file for file in os.listdir(image_folder) if file.startswith(f"{cat_class}_")]

            # Shuffle the list of images for randomness
            random.shuffle(class_images)

            # Calculate the split points based on the ratios
            train_split = int(len(class_images) * train_ratio)
            test_split = int(len(class_images) * (train_ratio + test_ratio))

            # Split the images into train, test, and validation sets
            train_images = class_images[:train_split]
            test_images = class_images[train_split:test_split]
            val_images = class_images[test_split:]

            # Move the images to their respective folders
            for image in train_images:
                shutil.move(os.path.join(image_folder, image), os.path.join(train_folder, image))

            for image in test_images:
                shutil.move(os.path.join(image_folder, image), os.path.join(test_folder, image))

            for image in val_images:
                shutil.move(os.path.join(image_folder, image), os.path.join(eval_folder, image))


    def splitData(self, folderName):

        original_folder = folderName

        organized_folder = 'Data/'+ folderName

        os.makedirs(organized_folder, exist_ok=True)

        for cat_class in self.keywords:
            # Create a subfolder for the current class
            class_folder = os.path.join(organized_folder, cat_class)
            os.makedirs(class_folder, exist_ok=True)

            # Get the list of images for the current class
            class_images = [file for file in os.listdir(original_folder) if file.startswith(f"{cat_class}_")]

            # Move the images to the class subfolder
            for image in class_images:
                source_path = os.path.join(original_folder, image)
                destination_path = os.path.join(class_folder, image)
                shutil.move(source_path, destination_path)


class ModelHead(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, n_classes):
        super(ModelHead, self).__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu2 = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(hidden_dim // 2, n_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

#prepareData = PrepareData()
#prepareData.removeDogData()
#prepareData.trainTestSplitBasedOnFile()
#prepareData.splitData('train')
#prepareData.splitData('test')
#prepareData.splitData('valid')



classifier = torchvision.models.resnet50(pretrained=True)
classifier.fc = ModelHead(input_dim=2048, hidden_dim=1024, n_classes=12)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}.')

# Transformations
transform_rotation = torchvision.transforms.RandomApply([
    torchvision.transforms.RandomRotation(20)
], p=0.2)

transform_train = torchvision.transforms.Compose([
    torchvision.transforms.Resize(256),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.RandomPerspective(distortion_scale=0.1, p=0.2),
    transform_rotation,
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

transform_valid = torchvision.transforms.Compose([
    torchvision.transforms.Resize(256),
    torchvision.transforms.CenterCrop(224),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

# DataLoaders
TRAIN_DATA_DIR = 'Data/train'
VALID_DATA_DIR = 'Data/valid'
TEST_DATA_DIR = 'Data/test'

BATCH_SIZE = 32

train_data = torchvision.datasets.ImageFolder(TRAIN_DATA_DIR,
                                              transform=transform_train,
                                              is_valid_file=lambda x: x.endswith('.jpg'))

valid_data = torchvision.datasets.ImageFolder(VALID_DATA_DIR,
                                              transform=transform_valid,
                                              is_valid_file=lambda x: x.endswith('.jpg'))

test_data = torchvision.datasets.ImageFolder(TEST_DATA_DIR,
                                             transform=transform_valid,
                                             is_valid_file=lambda x: x.endswith('.jpg'))

train_data_loader = torch.utils.data.DataLoader(
    train_data,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
)

valid_data_loader = torch.utils.data.DataLoader(
    valid_data,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
)

test_data_loader = torch.utils.data.DataLoader(
    test_data,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
)


model = torchvision.models.resnet50(pretrained=True).to(device)

# freeze the backbone
for parameter in model.parameters():
    parameter.requires_grad = False


class ModelHead(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, n_classes):
        super(ModelHead, self).__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu2 = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(hidden_dim // 2, n_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x


model.fc = ModelHead(2048, 1024, 12)
model.fc.to(device)

# Training
MODEL_SAVE_PATH = 'checkpoints'

LEARNING_RATE = 1e-3
N_EPOCHS = 10

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)


def train(model, n_epochs, criterion, optimizer, train_data_loader, valid_data_loader,
          device, model_save_path, logging_interval: int = 50):
    best_valid_f1_score = 0.0
    os.makedirs(model_save_path, exist_ok=True)

    for epoch in range(n_epochs):
        # training step
        model.train()

        for batch_idx, (batch_data, batch_labels) in enumerate(train_data_loader):
            inputs = batch_data.to(device)
            y_true = batch_labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimizer step
            y_pred = model(inputs)
            loss = criterion(y_pred, y_true)
            loss.backward()
            optimizer.step()

            if (batch_idx + 1) % logging_interval == 0:
                print(f'Epoch: {epoch + 1}\t| Batch: {batch_idx + 1}\t| Loss: {loss}')

        # validation step
        model.eval()
        y_true = []
        y_pred = []
        for valid_data, valid_labels in valid_data_loader:
            valid_data = valid_data.to(device)
            valid_labels = valid_labels.to(device)
            with torch.no_grad():
                valid_preds = model(valid_data)
            valid_pred_labels = torch.argmax(valid_preds, dim=1)
            y_true.extend(valid_labels.detach().cpu().numpy())
            y_pred.extend(valid_pred_labels.detach().cpu().numpy())
        valid_f1_score = f1_score(y_true, y_pred, average='macro')

        if valid_f1_score > best_valid_f1_score:
            best_valid_f1_score = valid_f1_score
            torch.save(model.state_dict(),
                       os.path.join(model_save_path, 'best_checkpoint.pth'))
        print(f'Epoch {epoch + 1} F1-score: {valid_f1_score}\t| Best F1-score: {best_valid_f1_score}')
        torch.save(model.state_dict(),
                   os.path.join(model_save_path, f'epoch_{epoch + 1}_checkpoint.pth'))


train(model, N_EPOCHS, criterion, optimizer,
      train_data_loader, valid_data_loader,
      device, MODEL_SAVE_PATH)

# Testing
model.load_state_dict(torch.load(os.path.join(MODEL_SAVE_PATH, 'best_checkpoint.pth')))
model.eval()

y_true = []
y_pred = []
for test_data, test_labels in test_data_loader:
    test_data = test_data.to(device)
    test_labels = test_labels.to(device)
    with torch.no_grad():
        test_preds = model(test_data)
    test_pred_labels = torch.argmax(test_preds, dim=1)
    y_true.extend(test_labels.detach().cpu().numpy())
    y_pred.extend(test_pred_labels.detach().cpu().numpy())

print(classification_report(y_true, y_pred))
