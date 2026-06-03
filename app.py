import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ===================== 核心：云端永久存储 =====================
# 存在Streamlit云端磁盘，永远不丢
DATA_FOLDER = "/mount/src/data"
os.makedirs(DATA_FOLDER, exist_ok=True)
DATA_FILE = os.path.join(DATA_FOLDER, "kpi_data.csv")

def init_data():
    cols = [
        "year","month","income_cum","contract_cum","renew_rate","quanyu_cum","dikong_cum","shilian_complete","market_share","huikuan_rate","shouzhicha_rate",
        "income_score","contract_score","renew_score","new_business_score","market_score","shilian_score","delivery_deduct","business_total",
        "huikuan_score","zhangqi_total","shouzhicha_deduct","quality_total","plus_total","deduct_total","key_total","final_score"
    ]
    df = pd.DataFrame(columns=cols)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    return df

def load_data():
    if not os.path.exists(DATA_FILE):
        return init_data()
    try:
        return pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    except:
        return init_data()

def save_data(df_new):
    df_old = load_data()
    df_all = pd.concat([df_old, df_new], ignore_index=True)
    df_all.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# ===================== 业务配置不变 =====================
monthly_progress = {
    1: {"收入": 0.0725, "回款": 0.06},2: {"收入": 0.145, "回款": 0.09},3: {"收入": 0.225, "回款": 0.14},
    4: {"收入": 0.305, "回款": 0.18},5: {"收入": 0.385, "回款": 0.22},6: {"收入": 0.465, "回款": 0.26},
    7: {"收入": 0.545, "回款": 0.29},8: {"收入": 0.625, "回款": 0.32},9: {"收入": 0.705, "回款": 0.36},
    10: {"收入": 0.785, "回款": 0.38},11: {"收入": 0.865, "回款": 0.41},12: {"收入": 1.0, "回款": 0.44}
}
annual_target = {
    "income_total": 750,"contract_base":1500,"contract_challenge":1875,"renew_target":0.65,
    "new_business_quanyu":152,"new_business_dikong":152,"shilian_target":73,"market_share_target":0.4,"huikuan_target":0.44,"shouzhicha_target":0.35
}

# ===================== 页面 =====================
st.set_page_config(page_title="鹤壁智联考核系统", layout="wide")
st.title("📊鹤壁智联业务月度考核系统")
st.subheader("✅得分测算｜指标对比｜优劣分析")

# 每次打开自动加载历史
df_all = load_data()

# 表单
with st.form("form"):
    col1,col2=st.columns(2)
    with col1:
        year=st.number_input("年份",min_value=2026,value=2026)
        month=st.number_input("月份",min_value=1,max_value=12,value=datetime.now().month)
    st.markdown("### 一、业务发展数据")
    col_a,col_b=st.columns(2)
    with col_a:
        income_cum=st.number_input("累计收入(万元)",value=0.0,step=0.1)
        contract_cum=st.number_input("累计新签合同(万元)",value=0.0,step=0.1)
        renew_rate=st.number_input("存量续签率",value=0.0,step=0.01)
        quanyu_cum=st.number_input("全域感知签约(万元)",value=0.0,step=0.1)
        dikong_cum=st.number_input("低空+智算签约(万元)",value=0.0,step=0.1)
    with col_b:
        shilian_complete=st.number_input("视联净增路数",value=0,step=1)
        market_share=st.number_input("重点场景市场份额",value=0.0,step=0.01)
        shifen_plus=st.number_input("室分+X加分",value=0.0,max_value=2.0)
        overdue_project=st.number_input("超期未交付项目",value=0)
        delivery_deduct=st.number_input("免扣分项目",value=0)
    st.markdown("### 二、质量效益数据")
    col_c,col_d=st.columns(2)
    with col_c:
        huikuan_rate=st.number_input("累计回款率",value=0.0,step=0.01)
        zhangqi_2025=st.number_input("2025账期回款率",value=0.0,step=0.01)
        zhangqi_2024=st.number_input("2024账期回款率",value=0.0,step=0.01)
        zhangqi_2023=st.number_input("2023账期回款率",value=0.0,step=0.01)
    with col_d:
        zhangqi_2022=st.number_input("2022账期回款率",value=0.0,step=0.01)
        zhangqi_2021=st.number_input("2021及以前回款率",value=0.0,step=0.01)
        shouzhicha_rate=st.number_input("收支差占收比",value=0.0,step=0.01)
        yingshou_deduct=st.number_input("应收占收比扣分",value=0.0)
    st.markdown("### 三、加减分项")
    col_e,col_f=st.columns(2)
    with col_e:
        hezuo_plus=st.number_input("战略合作加分",value=0.0,step=0.5)
        saishi_plus=st.number_input("赛事加分",value=0.0,max_value=5.0)
        zhuanxiang_plus=st.number_input("专项加分",value=0.0)
        anquan_plus=st.number_input("安质加分",value=0.0,max_value=10.0)
        xietong_plus=st.number_input("协同加分",value=0.0,max_value=2.0)
    with col_f:
        anquan_deduct=st.number_input("安全事故扣分",value=0.0)
        xietong_deduct=st.number_input("协同扣分",value=0.0,max_value=2.0)
        neikong_deduct=st.number_input("内控违规扣分",value=0.0)
    submit=st.form_submit_button("✅计算并保存到云端")

