import streamlit as st
import pandas as pd
from datetime import datetime

# 永久存储数据
if "df_data" not in st.session_state:
    st.session_state.df_data = pd.DataFrame(columns=[
        "year","month","income_cum","contract_cum","renew_rate","quanyu_cum","dikong_cum","shilian_complete","market_share","huikuan_rate","shouzhicha_rate",
        "income_score","contract_score","renew_score","new_business_score","market_score","shilian_score","delivery_deduct","business_total",
        "huikuan_score","zhangqi_total","shouzhicha_deduct","quality_total","plus_total","deduct_total","key_total","final_score"
    ])

# 月度进度、鹤壁目标不变
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

# 页面配置
st.set_page_config(page_title="鹤壁智联月度考核填报系统",layout="wide")
st.title("📊鹤壁2026智联业务月度考核填报系统")
st.subheader("✅指标测算｜📊指标详解｜全月份对比分析")

# 填报页面原样保留
with st.form("month_form"):
    col1,col2=st.columns(2)
    with col1:
        year=st.number_input("年份",min_value=2026,max_value=2030,value=2026)
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
    submit=st.form_submit_button("✅计算得分并保存提交")

# 计分公式完全原样保留
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
                         columns=st.session_state.df_data.columns)
    st.session_state.df_data = pd.concat([st.session_state.df_data, new_row], ignore_index=True)
    st.success(f"提交成功！{year}年{month}月最终得分：{final}分")

# 历史数据+分项得分展示
st.divider()
st.subheader("📋全量填报记录（含各指标得分）")
df = st.session_state.df_data
if len(df)>0:
    show_all=df[["year","month","income_score","contract_score","renew_score","new_business_score","market_score","shilian_score","business_total","huikuan_score","zhangqi_total","quality_total","final_score"]].copy()
    show_all.columns=["年份","月份","收入得分","新签得分","续签得分","新业务得分","份额得分","视联得分","业务总分","回款得分","账期得分","效益总分","最终总分"]
    st.dataframe(show_all, hide_index=True, width="stretch")
    csv=show_all.to_csv(index=False,encoding="utf-8-sig")
    st.download_button("📥导出全部得分明细",csv,"鹤壁得分明细.csv")
else:
    st.info("暂无填报数据")

# 全周期对比：显示上月分值+增减，只得分优化劣化
st.divider()
st.subheader("📊全周期得分对比（当月分值+环比增减）")
if len(df)>=2:
    df_sort = df.sort_values(["year","month"],ascending=[True,True])
    curr = df_sort.iloc[-1]
    curr_date = f"{int(curr['year'])}年{int(curr['month'])}月"
    score_list = [
        ("收入得分","income_score"),
        ("新签合同得分","contract_score"),
        ("续签得分","renew_score"),
        ("新业务得分","new_business_score"),
        ("市场份额得分","market_score"),
        ("视联得分","shilian_score"),
        ("业务合计得分","business_total"),
        ("回款得分","huikuan_score"),
        ("账期合计得分","zhangqi_total"),
        ("效益合计得分","quality_total"),
        ("最终总分","final_score")
    ]
    # 逐个往期对比
    for _,old_row in df_sort.iloc[:-1].iterrows():
        old_date = f"{int(old_row['year'])}年{int(old_row['month'])}月"
        st.markdown(f"### {curr_date} VS {old_date}")
        opt_list = []
        bad_list = []
        detail_table=[]
        for name,col in score_list:
            cv=round(curr[col],2)
            ov=round(old_row[col],2)
            diff=round(cv-ov,2)
            detail_table.append([name,ov,cv,diff])
            if diff>0:
                opt_list.append(f"{name} +{diff}")
            elif diff<0:
                bad_list.append(f"{name} {diff}")
        # 明细表格
        df_detail=pd.DataFrame(detail_table,columns=["指标","往期得分","本期得分","增减分值"])
        st.dataframe(df_detail,hide_index=True,width="stretch")
        c1,c2=st.columns(2)
        with c1:
            st.success(f"✅优化 {len(opt_list)}项")
            for i in opt_list:st.markdown(i)
        with c2:
            st.error(f"❌劣化 {len(bad_list)}项")
            for i in bad_list:st.markdown(i)
        st.divider()
else:
    st.info("需至少录入2个月数据，自动对比各指标得分变化")