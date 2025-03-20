from rubpy import Client, filters, utils
from rubpy.types import Updates
import requests
import random

bot = Client(name='search_bot')

def fetch_digikala_data(query):
    url = "https://open.wiki-api.ir/apis-1/SearchDigikala"
    params = {"q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def select_random_product(data):
    if data.get("status") and data.get("results"):
        return random.choice(data["results"])
    return None

def create_caption(product):
    product_info = product.get("product", {})
    seller_info = product.get("seller", {})
    seller_status = seller_info.get("status", {})
    
    caption = (
        f"📚 **عنوان:** {product_info.get('title_fa', 'نامعلوم')}\n"
        f"💰 **قیمت:** {product_info.get('price', 0):,} تومان\n"
        f"🛒 **فروشنده:** {seller_info.get('name', 'نامعلوم')}\n"
        f"⭐ **امتیاز فروشنده:** {seller_status.get('total_rate', 0)}\n"
        f"🔗 **لینک محصول:** {product_info.get('url', '#')}"
    )
    return caption

async def send_mhaslol(update: Updates, product):
    product_info = product.get("product", {})
    image_url = product_info.get("image", [""])[0]
    caption = create_caption(product)
    if image_url:
        await update.reply_photo(image_url, caption=caption)
    else:
        await update.reply(caption)

def fetch_youtube_data(query):
    url = "https://open.wiki-api.ir/apis-1/SearchYouTube"
    params = {"q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def create_caption_video(video):
    caption = (
        f"🎥 **عنوان:** {video.get('title', 'نامعلوم')}\n"
        f"📝 **توضیحات:** {video.get('description', 'بدون توضیحات')}\n"
        f"⏳ **مدت زمان:** {video.get('duration', {}).get('timestamp', 'نامعلوم')}\n"
        f"👀 **تعداد بازدیدها:** {video.get('views', 0):,}\n"
        f"📅 **تاریخ انتشار:** {video.get('ago', 'نامعلوم')}\n"
        f"👤 **نویسنده:** [{video.get('author', {}).get('name', 'نامعلوم')}]({video.get('author', {}).get('url', '#')})\n"
        f"🔗 **لینک ویدیو:** {video.get('url', '#')}"
    )
    return caption

def select_random_video(data):
    if data.get("status") and data.get("results"):
        return random.choice(data["results"])
    return None

async def send_video(update: Updates, video):
    caption = create_caption_video(video)
    await update.reply(caption)

def fetch_aparat_data(query):
    url = "https://open.wiki-api.ir/apis-1/AparatSearch"
    params = {"q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def create_caption_aparat(video):
    caption = (
        f"🎥 **عنوان:** {video.get('title', 'نامعلوم')}\n"
        f"👤 **ارسال کننده:** {video.get('sender_name', 'نامعلوم')}\n"
        f"👀 **تعداد بازدیدها:** {video.get('visit_cnt', 0):,}\n"
        f"📅 **تاریخ انتشار:** {video.get('sdate', 'نامعلوم')}\n"
        f"⏳ **مدت زمان:** {video.get('duration', 0)} ثانیه\n"
        f"🔗 **لینک ویدیو:** {video.get('frame', '#')}"
    )
    return caption

def select_random_aparat_video(data):
    if data.get("status") and data.get("results"):
        return random.choice(data["results"])
    return None

async def send_aparat_video(update: Updates, video):
    caption = create_caption_aparat(video)
    await update.reply(caption)

@bot.on_message_updates(filters.is_private)
async def updates(update: Updates):
    query = update.text
    
    if query.startswith("+"):
        await update.reply("**در حال پردازش و سرچ محصول شما هستم...**")
        q = query.replace("+", "").strip()
        
        data = fetch_digikala_data(q)
        if data:
            product = select_random_product(data)
            if product:
                await send_mhaslol(update, product)
                print("محصول با موفقیت ارسال شد!")
            else:
                await update.reply("هیچ محصولی یافت نشد.")
        else:
            await update.reply("خطا در دریافت داده‌ها از وب‌سرویس دیجی‌کالا.")
    
    elif query.startswith("/"):
        await update.reply("**در حال سرچ و به دست آوردن اطلاعات یوتیوب هستم...**")
        q2 = query.replace("/", "").strip()
        
        data = fetch_youtube_data(q2)
        if data:
            video = select_random_video(data)
            if video:
                await send_video(update, video)
                print("ویدیو با موفقیت ارسال شد!")
            else:
                await update.reply("هیچ ویدیویی یافت نشد.")
        else:
            await update.reply("خطا در دریافت داده‌ها از وب‌سرویس یوتیوب.")
    
    elif query.startswith("*"):
        await update.reply("**در حال سرچ در آپارات هستم...**")
        q3 = query.replace("*", "").strip()
        
        data = fetch_aparat_data(q3)
        if data:
            video = select_random_aparat_video(data)
            if video:
                await send_aparat_video(update, video)
                print("ویدیو آپارات با موفقیت ارسال شد!")
            else:
                await update.reply("هیچ ویدیویی در آپارات یافت نشد.")
        else:
            await update.reply("خطا در دریافت داده‌ها از وب‌سرویس آپارات.")
    
    else:
        await update.reply("لطفاً دستور صحیح را وارد کنید. (با +، / یا * شروع کنید)")

bot.run()