# 计分逻辑
if submit:
    m_target_inc=annual_target["income_total"]*monthly_progress[month]["收入"]
    inc_rate=income_cum/m_target_inc if m_target_inc>0 else 0
    inc_score=30+5*min((inc_rate-1)/0.05,1) if inc_rate>=1 else 30*inc_rate

    con_rate=contract_cum/annual_target["contract_base"]
    con_score=15+5*min((contract_cum-annual_target["contract_base"])/(annual_target["contract_challenge"]-annual_target["contract_base"]),1) if con_rate>=1 else 15*con_rate

    renew_score=5 if renew_rate>=0.6 else 5*(renew_rate/0.6)

    quan_rate=quanyu_cum/annual_target["new_business_quanyu"]
    quan_s=5+min((quan_rate-1)*5,2) if quan_rate>=1 else 5*quan_rate
    dik_rate=dikong_cum/annual_target["new_business_dikong"]
    dik_s=5+min((dik_rate-1)*5,2) if dik_rate>=1 else 5*dik_rate
    new_s=quan_s+dik_s+shifen_plus

    mar_score=5 if market_share>=0.4 else 5*(market_share/0.4)
    shi_rate=shilian_complete/annual_target["shilian_target"]
    shi_score=5 if shi_rate>=1 else 5*shi_rate
    deliv=min((overdue_project-delivery_deduct)*0.2,2)
    bus_total=round(inc_score+con_score+renew_score+new_s+mar_score+shi_score-deliv,2)

    hk_tar=monthly_progress[month]["回款"]
    hk_score=20+min((huikuan_rate-hk_tar)*100,10) if huikuan_rate>=hk_tar else 20*(huikuan_rate/hk_tar)
    hk_score=max(hk_score-yingshou_deduct,0)

    z25=2+min((zhangqi_2025-0.52)*100*0.1,1) if zhangqi_2025>=0.52 else 2*(zhangqi_2025/0.52)
    z24=2+min((zhangqi_2024-0.4)*100*0.1,1) if zhangqi_2024>=0.4 else 2*(zhangqi_2024/0.4)
    z23=2+min((zhangqi_2023-0.33)*5,1) if zhangqi_2023>=0.33 else 2*(zhangqi_2023/0.33)
    z22=2+min((zhangqi_2022-0.3)*5,1) if zhangqi_2022>=0.3 else 2*(zhangqi_2022/0.3)
    z21=2+min((zhangqi_2021-1)*5,1) if zhangqi_2021>=1 else 2*zhangqi_2021
    z_total=round(z25+z24+z23+z22+z21,2)

    sc_del=min(max((0.35-shouzhicha_rate)*100*0.2,0),3)
    qual_total=round(hk_score+z_total-sc_del,2)
    add=hezuo_plus+saishi_plus+zhuanxiang_plus+anquan_plus+xietong_plus
    sub=anquan_deduct+xietong_deduct+neikong_deduct
    item_total=round(add-sub,2)
    final=round(bus_total+qual_total+item_total,2)

    new_row=pd.DataFrame([[year,month,income_cum,contract_cum,renew_rate,quanyu_cum,dikong_cum,shilian_complete,market_share,huikuan_rate,shouzhicha_rate,
                           inc_score,con_score,renew_score,new_s,mar_score,shi_score,deliv,bus_total,hk_score,z_total,sc_del,qual_total,add,sub,item_total,final]],
                         columns=df_all.columns)
    save_data(new_row)
    st.success(f"✅ {year}年{month}月 提交成功！总分：{final} （已保存）")
    df_all = load_data()

# ===================== 展示历史 =====================
st.divider()
st.subheader("📋 历史记录）")
if len(df_all) > 0:
    show = df_all[["year","month","income_score","contract_score","renew_score","new_business_score","market_score","shilian_score","business_total","huikuan_score","zhangqi_total","quality_total","final_score"]].copy()
    show.columns = ["年","月","收入","新签","续签","新业务","市场","视联","业务分","回款","账期","效益分","总分"]
    st.dataframe(show, use_container_width=True, hide_index=True)
else:
    st.info("暂无数据")

# ===================== 对比 =====================
# ===================== 月度得分对比（全月份两两全部对比） =====================
st.divider()
st.subheader("📊 月份指标得分对比")
if len(df_all) >= 2:
    df_sort = df_all.sort_values(["year","month"], ascending=[True,True]).reset_index(drop=True)
    items = [
        ("收入得分","income_score"),("新签合同得分","contract_score"),("续签得分","renew_score"),
        ("新业务得分","new_business_score"),("市场份额得分","market_score"),("视联得分","shilian_score"),
        ("业务合计得分","business_total"),("回款得分","huikuan_score"),("账期合计得分","zhangqi_total"),
        ("效益合计得分","quality_total"),("最终总分","final_score")
    ]
    # 双重循环，全部两两配对
    import itertools
    for idx1,idx2 in itertools.combinations(range(len(df_sort)),2):
        old = df_sort.iloc[idx1]
        curr = df_sort.iloc[idx2]
        old_label = f"{int(old.year)}年{int(old.month)}月"
        curr_label = f"{int(curr.year)}年{int(curr.month)}月"
        st.markdown(f"### {curr_label} VS {old_label}")
        opt = []
        bad = []
        table = []
        for name, col in items:
            c = round(curr[col],2)
            o = round(old[col],2)
            d = round(c-o,2)
            table.append([name, o, c, d])
            if d>0: opt.append(f"{name} +{d}")
            elif d<0: bad.append(f"{name} {d}")

        st.dataframe(pd.DataFrame(table, columns=["指标","往期","本期","增减"]), hide_index=True, use_container_width=True)
        c1,c2 = st.columns(2)
        c1.success(f"✅ 优化 {len(opt)} 项")
        for i in opt: c1.write(i)
        c2.error(f"❌ 劣化 {len(bad)} 项")
        for i in bad: c2.write(i)
        st.divider()
else:
    st.info("需要至少2个月数据才可对比")