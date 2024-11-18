from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import API_ID, API_HASH, admin
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import pytz
import os
import json
import datetime
import random

# دل انمی مشکل داره
if os.path.exists("data"):
    if os.path.exists("data/chatactions"):
        if os.path.exists("data/textformats"):
            pass
else:
    os.mkdir("data")
    os.mkdir("data/chatactions")
    os.mkdir("data/textformats")

# text format
with open("data/textformats/bold.txt", "w") as bold:
    bold.write("off")
# actions
with open("data/chatactions/typing.txt", "w") as type:
    type.write("off")
with open("data/chatactions/playing.txt", "w") as play:
    play.write("off") 
with open("data/chatactions/recordvideo.txt", "w") as video:
    video.write("off")
with open("data/chatactions/speaking.txt", "w") as speak:
    speak.write("off")
# ////times
with open("timename.txt", "w") as timename:
    timename.write("off")
# //////
with open("savepv.txt", "w") as savepv:
    savepv.write("off")
# ////
with open("tsave.txt", "w") as tsave:
    tsave.write("off")
# ////
# with open("enemy.txt", "w") as e:
#     e.write("off")
# ////
with open("crashlist.txt", "w") as crash:
    crash.write("off")
with open("love.txt", "w") as lve:
    lve.write("off")

amir = Client(
    "MetaSelf",
    api_id=API_ID,
    api_hash=API_HASH
)

