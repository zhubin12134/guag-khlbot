import io
from PIL import Image, ImageDraw, ImageFont

from config.common import settings

class ImageProcessor:

    def merge_avatar_with_meme(self, background_img_bytes, overlay_img_bytes, position=(20, 410)):
        background_img = Image.open(io.BytesIO(background_img_bytes))
        overlay_img = Image.open(io.BytesIO(overlay_img_bytes))

        new_size = (80, 80)
        overlay_img = overlay_img.resize(new_size, Image.BILINEAR)

        mask = Image.new('L', new_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, new_size[0], new_size[1]), fill=255)
        overlay_img.putalpha(mask)

        # 设置叠加位置（左上角为原点）
        position = position  # 在背景图上放置的位置

        # 将叠加图片粘贴到背景图片上
        background_img.paste(overlay_img, position, overlay_img)

        output_byte_io = io.BytesIO()
        background_img.save(output_byte_io, format='JPEG')  # 修改格式

        # 从 BytesIO 对象中获取字节数据
        image_bytes = output_byte_io.getvalue()

        return image_bytes

    def add_text_to_image(self, img_bytes: bytes, text: str, position=(0, 0)):
        background_img = Image.open(io.BytesIO(img_bytes))

        # 在图片上添加文字
        draw = ImageDraw.Draw(background_img)
        text = text  # 要添加的文字内容

        # 选择字体和字号
        font_path = settings.font  # 字体文件路径
        font_size = 40

        font = ImageFont.truetype(font_path, font_size)

        # 指定文字的位置（左上角为原点）
        text_position = position  # 要添加文字的位置

        # 指定文字颜色
        text_color = (255, 255, 255)  # 白色

        # 添加文字到图片
        draw.text(text_position, text, font=font, fill=text_color)

        output_byte_io = io.BytesIO()
        background_img.save(output_byte_io, format='JPEG')  # 修改格式

        # 从 BytesIO 对象中获取字节数据
        image_bytes = output_byte_io.getvalue()

        return image_bytes
