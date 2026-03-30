from flask import Flask, render_template_string
import random
import datetime

app = Flask(__name__)

results = []
test_creatives = [
    "AI微习惯教练：每天推送30秒个性化微习惯视频，根据用户日程和情绪自动调整。",
    "老人AI故事机：输入孙子名字+兴趣，AI生成睡前互动故事+语音。",
    "城市隐藏美食地图：AI根据用户口味+实时天气，生成只属于你的3条美食路线。",
    "职场AI谈判助手：输入谈判场景，AI实时生成话术+语气建议。",
    "可持续穿搭AI：用户拍衣橱照片，AI生成30天零浪费穿搭计划。"
]

HTML = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能链经济 MVP</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f0f23; color: #fff; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header { text-align: center; padding: 40px 0; border-bottom: 1px solid #333; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { color: #888; }
        .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; margin-top: 30px; }
        .card { background: #1a1a2e; border-radius: 16px; padding: 24px; }
        .card h2 { margin-bottom: 20px; font-size: 1.2em; color: #00d4ff; }
        textarea { width: 100%; height: 120px; background: #16213e; border: 1px solid #333; border-radius: 8px; color: #fff; padding: 12px; font-size: 14px; resize: none; }
        textarea:focus { outline: none; border-color: #00d4ff; }
        select { width: 100%; background: #16213e; border: 1px solid #333; border-radius: 8px; color: #fff; padding: 10px; margin: 10px 0; }
        button { width: 100%; background: linear-gradient(135deg, #00d4ff, #0099cc); border: none; border-radius: 8px; color: #fff; padding: 14px; font-size: 16px; cursor: pointer; margin-top: 15px; transition: transform 0.2s; }
        button:hover { transform: scale(1.02); }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
        .stat { background: #16213e; padding: 20px; border-radius: 12px; text-align: center; }
        .stat-value { font-size: 2em; font-weight: bold; color: #00d4ff; }
        .stat-label { color: #888; font-size: 0.9em; }
        .result { background: #16213e; border-radius: 12px; padding: 20px; margin-top: 20px; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .result-value { color: #00ff88; font-size: 1.5em; font-weight: bold; }
        .metrics { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: 15px 0; }
        .metric { background: #0f0f23; padding: 15px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 1.3em; font-weight: bold; }
        .metric-label { color: #888; font-size: 0.8em; }
        .content-box { background: #0f0f23; padding: 15px; border-radius: 8px; white-space: pre-wrap; font-size: 13px; line-height: 1.6; margin-top: 15px; }
        .tags { display: flex; gap: 10px; margin-top: 10px; }
        .tag { background: #333; padding: 5px 12px; border-radius: 20px; font-size: 0.8em; }
        .tag.pass { background: #00ff8833; color: #00ff88; }
        .tag.score { background: #00d4ff33; color: #00d4ff; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔗 智能链经济 MVP</h1>
            <p class="subtitle">内容链模式 - 人类注入创意，AI自主运行</p>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>📝 提交创意</h2>
                <textarea id="creative" placeholder="输入你的商业创意..."></textarea>
                <select id="presets" onchange="selectPreset()">
                    <option value="">-- 选择预设创意 --</option>
                    {% for c in creatives %}
                    <option value="{{ c }}">{{ c[:30] }}...</option>
                    {% endfor %}
                </select>
                <button onclick="submitCreative()">🚀 执行创意</button>
                
                <div style="margin-top: 30px;">
                    <h2>📊 数据概览</h2>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-value">{{ stats.total }}</div>
                            <div class="stat-label">总创意</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{{ stats.rate }}%</div>
                            <div class="stat-label">通过率</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">¥{{ stats.avg }}</div>
                            <div class="stat-label">平均价值</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📋 执行结果</h2>
                <div id="result-area">
                    {% if last %}
                    <div class="result">
                        <div class="result-header">
                            <span class="tags">
                                <span class="tag pass">✅ 通过</span>
                                <span class="tag score">评分: {{ last.assessment.score }}</span>
                            </span>
                            <span class="result-value">¥{{ last.value.estimated }}</span>
                        </div>
                        <div class="metrics">
                            <div class="metric"><div class="metric-value">{{ last.metrics.views }}</div><div class="metric-label">浏览</div></div>
                            <div class="metric"><div class="metric-value">{{ last.metrics.likes }}</div><div class="metric-label">点赞</div></div>
                            <div class="metric"><div class="metric-value">{{ last.metrics.comments }}</div><div class="metric-label">评论</div></div>
                            <div class="metric"><div class="metric-value">{{ last.metrics.shares }}</div><div class="metric-label">分享</div></div>
                            <div class="metric"><div class="metric-value">{{ last.metrics.conversion }}%</div><div class="metric-label">转化</div></div>
                        </div>
                        <div style="color:#888;margin-top:10px;">生成内容:</div>
                        <div class="content-box">{{ last.generated }}</div>
                        <div style="color:#888;margin-top:15px;">规模化潜力: <span style="color:#00d4ff">¥{{ last.value.scale }}</span></div>
                    </div>
                    {% else %}
                    <p style="color:#666;text-align:center;padding:40px;">👈 提交创意开始执行</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let creatives = {{ creatives|tojson }};
        
        function selectPreset() {
            const select = document.getElementById('presets');
            if (select.value) document.getElementById('creative').value = select.value;
        }
        
        async function submitCreative() {
            const creative = document.getElementById('creative').value;
            if (creative.length < 15) { alert('创意太短了'); return; }
            
            const btn = document.querySelector('button');
            btn.textContent = '执行中...';
            btn.disabled = true;
            
            const res = await fetch('/api/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({creative})
            });
            const data = await res.json();
            location.reload();
        }
    </script>
</body>
</html>
'''

def execute_creative(creative):
    score = random.randint(60, 95)
    if len(creative) < 15 or "测试" in creative:
        return None
    
    metrics = {
        "views": random.randint(800, 3500),
        "likes": random.randint(45, 320),
        "comments": random.randint(8, 65),
        "shares": random.randint(12, 89),
        "conversion": round(random.uniform(3, 12), 1)
    }
    
    generated = f"【AI生成内容】基于「{creative}」创作的短视频脚本：\n开头钩子：你知道吗？\n核心价值：{creative}\n结尾呼吁：立即试试！（30秒版本）"
    
    estimated = (metrics["views"] * 0.008) + (metrics["likes"] * 0.15) + (metrics["shares"] * 0.3)
    
    return {
        "assessment": {"score": score},
        "metrics": metrics,
        "generated": generated,
        "value": {"estimated": round(estimated, 2), "scale": round(estimated * 100, 2)}
    }

@app.route('/')
def index():
    stats = {"total": len(results), "rate": 100 if results else 0, "avg": round(sum(r["value"]["estimated"] for r in results) / max(1, len(results)), 2)}
    return render_template_string(HTML, creatives=test_creatives, stats=stats, last=results[-1] if results else None)

@app.route('/api/execute', methods=['POST'])
def execute():
    from flask import request
    data = request.json
    result = execute_creative(data.get("creative", ""))
    if result:
        results.append(result)
    return {"success": True}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
