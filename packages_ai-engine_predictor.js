// packages/ai-engine/predictor.js
const calculatePower = (stats) => {
    return (stats.attack * 0.3) + (stats.form * 0.4) + (stats.h2h * 0.2) + (stats.homeAdv * 0.1);
};

const getPrediction = (homeTeam, awayTeam) => {
    const hPower = calculatePower(homeTeam);
    const aPower = calculatePower(awayTeam);
    
    const total = hPower + aPower;
    const win = ((hPower / total) * 100).toFixed(1);
    const loss = ((aPower / total) * 100).toFixed(1);
    const draw = (100 - (parseFloat(win) + parseFloat(loss))).toFixed(1);

    return {
        win, draw, loss,
        confidence: Math.max(win, loss),
        recommendation: win > 60 ? "Safe: Home" : win > 45 ? "Medium: 1X" : "High Risk"
    };
};

module.exports = { getPrediction };
