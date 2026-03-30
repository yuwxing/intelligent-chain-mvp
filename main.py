import json
import datetime
import random
import sys
from typing import Dict, Any

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class IntelligentChainMVP:
    def __init__(self):
        self.processed_count = 0
        self.results = {}
        print("🔗 智能链经济MVP 已启动（内容链模式）\n")

    def submit_creative(self, creative: str, user_id: str = "demo") -> Dict:
        """人类节点：注入创意 → 智能链自主运行"""
        self.processed_count += 1
        print(f"🌱 Day {self.processed_count} | 收到创意：{creative[:50]}...")

        # 1. 评估代理
        assessment = self._assessment_agent(creative)
        if not assessment["pass"]:
            print(f"❌ 评估驳回：{assessment['reason']}")
            return {"status": "rejected", **assessment}

        # 2. 路由代理（当前固定内容链，后续可扩展）
        route = self._routing_agent(creative)
        print(f"➡️ 路由到：{route}")

        # 3. 执行代理集群（内容链）
        execution = self._execution_agent(route, creative)

        # 4. 价值计算代理
        value = self._value_agent(execution)

        # 5. 反馈层
        result = {
            "creative": creative,
            "assessment": assessment,
            "execution_log": execution["log"],
            "generated_content": execution.get("generated", ""),
            "data_metrics": execution["metrics"],
            "value_estimate": value,
            "timestamp": datetime.datetime.now().isoformat(),
            "chain_version": "MVP-v1"
        }

        self.results[self.processed_count] = result
        print(f"✅ 执行完成！价值预估：{value['estimated_value']:.2f} 元\n")
        return result

    def _assessment_agent(self, creative: str) -> Dict:
        """评估代理：这个创意值得跑吗？（Mock，后续换LLM）"""
        # 真实场景可替换为LLM调用 + 结构化输出
        score = random.randint(60, 95)
        if len(creative) < 15 or "测试" in creative:
            return {"pass": False, "score": score, "reason": "创意太模糊或测试专用"}
        return {"pass": True, "score": score, "reason": "高潜力创意，已进入执行链"}

    def _routing_agent(self, creative: str) -> str:
        """路由代理：分配执行链"""
        # 未来可根据关键词智能路由
        return "content_chain"

    def _execution_agent(self, route: str, creative: str) -> Dict:
        """内容链执行：生成→模拟发布→收集数据"""
        if route == "content_chain":
            # Mock生成内容（后续换真实生成）
            generated = f"【AI生成内容】基于「{creative}」创作的短视频脚本：\n" \
                        f"开头钩子：你知道吗？\n" \
                        f"核心价值：{creative}\n" \
                        f"结尾呼吁：立即试试！（30秒版本）"
            
            # Mock发布数据（真实可接Twitter/X API、抖音模拟等）
            metrics = {
                "views": random.randint(800, 3500),
                "likes": random.randint(45, 320),
                "comments": random.randint(8, 65),
                "shares": random.randint(12, 89),
                "conversion_rate": round(random.uniform(0.03, 0.12), 3)
            }
            
            log = f"内容链执行完成：生成脚本 + 模拟发布到测试渠道（X/小红书）"
            return {"log": log, "generated": generated, "metrics": metrics}

    def _value_agent(self, execution: Dict) -> Dict:
        """价值计算代理"""
        m = execution["metrics"]
        estimated = (m["views"] * 0.008) + (m["likes"] * 0.15) + (m["shares"] * 0.3)
        return {
            "estimated_value": round(estimated, 2),
            "scale_potential": round(estimated * 100, 2),  # 规模化后100倍潜力
            "unit": "元"
        }

    def generate_report(self) -> str:
        """7天报告模板，直接给投资人"""
        report = {
            "total_creatives": self.processed_count,
            "success_rate": round(len([r for r in self.results.values() if r.get("assessment", {}).get("pass")]) / max(1, self.processed_count) * 100, 1),
            "average_value": round(sum(r["value_estimate"]["estimated_value"] for r in self.results.values()) / max(1, self.processed_count), 2),
            "results": self.results
        }
        print("📊 7天MVP数据报告生成完成！")
        return json.dumps(report, ensure_ascii=False, indent=2)


# ====================== 立即运行 ======================
if __name__ == "__main__":
    chain = IntelligentChainMVP()
    
    # 测试你的5个创意（直接运行即可）
    test_creatives = [
        "AI微习惯教练：每天推送30秒个性化微习惯视频，根据用户日程和情绪自动调整。",
        "老人AI故事机：输入孙子名字+兴趣，AI生成睡前互动故事+语音。",
        "城市隐藏美食地图：AI根据用户口味+实时天气，生成只属于你的3条美食路线。",
        "职场AI谈判助手：输入谈判场景，AI实时生成话术+语气建议。",
        "可持续穿搭AI：用户拍衣橱照片，AI生成30天零浪费穿搭计划。"
    ]
    
    for i, creative in enumerate(test_creatives, 1):
        print(f"\n=== 测试创意 {i}/5 ===")
        result = chain.submit_creative(creative)
    
    # 生成投资人报告
    report = chain.generate_report()
    print("\n" + "="*60)
    print(report)
