FROM python:3.10.7
USER root

WORKDIR /app
COPY . /app

RUN pip install --upgrade -r /app/requirements.txt # pythonのライブラリはrequirements.txtに記述します。

RUN apt-get update # ffmpegをビルド済みバイナリでinstallします。
RUN apt-get install -y ffmpeg

CMD ["python", "main.py"]
