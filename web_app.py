import streamlit as st
import json
import datetime
import random
from typing import Dict

class IntelligentChainMVP:
    def __init__(self):
        self.processed_count = 0
        self.results = {}

    def submit_creative(self, creative: str) -> Dict:
        self.processed_count += 1
        
        score = random.randint(60, 95)
        if len(creative) < 15 or "测试" in creative:
            return {"status": "rejected", "pass": False, "score": score, "reason": "创意太模糊或测试专用"}
        
        route = "content_chain"
        
        generated = f"【AI生成内容】基于「{creative}」创作的短视频脚本：\n开头钩子：你知道吗？\n核心价值：{creative}\n结尾呼吁：立即试试！（30秒版本）"
        
        metrics = {
            "views": random.randint(800, 3500),
            "likes": random.randint(45, 320),
            "comments": random.randint(8, 65),
            "shares": random.randint(12, 89),
            "conversion_rate": round(random.uniform(0.03, 0.12), 3)
        }
        
        estimated = (metrics["views"] * 0.008) + (metrics["likes"] * 0.15) + (metrics["shares"] * 0.3)
        value = {
            "estimated_value": round(estimated, 2),
            "scale_potential": round(estimated * 100, 2),
            "unit": "元"
        }
        
        result = {
            "creative": creative,
            "assessment": {"pass": True, "score": score, "reason": "高潜力创意，已进入执行链"},
            "execution_log": "内容链执行完成：生成脚本 + 模拟发布到测试渠道",
            "generated_content": generated,
            "data_metrics": metrics,
            "value_estimate": value,
            "timestamp": datetime.datetime.now().isoformat(),
            "chain_version": "MVP-v1"
        }
        
        self.results[self.processed_count] = result
        return result

    def get_report(self) -> Dict:
        return {
            "total_creatives": self.processed_count,
            "success_rate": round(len([r for r in self.results.values() if r.get("assessment", {}).get("pass")]) / max(1, self.processed_count) * 100, 1),
            "average_value": round(sum(r["value_estimate"]["estimated_value"] for r in self.results.values()) / max(1, self.processed_count), 2),
            "results": self.results
        }

if 'chain' not in st.session_state:
    st.session_state.chain = IntelligentChainMVP()

st.set_page_config(page_title="智能链经济MVP", page_icon="🔗", layout="wide")

st.title("🔗 智能链经济 MVP")
st.markdown("**内容链模式** - 人类注入创意，AI自主运行")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 提交创意")
    
    test_creatives = [
        "AI微习惯教练：每天推送30秒个性化微习惯视频，根据用户日程和情绪自动调整。",
        "老人AI故事机：输入孙子名字+兴趣，AI生成睡前互动故事+语音。",
        "城市隐藏美食地图：AI根据用户口味+实时天气，生成只属于你的3条美食路线。",
        "职场AI谈判助手：输入谈判场景，AI实时生成话术+语气建议。",
        "可持续穿搭AI：用户拍衣橱照片，AI生成30天零浪费穿搭计划。"
    ]
    
    creative_input = st.text_area("输入你的创意", height=100, placeholder="描述你的商业创意...")
    
    selected_creative = st.selectbox("或选择预设创意", [""] + test_creatives)
    if selected_creative:
        creative_input = selected_creative
    
    if st.button("🚀 执行创意", type="primary"):
        if creative_input and len(creative_input) >= 15:
            result = st.session_state.chain.submit_creative(creative_input)
            st.session_state.last_result = result
        else:
            st.error("创意太短了（至少15个字符）")
    
    st.divider()
    
    report = st.session_state.chain.get_report()
    st.subheader("📊 数据概览")
    col_a, col_b = st.columns(2)
    col_a.metric("总创意数", report["total_creatives"])
    col_b.metric("通过率", f"{report['success_rate']}%")
    st.metric("平均价值", f"¥{report['average_value']}")

with col2:
    st.subheader("📋 执行结果")
    
    if 'last_result' in st.session_state:
        r = st.session_state.last_result
        
        if r.get("status") == "rejected":
            st.error(f"❌ 评估驳回: {r['reason']}")
        else:
            st.success(f"✅ 执行完成！价值预估: ¥{r['value_estimate']['estimated_value']}")
            
            with st.expander("📈 数据指标", expanded=True):
                m = r["data_metrics"]
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("浏览", m["views"])
                c2.metric("点赞", m["likes"])
                c3.metric("评论", m["comments"])
                c4.metric("分享", m["shares"])
                c5.metric("转化", f"{m['conversion_rate']*100}%")
            
            with st.expander("🎬 生成内容"):
                st.text(r["generated_content"])
            
            with st.expander("💰 价值评估"):
                st.write(f"预估价值: ¥{r['value_estimate']['estimated_value']}")
                st.write(f"规模化潜力: ¥{r['value_estimate']['scale_potential']}")
            
            with st.expander("🔍 评估详情"):
                st.write(f"评分: {r['assessment']['score']}")
                st.write(f"原因: {r['assessment']['reason']}")
    else:
        st.info("👈 提交创意开始执行")

st.divider()
st.caption("🔗 智能链经济 MVP v1.0 - 投资人演示版本")
