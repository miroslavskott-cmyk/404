// apps/api/src/modules/payments/service.js
const crypto = require('crypto');

const generateLicenseKey = (userId) => {
    // توليد مفتاح عشوائي فريد
    return `VETO-${crypto.randomBytes(3).toString('hex').toUpperCase()}-${userId.slice(-3)}`;
};

const verifyAccess = (userId, providedKey, userDb, botToken) => {
    // 1. شرط المالك: توكن البوت هو المفتاح المطلق
    if (providedKey === botToken) return { status: 'OWNER', access: true };

    // 2. شرط المستخدم: فحص قاعدة البيانات
    const user = userDb[userId];
    if (user && user.vip && new Date() < new Date(user.expiry)) {
        return { status: 'VIP', access: true };
    }
    return { status: 'FREE', access: false };
};

module.exports = { generateLicenseKey, verifyAccess };
