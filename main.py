import streamlit as st
from calculater import SettlementCalculator, SettlementItem
from excel_export import create_excel

st.set_page_config(page_title = "모임 정산기")
st.title("💰 모임 정산기")

people_text = st.text_area("참가자", placeholder = "철수\n영희\n민수")
people = [p.strip() for p in people_text.split("\n") if p.strip()]

food_price = st.number_input("음식 총액", min_value = 0, step = 100)
unit = st.selectbox("잔액 처리 단위", [10, 100, 1000], index = 0)

drink_count = st.number_input("음료 종류 수", min_value = 0, step = 1)
drinks = []
for i in range(drink_count):
    with st.expander(f"음료 {i+1}"):
        name = st.text_input("음료 이름", key=f"name_{i}")
        price = st.number_input("금액", min_value = 0, step = 100, key=f"price_{i}")
        memo = st.text_area("메모", key=f"memo_{i}")
        mode = st.radio("계산 방식", ["인원 기준", "개수 기준"], key=f"mode_{i}")

        shares = []
        if mode == "인원 기준":
            shares = st.multiselect("마신 사람", people, key=f"drinkers_{i}")
        else:
            for person in people:
                count = st.number_input(f"{person} 개수", min_value = 0, step = 1,
                key=f"{i}_{person}")
                shares.extend([person] * count)

        drinks.append(SettlementItem(name=name, price=price, shares = shares,
        memo = memo))

if st.button("정산하기"):
    calc = SettlementCalculator(people, unit)
    calc.add_item(SettlementItem(name="음식", price=food_price, shares=people))

    for drink in drinks:
        calc.add_item(drink)
    
    result, details = clac.calculate()

    st.subheader("정산 결과")
    summary_text = ("[모임 정산]\n\n")

    for person, amount in sorted(result.items(), key=lambda x: x[1], reverse=True):
        st.write(f"### {person} : {amount:,}원")
        for detail in details[person]:
            st.write(f"- {detail}")
        summary_text += (f"{person} : "
        f"{amount,:}원\n")
    
    st.subheader("카카오톡 공유용")
    st.code(summary_text, language=None)

    excel_data = create_excel(result, details, calc.itmes, food_price, unit)
    st.download_button("📊 엑셀 다운로드",
        data=excel_data,
        file_name="모임정산.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")