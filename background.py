import torch
import torchvision.transforms as T
from PIL import Image
import requests
from io import BytesIO

import numpy as np

def find_person_location(mask):
    y_indices, x_indices = np.where(mask)
    if len(y_indices) == 0 or len(x_indices) == 0:
        return None  # Pessoa não encontrada
    x_min, x_max = x_indices.min(), x_indices.max()
    y_min, y_max = y_indices.min(), y_indices.max()
    return x_min, x_max, y_min, y_max

def crop_to_person(image, mask):
    location = find_person_location(mask)
    if location is None:
        return image  
    x_min, x_max, y_min, y_max = location
    
    width = x_max - x_min
    height = image.size[1]
    center_x = (x_max + x_min) // 2
    new_x_min = max(center_x - width // 2, 0)
    new_x_max = min(center_x + width // 2, image.size[0])
    
    return image.crop((new_x_min, 0, new_x_max, height))

def load_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image

def load_image_from_file(file_path):
    with open(file_path, 'rb') as file:
        image = Image.open(file).convert("RGB")
    return image

def load_image_from_data(image_data):
    if isinstance(image_data, str):  # Se for um caminho de arquivo
        with open(image_data, 'rb') as file:
            image = Image.open(file).convert("RGB")
    else:  # Se for dados binários (como BytesIO)
        image = Image.open(image_data).convert("RGB")
    return image

def transform_image(image):
    transform = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)

def segment(image, threshold=0.5):
    model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
    model.eval()
    input_tensor = transform_image(image)
    with torch.no_grad():
        output = model(input_tensor)['out'][0]
    output_predictions = output.argmax(0)
    mask = output_predictions.byte().cpu().numpy()
    mask = (mask == 15)
    return mask

def remove_background(image, mask):
    image = image.copy()
    image.putalpha(255)
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if not mask[y, x]:
                image.putpixel((x, y), (0, 0, 0, 0))
    return image

def add_red_background(image, mask):
    image = image.copy()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if not mask[y, x]:
                image.putpixel((x, y), (255, 0, 0)) 
    return image

def add_background_image(foreground_image, mask, background_image_url):
    background_image = load_image_from_file(background_image_url)
    background_image = background_image.resize(foreground_image.size)

    final_image = Image.new("RGBA", foreground_image.size)

    width, height = foreground_image.size
    for x in range(width):
        for y in range(height):
            if mask[y, x]: 
                final_image.putpixel((x, y), foreground_image.getpixel((x, y)))
            else: 
                final_image.putpixel((x, y), background_image.getpixel((x, y)))

    return final_image

image_url = "imagem.png"
background_image_url = "./background.png"

def getImage(image_original):
    image = load_image_from_file(image_original)
    mask = segment(image)
    image_with_background = add_background_image(image, mask, background_image_url)
    cropped_image = crop_to_person(image_with_background, mask)
    
    return cropped_image

# Mostrar a imagem resultante
# plt.imshow(cropped_image)
# plt.axis('off')
# plt.show()
# Mostrar a imagem resultante