crashemojis = ["❤️", "🥰", "🌚", "🍓", "💋"]
crashlist = []
# enemylist = []
# FoshList = [
#     'کیرم تو رحم اجاره ای و خونی مالی مادرت حاضرم',
#     ' دو میلیون شبی پول ویلا بدم تا مادرتو تو گوشه کناراش بگام و اب کوسشو بریزم کف خونه تا فردا صبح کارگرای افغانی برای نظافت اومدن با بوی اب کس مادرت بجقن و ابکیراشون نثار قبر مرده هات بشه',
#     'آخه احمق مادر کونی من کس مادرت گذاشتم تو بازم داری کسشر میگی',
#     ' کیرم تا تخمدانش تو کس مادرت بی سطح خار کسه انقدسرعتت پایینه خستم کردی کیرمو جاساز کردم تو کس چرب مادرت به قول والدفری ک الان قیافشو یادم نمیاد میگفت هر شمشیر یه قلاف میخواد ولی قافل از این ک کیر من مثل گرز رستمه و کس مادرت مثل قلاف چاقو دستی پس کیر تو ناموست ',
#     'قراره به مادرت به سهمگین ترین شکل ممکن تجاوز کنم و توی فاحشه ی نتی و هرزه ی متصل به اینترنت جهانی و بین الملل بیای توی اپلیکیشن تلگرام بگی نخوندم',
#     'مرسی فک میکنی میخونم این اراجیف خزتو احمق مادر جنده من مادرتو دارم میکشم تو واسه من پنج خط تکس پر می‌کنی خز ممبر دوساعتع رو تایپی این کسشرا چیه میگی آخه کیرم تو سطح گوهت',
#     'وقتی کیرمو نشون مادرت دادم سوار پراید ۷۹ شد و باهاش شبانه روز تاخت تا کیلومتر ها از من دور بشه ولی قافل از این بود ک من سوار سوزوکی ۱۰۰۰ بودم و تا روز قیامت مادرتو تعقیب کردم ریدم پراید هفتاد نه سکو با لانچیکو بزنی سوار پراید ۸۲ نمیشه احمق با پراید مدل ۷۹ میرم تو کس ننت تا مثل یه ماشین زمان عمل کنه',
#     'اتحادی خر ممبر این اراجیف چیه می‌نویسی آخه کیرم تو ناموس پاموست با زبون مثل موتور برقم میافتم به کس مادرت و لیسای عمیق میزنم و اب کوسشو را میندازم ',
#     'ببین مادرت که اینجاس ببینم زبون درازی میکنم همین الان از کس دارش میزنم تگ مگ چیه خارکسته ی ولد موش حاصل زنای خرس گریزلی با مادرت مگه مثل توی مادر پیچ گوشتی داگ اتحادیم سگ افغان با اسم گوه و کمترین داشته های زندگی و بی همه چیز بودن کیر تو همه کست همه کس کونی تو دوساعت باقی‌موندش سینه های گوشتالوی ',
#     'مادرتو میگیرم تو دستمو میمالم و دهنمو چفت کوس مادرت میکنم و مثل همیشه و مثل یه لیسر قهار زبون میندازم به چوچول سیاه مادرت و یکاری میکنم صدای اه و نالش کل ۷ اسمونو برداره ',
#     'ای کس ننت مادر جنده که انقد خری که داری از خایه هام بالامیری مادر جنده کیرم به پهنا تو کس مادرت دارم با کس ننت بازی میکنم تو داری جق میزنی با پورنایی که از مادرت فرسادم واست بیناموس کیرم تو ناموست فیلم ابد و یک روز بره تو کس ننه ی هرکی تماشاش کرده خارکسته فقط بنرشو یبار تو سینما دیدم مادر خر مگ مثل توی کسته ناموس خزم برم فیلمای گوه ایرانیارو نیگا کنم مادر سکسچتر کفتر مادر کلاغ بیاد نوک بزنه تو کس ننت مادرکسته میدونم جلوی تکسام داری کم میاری و به پته پته افتادی ولی گوه تو کس ناموست من دست بردار نیستم و امپولای ادمای انسولینی رو میکنم تو کس ننتآخه کس ننت گذاشتم که انقد فشاری شدی واسه من ده خط پر می‌کنی اتحادی خر ممبر کس ننتو گاییدم بعد شروع میکنی کسشر گفتن مثل شکلاتای فرمند که دو رنگن با مادرت ترکیب میشم و میدم پدر بی غیرتت بخوره خارکسته پول نداری چیه مادر خر اندازه حقوق یه ماه بابای کارگر فقیرت فقط خرج شورت و سوتینای مادرت میکنم ک موقع سکس هرشب پارشون میکنم و به خورد مادرت میدم ببین بابات انقد بی غیرته که داره اینجا با کس ننت ور می‌ره من دارم فیلم میگیرم دست از سر خایه هام بردار کسکش پدر خدازده بی ابرو سیک کن دلقک با اون ایموجی خز که یه مش بچ سال عنشو دراوردن اتحادی چیه خارکسته به مادرت غذا نمیدم تا قند مغزش بیاد پایین و جوش بیاره و همین ک عصبانی شد کیرمو بکنم تک دهنش تا خفه خون بگیدخ اموجی تو کص ننت رفته مقدس شده واسم پسر کونی نهایت ۱۶ سالن باشه نبینم واسه من قد علم کنی که کس مادرتو با همین چاقو اینجا پاره میکنم کس ننت بگیدخ چیه لرز چیه داش وقتی میترسی مادرت راحت تر کسش باز میشه کیرمو میکنم تو کس ناموست و با رمز عملیاتی ک الان تو خاطرم نیست به مادرت یورش میبرم خر مادر تا اعتراف نکنی مادرت به اعماق اقیانوس ارام پیوسته دست از سر کچل بابای بی غیرتت برنمیدارم آخه کیرم تو سطح کوهت سر ناموست شرط بستم مادر جنده کس ننت کیرم تو ناموست مادربَرده خسته نمیشی اتقد دلقک بازی درمیاری کودکستانی خارکسته ترس مرس تو کارم نیست و مثل یه شیر میافتم به جون پستونای بلوری مادرت و میمیکم و میمیکم ابکیرمو خالی میکنم رو سنگ قبر مشکی بابای خدابیامرزت مادرت پورن استاره میدونستی؟ زشته انقد بی غیرتی جای این که از زیر پل جمعش کنی نشستی با فحاشی های بچه سالانه صورت مسعله رو پاک میکنی خارکسته اینجا حق بت زدن نداری کجکی ناموس پوسته گوجه ناموس میرم تو کسه مادرت درم نمیبندم کیرم تو خار مادرت مادر جنده من کس ننتو دارم با اشتهای کاذب میخورم تو داری به کس ننت میخندی کیرم تو رحم اجاره ای و خونی مالی مادرت حاضرم دو میلیون شبی پول ویلا بدم تا مادرتو تو گوشه کناراش بگام و اب کوسشو بریزم کف خونه'
# ]

