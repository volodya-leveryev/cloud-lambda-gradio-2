# Базовый образ
FROM public.ecr.aws/docker/library/python:3.14-slim
# Добавляем файлы из другого образ
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:1.1.0 /lambda-adapter /opt/extensions/lambda-adapter
# Рабочий каталог
WORKDIR /app
# Копируем исходный код в образ
COPY app.py ./
# Установка пакетов при сборке образа
RUN python -m pip install --upgrade pip gradio
RUN pip install --index-url https://download.pytorch.org/whl/cpu torchvision
# Команда для запуска контейнера
CMD ["python3", "app.py"]
