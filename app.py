import os
import gradio as gr
import torch
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights

weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def image_classifier(image):
    inputs = transform(image)
    inputs = inputs.unsqueeze(0)
    with torch.no_grad():
        prediction = model(inputs).squeeze(0).softmax(0)
    class_id = prediction.argmax().item()
    score = prediction[class_id].item()
    category_name = weights.meta["categories"][class_id]
    return f"{category_name}: {100 * score}%"


img_widget = gr.Image(image_mode='RGB', type='pil')
app = gr.Interface(fn=image_classifier, inputs=img_widget,
                   outputs='label', flagging_mode='never')

server_port = int(os.environ.get("AWS_LAMBDA_HTTP_PORT", 8080))
app.launch(server_name='0.0.0.0', server_port=server_port)