async def Timename():
    with open("timename.txt", "r") as timename:
        times = timename.read()
    
    if times == "on":
        time = pytz.timezone("Asia/Tehran")
        now = datetime.datetime.now(time)
        await amir.update_profile(last_name=now.strftime("%H:%M"))
    
scheduler = AsyncIOScheduler()
scheduler.add_job(Timename, "interval", seconds=1)

async def love():
    with open("timebio.txt", "r") as time:
        lovemod = time.read()

    if lovemod == "on":
        time = pytz.timezone("Asia/Tehran")
        now = datetime.datetime.now(time)
        print(now.strftime("%H:%M"))

@amir.on_message(filters.user(admin))
async def test(client: Client, event: Message):
    e = event.text
    await BoldFormat(client, event)
    # actions
    if e.lower() == "typing on":
        with open("data/chatactions/typing.txt", "w") as type:
            type.write("on")
            await event.edit("**Typing Mode is On!**")
    elif e.lower() == "typing off":
        with open("data/chatactions/typing.txt", "w") as type:
            type.write("off")
            await event.edit("**Typing Mode is Off!**")
    # text format
    elif e.lower() == "bold on":
        with open("data/textformats/bold.txt", "w") as bold:
            bold.write("on")
            await event.edit("**Bold mode is On!**")

    elif e.lower() == "bold off":
        with open("data/textformats/bold.txt", "w") as bold:
            bold.write("off")
            await event.edit("**Bold mode is Off!**")

    elif e.lower() == "playing on":
        with open("data/chatactions/playing.txt", "w") as p:
            p.write("on")
            await event.edit("**Playing Mode action is On!**")

    elif e.lower() == "playing off":
        with open("data/chatactions/playing.txt", "w") as p:
            p.write("off")
            await event.edit("**Playing Mode action  is Off!**")

    elif e.lower() == "raudio on":
        with open("data/chatactions/reacordaudio.txt", "w") as record:
            record.write("on")
            await event.edit("**Record Audio action is on!**")

    elif e.lower() == "raudio off":
        with open("data/chatactions/reacordaudio.txt", "w") as record:
            record.write("off")
            await event.edit("**Record Audio action is off!**")

    elif e.lower() == "rvideo off":
        with open("data/chatactions/recordvideo.txt", "w") as video:
            video.write("off")
            await event.edit("**Record vido action is off!**")

    elif e.lower() == "rvideo on":
        with open("data/chatactions/recordvideo.txt", "w") as video:
            video.write("on")
            await event.edit("**Record video action is on!**")

    elif e.lower() == "speaking off":
        with open("data/chatactions/speaking.txt", "w") as speak:
            speak.write("off")
            await event.edit("**Speaking action off**")

    elif e.lower() == "speaking on":
        with open("data/chatactions/speaking.txt", "w") as speak:
            speak.write("on")
            await event.edit("**Speaking action on**")

    elif e.lower() == "timename off":
        with open("timename.txt", "w") as timename:
            timename.write("off")
            await event.edit("**Time Name Mode is Off!")

    elif e.lower() == "timename on":
        with open("timename.txt", "w") as timename:
            timename.write("on")
            await event.edit("**Time Name Mode is On!**")

    elif e.lower() == "savepv off":
        with open("savepv.txt", "w") as savepv:
            savepv.write("off")
            await event.edit("**Save Pv Mode is Off!**")

    elif e.lower() == "savepv on":
        with open("savepv.txt", "w") as savepv:
            savepv.write("on")
            await event.edit("**Save Pv Mode is On!**\n Save items in your SavedMassages")

    elif e.lower() == "tsave off":
        with open("tsave.txt", "w") as tsave:
            tsave.write("off")
            await event.edit("**Tsave Mode is Off!**")

    elif e.lower() == "tsave on":
        with open("tsave.txt", "w") as tsave:
            tsave.write("on")
            await event.edit("**Tsave Mode is On!**\n Save items in your SavedMassages")
            
    # elif e.lower() == "setenemy":
    #     if event.reply_to_message:
    #         userid = event.reply_to_message.from_user.id
    #         with open("enemy.txt", "w") as en:
    #             if userid not in enemylist:
    #                 enemylist.append(userid)
    #                 json.dump(enemylist, en)
    #                 await event.edit("**User Added Enemy List!**")
    #     else:
    #         await event.edit("**Please Reply to User**")

    # elif e.lower == "delenemy":
    #     if event.reply_to_message:
    #         userid = event.reply_to_message.from_user.id
    #         with open("enemy.txt", "w") as en:
    #             if userid in enemylist:
    #                 en.write("off")
    #                 await event.edit("**User Removed From Enemy List!**")
        # else:
        #     await event.edit("**Please Reply to User**")
    elif e.lower() == "addcrash":
        if event.reply_to_message:
            userid = event.reply_to_message.from_user.id
            with open("crashlist.txt", "w") as crash:
                crash.write("on")
                crashlist.append(userid)
                await event.edit("**User Added to Crash List**")
        else:
            await event.edit("**Please Reply To User**")

    elif e.lower() == "bot":
        await event.edit(f"""**[Bos is Online..](tg://user?id=)**""")
    elif e.lower() == "help":
        await event.edit("**اطلاع از آنلاین بودن ربات:**\n `ping`\n**فعال کردن اکشن تایپینگ:**\n `typing on` | `typing off`\n**فعال کردن اکشن درحال بازی:**\n `playing on` | `playing off`\n**حالت ضبط صدا:**\n`raudio on` | `raudio off`\n**حالت ضبط ویدیو:**\n`rvideo on` | `rvideo off`\n**تبدیل کردن متن به بولد:**\n`bold on` | `bold off`")
    elif e.lower() == "id" and event.reply_to_message:
        message = event.reply_to_message.from_user.id
        name = event.reply_to_message.from_user.mention
        await event.edit(text=f"[`{message}` - **{name}**]")

