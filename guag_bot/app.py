import random
import os
import aiohttp
import aiofiles
import asyncio


from exte.Register import command
from exte.Message import Messags
from exte.CardMessage import Card
from exte.Musc import Musc
from exte.Ps import ImageProcessor
from config.common import settings


@command(name="ping")
async def test(msg: Messags):
    await msg.send_channel_message("鸡尼太妹", quote=True)


@command(name="test-1")
async def test1(msg: Messags):
    await msg.send_channenl_image("六花.jpeg")


@command(name="test-2")
async def test2(msg: Messags, text):
    if users := msg.mentions:
        user = users[0]
        id = user.id
        usernmae = user.username
        avatar = user.avatar
        await msg.send_channel_message("id: {}, username: {}, avatar: {}".format(id, usernmae, avatar))


@command(name="test-3")
async def test3(msg: Messags):
    await msg.send_channel_card("还在开发中")


@command(name="来")
async def come(msg: Messags):
    channel_id = await msg.void_channel_id
    print(channel_id)
    if channel_id:
        settings.channel_id = channel_id
        await msg.send_channel_message(f"频道: {settings.channel_id}")
    else:
        await msg.send_channel_message(f"请先进入一个频道")


@command(name="点歌")
async def test4(msg: Messags, music: str):
    await msg.add_playlist(Musc(music))
    await msg.send_channel_message(f"播放中: {music}")


@command(name="本地")
async def local_play(msg: Messags, music: str):
    if not os.path.exists(os.path.join(settings.music_path, music)):
        await msg.send_channel_message("本地没有这首歌")
    else:
        await msg.add_playlist(Musc(music))
        await msg.send_channel_message(f"添加到播放列表: {music}")


@command(name="列表")
async def play_list(msg: Messags):
    if settings.music_play:
        list2str = [f"{index + 1}, {value}" for index, value in enumerate(settings.music_play[:15])]
        await msg.send_channel_message("\n".join(list2str))
    else:
        await msg.send_channel_message("没有歌了")
    


@command(name="本地列表")
async def local_list(msg: Messags):
    local_musc_list = filter(lambda file: (not file.startswith("_")) and (file.endswith(".mp3")), os.listdir(settings.music_path))
    list2str = '\n'.join(list(local_musc_list))
    await msg.send_channel_message(list2str)


@command(name="切歌")
async def cut(msg: Messags):
    settings.cut = True
    await msg.send_channel_message(f"切歌中")
    await asyncio.sleep(5)
    if len(settings.music_play) == 0:
        await msg.send_channel_message("后面没有歌了")
        settings.cut = False



@command(name="歌单")
async def playlist(msg: Messags, sheet):
    if sheet == "阿态":
        tail_sheet = os.listdir(settings.music_path)
        random.shuffle(tail_sheet)
        for music_name in tail_sheet:
            settings.music_list.append(Musc(music_name))
        await msg.send_channel_message("添加成功")


@command(name="清空歌单")
async def clear_playlist(msg: Messags):
    settings.music_list.clear()
    settings.music_play.clear()
    await msg.send_channel_message("已清空")


@command(name="wyy")
async def test2(msg: Messags, music: str):
    await msg.send_channel_message("还在开发中")


@command(name="爬")
async def hanler(msg: Messags, met: str):
    if users := msg.mentions:
        user = users[0]
        avatar = user.avatar
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar) as resp:
                data = await resp.content.read()

                images_list = list(filter(lambda x: x.endswith(".jpeg") and x.startswith("爬"), os.listdir("images")))
                image_random = random.choice(images_list)

                async with aiofiles.open(os.path.join(settings.image_path, image_random), "rb") as file:
                    img_hanler = ImageProcessor()
                    result = img_hanler.merge_avatar_with_meme(await file.read(), data)
                    await msg.send_channenl_image_byte(result)



@command(name="鲁迅说")
async def luxun_image(msg: Messags, text: str):
    async with aiofiles.open(f"{settings.image_path}/鲁迅说.jpeg", "rb") as file:
        img_hanler = ImageProcessor()
        result = img_hanler.add_text_to_image(await file.read(), text=text, position=(18, 405))
        await msg.send_channenl_image_byte(result)


@command(name="麦克说")
async def mike_image(msg: Messags, text: str):
    async with aiofiles.open(f"{settings.image_path}/麦克说.jpeg", "rb") as file:
        img_hanler = ImageProcessor()
        result = img_hanler.add_text_to_image(await file.read(), text=text, position=(13, 478))
        await msg.send_channenl_image_byte(result)


@command(name="六花")
async def help(msg: Messags):
    text = """欢迎使用六花酱多功能G7人
1. 发送鲁迅表情包： +鲁迅说 不是我说的
2. 发送麦克表情包： +麦克说 不是我说的
3. 发送爬表情包: +爬 @用户
4. 绑定语音频道: +来
5. 播放服务器上的歌曲,需要先绑定语音频道： +本地 歌名
6. 切歌: +切歌
7. 列表: +播放列表
8. ping: +ping
todo:
各大主流音乐平台播放
"""
    await msg.send_channel_message(text)