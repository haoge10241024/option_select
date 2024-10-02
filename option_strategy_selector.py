# 文件名：option_strategy_selector.py

import streamlit as st

# 定义策略类
class OptionStrategy:
    def __init__(self, name, description, applicable_market, applicable_volatility,
                 holding_requirement, advantages, disadvantages, example, guidelines):
        self.name = name
        self.description = description
        self.applicable_market = applicable_market  # 市场预期列表
        self.applicable_volatility = applicable_volatility  # 波动率预期列表
        self.holding_requirement = holding_requirement  # '持有多头'、'持有空头'、'无持仓' 或 '任意'
        self.advantages = advantages
        self.disadvantages = disadvantages
        self.example = example
        self.guidelines = guidelines

# 定义策略库
strategy_library = [
    # 买入看涨期权（Long Call）
    OptionStrategy(
        name="买入看涨期权（Long Call）",
        description="买入一份看涨期权，预期标的资产价格上涨。",
        applicable_market=["大涨", "小涨"],
        applicable_volatility=["增加", "稳定"],
        holding_requirement="无持仓",
        advantages=["潜在收益无限", "风险有限于期权费"],
        disadvantages=["需要标的价格大幅上涨才能盈利", "期权费成本可能较高"],
        example="以5元的期权费购买执行价为100元的看涨期权，若到期时标的资产价格为110元，盈利为5元（不含期权费）。",
        guidelines={
            "执行价选择": "选择接近当前标的价格的执行价，以平衡成本和盈利概率。",
            "合约数量": "根据资金规模决定购买数量。",
            "到期日选择": "选择适合预期价格上涨时间框架的到期日。",
            "其他注意事项": "注意时间价值损耗，尽量避免临近到期日才购买。"
        }
    ),

    # 买入看跌期权（Long Put）
    OptionStrategy(
        name="买入看跌期权（Long Put）",
        description="买入一份看跌期权，预期标的资产价格下跌。",
        applicable_market=["大跌", "小跌"],
        applicable_volatility=["增加", "稳定"],
        holding_requirement="无持仓",
        advantages=["在价格下跌时获利", "风险有限于期权费"],
        disadvantages=["需要标的价格大幅下跌才能盈利", "期权费成本可能较高"],
        example="以5元的期权费购买执行价为100元的看跌期权，若到期时标的资产价格为90元，盈利为5元（不含期权费）。",
        guidelines={
            "执行价选择": "选择接近当前标的价格的执行价。",
            "合约数量": "根据资金规模决定购买数量。",
            "到期日选择": "选择适合预期价格下跌时间框架的到期日。",
            "其他注意事项": "适用于预期价格下跌或作为持仓的对冲手段。"
        }
    ),

    # 备兑看涨期权（Covered Call）
    OptionStrategy(
        name="备兑看涨期权（Covered Call）",
        description="持有标的资产的多头仓位，同时卖出相应数量的看涨期权。",
        applicable_market=["小涨", "盘整"],
        applicable_volatility=["稳定", "减少"],
        holding_requirement="持有多头",
        advantages=["获得期权费收入", "降低持仓成本"],
        disadvantages=["在标的价格大幅上涨时，收益被限制"],
        example="持有100股股票，同时卖出一份执行价为105元的看涨期权，获得期权费3元。",
        guidelines={
            "执行价选择": "选择高于当前价格的执行价，以获得期权费并保留一定上涨空间。",
            "合约数量": "卖出期权的合约数量应与持有的标的数量匹配。",
            "到期日选择": "根据收益目标和市场预期选择短期或长期期权。",
            "其他注意事项": "适用于看好标的资产但预期涨幅有限的情况。"
        }
    ),

    # 保护性看跌期权（Protective Put）
    OptionStrategy(
        name="保护性看跌期权（Protective Put）",
        description="持有标的资产的多头仓位，同时买入相应数量的看跌期权。",
        applicable_market=["小跌", "大跌"],
        applicable_volatility=["增加"],
        holding_requirement="持有多头",
        advantages=["限制下行风险", "保留价格上涨的潜力"],
        disadvantages=["需要支付期权费", "成本增加"],
        example="持有100股股票，同时以5元的期权费买入一份执行价为95元的看跌期权。",
        guidelines={
            "执行价选择": "选择略低于当前价格的执行价，以平衡成本和保护力度。",
            "合约数量": "买入期权的合约数量应与持有的标的数量匹配。",
            "到期日选择": "选择适合风险保护期限的到期日。",
            "其他注意事项": "适用于担心短期价格下跌，但长期看好标的资产。"
        }
    ),

    # 牛市看涨价差（Bull Call Spread）
    OptionStrategy(
        name="牛市看涨价差（Bull Call Spread）",
        description="买入低执行价看涨期权，同时卖出高执行价看涨期权。",
        applicable_market=["小涨"],
        applicable_volatility=["稳定", "减少"],
        holding_requirement="无持仓",
        advantages=["成本低于单独买入看涨期权", "风险有限"],
        disadvantages=["收益被限制", "需要支付净期权费"],
        example="以5元的期权费买入执行价为100元的看涨期权，同时以2元的期权费卖出执行价为110元的看涨期权，净成本3元。",
        guidelines={
            "执行价选择": "买入执行价较低的期权，卖出执行价较高的期权。",
            "合约数量": "买入和卖出期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "适用于预期价格小幅上涨的情况。"
        }
    ),

    # 熊市看跌价差（Bear Put Spread）
    OptionStrategy(
        name="熊市看跌价差（Bear Put Spread）",
        description="买入高执行价看跌期权，同时卖出低执行价看跌期权。",
        applicable_market=["小跌"],
        applicable_volatility=["稳定", "减少"],
        holding_requirement="无持仓",
        advantages=["成本低于单独买入看跌期权", "风险有限"],
        disadvantages=["收益被限制", "需要支付净期权费"],
        example="以5元的期权费买入执行价为110元的看跌期权，同时以2元的期权费卖出执行价为100元的看跌期权，净成本3元。",
        guidelines={
            "执行价选择": "买入执行价较高的期权，卖出执行价较低的期权。",
            "合约数量": "买入和卖出期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "适用于预期价格小幅下跌的情况。"
        }
    ),

    # 领口策略（Collar Strategy）
    OptionStrategy(
        name="领口策略（Collar Strategy）",
        description="持有标的资产的多头仓位，同时买入看跌期权，卖出看涨期权。",
        applicable_market=["小涨", "小跌", "盘整"],
        applicable_volatility=["稳定", "减少"],
        holding_requirement="持有多头",
        advantages=["降低下行风险", "期权费成本低或为零"],
        disadvantages=["限制了上涨收益", "策略复杂度增加"],
        example="持有100股股票，同时以3元的期权费买入执行价为95元的看跌期权，卖出执行价为105元的看涨期权，获得期权费3元，净成本为零。",
        guidelines={
            "执行价选择": "买入略低于当前价格的看跌期权，卖出略高于当前价格的看涨期权。",
            "合约数量": "买入和卖出期权的合约数量应与持有的标的数量匹配。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "适用于希望保护已有收益并限制下行风险的情况。"
        }
    ),

    # 买入跨式策略（Long Straddle）
    OptionStrategy(
        name="买入跨式策略（Long Straddle）",
        description="同时买入相同执行价的看涨期权和看跌期权。",
        applicable_market=["不确定"],
        applicable_volatility=["增加"],
        holding_requirement="无持仓",
        advantages=["在价格大幅波动时获利", "风险有限于期权费"],
        disadvantages=["成本高", "时间价值损耗"],
        example="购买执行价为100元的看涨期权和看跌期权，各支付期权费5元，总成本10元。价格大幅上涨或下跌时，可获利。",
        guidelines={
            "执行价选择": "选择接近当前价格的执行价。",
            "合约数量": "买入看涨和看跌期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "需要标的资产有较大波动才能获利。"
        }
    ),

    # 买入勒式策略（Long Strangle）
    OptionStrategy(
        name="买入勒式策略（Long Strangle）",
        description="同时买入不同执行价的看涨期权和看跌期权。",
        applicable_market=["不确定"],
        applicable_volatility=["增加"],
        holding_requirement="无持仓",
        advantages=["成本较低（相比跨式策略）", "在价格大幅波动时获利"],
        disadvantages=["需要更大价格波动才能获利", "时间价值损耗"],
        example="购买执行价为110元的看涨期权和90元的看跌期权，各支付期权费3元，总成本6元。价格大幅上涨或下跌时，可获利。",
        guidelines={
            "执行价选择": "看涨期权执行价高于当前价格，看跌期权执行价低于当前价格。",
            "合约数量": "买入看涨和看跌期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "适用于预期大幅波动但方向不明的情形。"
        }
    ),

    # 蝶式价差（Butterfly Spread）
    OptionStrategy(
        name="蝶式价差（Butterfly Spread）",
        description="同时买入和卖出多份看涨或看跌期权，以构建有限风险和有限收益的策略。",
        applicable_market=["盘整"],
        applicable_volatility=["减少"],
        holding_requirement="无持仓",
        advantages=["成本低", "风险有限"],
        disadvantages=["收益有限", "策略复杂"],
        example="买入一份执行价为95元的看涨期权，卖出两份执行价为100元的看涨期权，买入一份执行价为105元的看涨期权。",
        guidelines={
            "执行价选择": "三种执行价，中心执行价对应当前价格。",
            "合约数量": "买入和卖出期权的比例通常为1:2:1。",
            "到期日选择": "所有期权的到期日应相同。",
            "其他注意事项": "适用于预期价格波动较小的情形。"
        }
    ),

    # 铁鹰式价差（Iron Condor）
    OptionStrategy(
        name="铁鹰式价差（Iron Condor）",
        description="结合看涨和看跌价差策略，构建在价格保持稳定时获利的策略。",
        applicable_market=["盘整"],
        applicable_volatility=["减少"],
        holding_requirement="无持仓",
        advantages=["风险有限", "收益稳定"],
        disadvantages=["收益有限", "策略复杂"],
        example="卖出一份执行价为95元的看跌期权，买入一份执行价为90元的看跌期权；同时，卖出一份执行价为105元的看涨期权，买入一份执行价为110元的看涨期权。",
        guidelines={
            "执行价选择": "卖出执行价接近当前价格的期权，买入更远执行价的期权。",
            "合约数量": "买入和卖出期权的合约数量应相同。",
            "到期日选择": "所有期权的到期日应相同。",
            "其他注意事项": "适用于预期价格在一定范围内波动的情形。"
        }
    ),

    # 日历价差（Calendar Spread）
    OptionStrategy(
        name="日历价差（Calendar Spread）",
        description="买入长期期权，卖出短期期权，执行价相同。",
        applicable_market=["盘整"],
        applicable_volatility=["增加", "稳定"],
        holding_requirement="无持仓",
        advantages=["利用时间价值差异获利", "风险有限"],
        disadvantages=["对波动率变化敏感", "策略复杂"],
        example="买入6个月后到期的执行价为100元的看涨期权，卖出1个月后到期的执行价为100元的看涨期权。",
        guidelines={
            "执行价选择": "买入和卖出期权的执行价相同。",
            "合约数量": "买入和卖出期权的合约数量应相同。",
            "到期日选择": "买入长期期权，卖出短期期权。",
            "其他注意事项": "适用于预期短期内价格稳定，长期有波动的情形。"
        }
    ),

    # 保护性看涨期权（Protective Call）
    OptionStrategy(
        name="保护性看涨期权（Protective Call）",
        description="持有标的资产的空头仓位，同时买入相应数量的看涨期权。",
        applicable_market=["小涨", "大涨"],
        applicable_volatility=["增加"],
        holding_requirement="持有空头",
        advantages=["限制上行风险", "保留价格下跌的潜力"],
        disadvantages=["需要支付期权费", "成本增加"],
        example="持有100股股票的空头仓位，同时以5元的期权费买入一份执行价为105元的看涨期权。",
        guidelines={
            "执行价选择": "选择略高于当前价格的执行价，以平衡成本和保护力度。",
            "合约数量": "买入期权的合约数量应与持有的空头标的数量匹配。",
            "到期日选择": "选择适合风险保护期限的到期日。",
            "其他注意事项": "适用于担心价格上涨，对空头仓位进行保护。"
        }
    ),

    # 备兑看跌期权（Covered Put）
    OptionStrategy(
        name="备兑看跌期权（Covered Put）",
        description="持有标的资产的空头仓位，同时卖出相应数量的看跌期权。",
        applicable_market=["小跌", "盘整"],
        applicable_volatility=["稳定", "减少"],
        holding_requirement="持有空头",
        advantages=["获得期权费收入", "降低持仓成本"],
        disadvantages=["在标的价格大幅下跌时，收益被限制"],
        example="持有100股股票的空头仓位，同时卖出一份执行价为95元的看跌期权，获得期权费3元。",
        guidelines={
            "执行价选择": "选择低于当前价格的执行价，以获得期权费并保留一定下跌空间。",
            "合约数量": "卖出期权的合约数量应与持有的空头标的数量匹配。",
            "到期日选择": "根据收益目标和市场预期选择短期或长期期权。",
            "其他注意事项": "适用于看空标的资产但预期跌幅有限的情况。"
        }
    ),

    # 卖出跨式策略（Short Straddle）
    OptionStrategy(
        name="卖出跨式策略（Short Straddle）",
        description="同时卖出相同执行价的看涨期权和看跌期权。",
        applicable_market=["盘整"],
        applicable_volatility=["减少"],
        holding_requirement="无持仓",
        advantages=["获得期权费收入", "在价格稳定时获利"],
        disadvantages=["潜在损失无限", "风险高"],
        example="卖出执行价为100元的看涨期权和看跌期权，各获得期权费5元，总收入10元。价格保持在100元附近时，可获利。",
        guidelines={
            "执行价选择": "选择接近当前价格的执行价。",
            "合约数量": "卖出看涨和看跌期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "需注意潜在的无限风险，适用于有经验的投资者。"
        }
    ),

    # 卖出勒式策略（Short Strangle）
    OptionStrategy(
        name="卖出勒式策略（Short Strangle）",
        description="同时卖出不同执行价的看涨期权和看跌期权。",
        applicable_market=["盘整"],
        applicable_volatility=["减少"],
        holding_requirement="无持仓",
        advantages=["获得期权费收入", "在价格稳定时获利", "风险低于卖出跨式策略"],
        disadvantages=["潜在损失仍然很大", "风险高"],
        example="卖出执行价为110元的看涨期权和90元的看跌期权，各获得期权费3元，总收入6元。价格在90元至110元之间时，可获利。",
        guidelines={
            "执行价选择": "看涨期权执行价高于当前价格，看跌期权执行价低于当前价格。",
            "合约数量": "卖出看涨和看跌期权的合约数量应相同。",
            "到期日选择": "选择相同的到期日。",
            "其他注意事项": "风险高于单纯卖出期权，需注意风险管理。"
        }
    ),
]