@amir.on_message()
async def workever(client: Client, event: Message):
    user = event.from_user.id
    # actions
    love()
    with open("data/chatactions/playing.txt", "r") as p:
        Playing = p.read()
    with open("data/chatactions/typing.txt", "r") as t:
        typing = t.read()
    with open("data/chatactions/reacordaudio.txt", "r") as audio:
        recordaudio = audio.read()
    with open("data/chatactions/recordvideo.txt", "r") as video:
        recordvideo = video.read()
    with open("data/chatactions/speaking.txt", "r") as speak:
        speaking = speak.read()
    with open("savepv.txt", "r") as savepv:
        savepv1 = savepv.read()
    with open("tsave.txt", "r") as tsave:
        tsave2 = tsave.read()
    with open("crashlist.txt", "r") as crash:
        crashinfo = crash.read()

    if typing == "on":
        await amir.send_chat_action(chat_id=event.chat.id, action=enums.ChatAction.TYPING)
    if Playing == "on":
        await amir.send_chat_action(chat_id=event.chat.id, action=enums.ChatAction.PLAYING)
    if recordaudio == "on":
        await amir.send_chat_action(chat_id=event.chat.id, action=enums.ChatAction.RECORD_AUDIO)
    if recordvideo == "on":
        await amir.send_chat_action(chat_id=event.chat.id, action=enums.ChatAction.RECORD_VIDEO)
    if speaking == "on":
        await amir.send_chat_action(chat_id=event.chat.id, action=enums.ChatAction.SPEAKING)
    if savepv1 == "on":
        await amir.forward_messages(chat_id=admin, from_chat_id=event.chat.id, message_ids=event.id)
    if tsave2 == "on":
        if event.photo:
            await event.download("photo.jpg")
            await amir.send_photo(chat_id=admin, photo="downloads/photo.jpg", caption=f"**Destroy Photo Saved!**\n info: {event.from_user.id}")
            os.remove("downloads/photo.jpg")
        elif event.video:
            await event.download("video.mp4")
            await amir.send_video(chat_id=admin, video="downloads/video.mp4", caption=f"**Destroy Video Saved!**\n info: {event.from_user.id}")
            os.remove("downloads/video.mp4")
        elif event.voice:
            await event.download("voice.mp3")
    if crashinfo == "on":
        if user in crashlist:
            await amir.send_reaction(chat_id=event.chat.id, message_id=event.id, emoji=random.choice(crashemojis))

async def BoldFormat(client, event):
    with open("data/textformats/bold.txt", "r") as b:
        bold = b.read()

    if bold == "on":
        await client.edit_message_text(chat_id=event.chat.id, message_id=event.id, text=f"<b>{event.text}</b>")

print("Bot is Starting...")
scheduler.start()
amir.run()
