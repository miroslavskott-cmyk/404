// apps/bot/src/bot.js
const { Telegraf, Markup } = require('telegraf');
const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
    ctx.reply(`مرحباً ${ctx.from.first_name}! 🚀\nاستخدم المحلل الذكي لتوقع نتائج اليوم.`, 
    Markup.inlineKeyboard([
        [Markup.button.webApp("📊 فتح تطبيق التحليل", process.env.WEBAPP_URL)],
        [Markup.button.callback("💎 اشتراك VIP", "buy_vip")]
    ]));
});

// لوحة تحكم المالك (أنت)
bot.command('admin', (ctx) => {
    // يمكنك إضافة أوامر هنا لتوليد مفاتيح يدوية
    ctx.reply("Owner Dashboard: Welcome Boss.");
});

bot.launch();
