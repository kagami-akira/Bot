import os
import discord
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('テストボット、起動しました！'.format(client))

@client.event
async def on_message(message):

    # 音声を流す準備および音を小さく
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("Q-furi-rugi2.mp3"), volume=0.2)
    guild = client.get_guild(int(os.getenv('GUILD_ID')))

    if message.author == client.user:
        return
  
    if message.author.bot:   # メッセージ送信者がBotだった場合は無視する
        return

    if 'おはよう' in message.content :
        await message.channel.send('はい、おはようございます')

    if message.content == 'おみくじ':
        unsei = ["大吉です！", "中吉です。", "吉ですね。", "小吉です～。", "凶でした。"]
        choice = random.choice(unsei) 
        await message.channel.send('今日の運勢は……' + choice) 

# 人数取得の準備
    stagevch = client.get_channel(int(os.getenv('STAGEVCH_ID')))

    if message.content == "きゅーふりよろ":

        # ぼいちゃにいないのに呼ばれたら注意する
        if message.author.voice is None:
            await message.channel.send("ぼいちゃに入ってから呼んでください。")
            return
        # ぼいちゃに接続する
        await message.author.voice.channel.connect()
        message.guild.voice_client.play(source)
        await message.channel.send("はじまりはじまりー！")

    # 切断する準備
    if message.content == "おちていいよ":
        # botがぼいちゃにいないのに切断しようとしたら注意する
        if message.guild.voice_client is None:
            await message.channel.send("私ぼいちゃにいませんよ。")
            return

        # 切断する
        await message.guild.voice_client.disconnect()
        await message.channel.send("失礼しました～。") 

    # かぞえる
    if message.content == "人数カウント":
        # ミュートでない人カウント   
        active_list = [] #空のlistを作成
        for key, value in stagevch.voice_states.items():
            if value.self_mute == False:
                active_list.append(key)
        vch_count = len(active_list)
        # 男性カウント
        male = guild.get_role(int(os.getenv('MALE_ROLE')))
        allmale_list = male.members  #forで回すリストの中身を定義
        male_idlist = []  #空のlistを作成
        for i in range(len(allmale_list)): # 人数分繰り返す
            male_seti = allmale_list[i]
            male_idlist.append(male_seti.id)
        # 女性カウント
        female =  guild.get_role(int(os.getenv('FEMALE_ROLE')))
        allfemale_list = female.members  #forで回すリストの中身を定義
        female_idlist = []  #空のlistを作成
        for i in range(len(allfemale_list)): # 人数分繰り返す
            female_seti = allfemale_list[i]
            female_idlist.append(female_seti.id)

        maleinvch = set(male_idlist) & set(active_list)
        femaleinvch = set(female_idlist) & set(active_list)

        await message.channel.send(f'参加者は{vch_count}人です。内訳は男性{len(maleinvch)}人：女性{len(femaleinvch)}人：性別不問{vch_count - len(maleinvch) - len(femaleinvch)}人です。')       
    

    # ウェルカムメッセージ
@client.event
async def on_member_join(member):
    WelcomeChannel = client.get_channel(int(os.getenv('WELCOME_CH')))
    msg = f'{member.name}さん、ようこそいらっしゃいませ。必読１・２にはしっかり目を通してくださいね。\n おーい、' + (os.getenv('MASTER')) + '～！　お客様がお見えですよ！'
    await WelcomeChannel.send(msg)


#  入退室ログ
@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.id == (int(os.getenv('GUILD_ID'))):
        text_ch = client.get_channel(int(os.getenv('GUESTNOTE_CH')))
        if before.channel is None:
            msg = f'{member.name} が {after.channel.name} に入室しました。'
            await text_ch.send(msg)
        if after.channel is None:
            msg = f'{member.name} が {before.channel.name} から退室しました。'
            await text_ch.send(msg)


client.run(os.environ["DISCORD_TOKEN"])