# 策略推荐函数
def recommend_strategies(market_view, volatility_view, holding_position):
    recommended = []
    for strategy in strategy_library:
        # 检查必要条件（例如持仓要求）
        if strategy.holding_requirement != "任意" and strategy.holding_requirement != holding_position:
            continue  # 不满足必要条件，跳过该策略

        score = 0
        total_weight = 0

        # 条件权重
        weights = {
            'market_view': 3,
            'volatility_view': 2
        }

        # 检查市场预期
        total_weight += weights['market_view']
        if market_view in strategy.applicable_market:
            score += weights['market_view']

        # 检查波动率预期
        total_weight += weights['volatility_view']
        if volatility_view in strategy.applicable_volatility:
            score += weights['volatility_view']

        # 计算匹配度
        match_ratio = score / total_weight

        # 如果匹配度大于等于0.6，则推荐该策略
        if match_ratio >= 0.6:
            recommended.append((strategy, match_ratio))

    # 按照匹配度从高到低排序
    recommended.sort(key=lambda x: x[1], reverse=True)

    return [item[0] for item in recommended]

# 主程序
def main():
    st.title("期权策略选择助手")
    st.write("根据您的市场预期和持仓情况，我们将推荐适合的期权策略，并提供详细的策略信息和操作指导。")

    st.header("输入您的市场预期和持仓情况：")

    # 用户输入
    holding_position = st.selectbox("您的标的资产持仓情况：", ("无持仓", "持有多头", "持有空头"))
    market_view = st.selectbox("您的市场预期是？", ("大涨", "小涨", "盘整", "小跌", "大跌", "不确定"))
    volatility_view = st.selectbox("您对波动率的预期是？", ("增加", "减少", "稳定"))

    # 推荐策略
    strategies = recommend_strategies(market_view, volatility_view, holding_position)

    st.header("推荐的期权策略：")
    if strategies:
        for strategy in strategies:
            st.subheader(strategy.name)
            st.write(f"**策略描述**：{strategy.description}")
            st.write(f"**适用市场预期**：{'、'.join(strategy.applicable_market)}")
            st.write(f"**适用波动率预期**：{'、'.join(strategy.applicable_volatility)}")
            st.write(f"**持仓要求**：{strategy.holding_requirement}")
            st.write(f"**优点**：{'；'.join(strategy.advantages)}")
            st.write(f"**缺点**：{'；'.join(strategy.disadvantages)}")
            st.write(f"**案例分析**：{strategy.example}")
            st.write("**策略操作要点**：")
            st.write(f"- **执行价选择**：{strategy.guidelines['执行价选择']}")
            st.write(f"- **合约数量**：{strategy.guidelines['合约数量']}")
            st.write(f"- **到期日选择**：{strategy.guidelines['到期日选择']}")
            st.write(f"- **其他注意事项**：{strategy.guidelines['其他注意事项']}")
            st.write("---")
    else:
        st.write("根据您的输入，未找到合适的策略，请调整您的选项。")

if __name__ == "__main__":
    main()
