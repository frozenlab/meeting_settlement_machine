import streamlit as st
import random

st.set_page_config(page_title="모임 정산기")

st.title("💰 모임 정산기")

# 참가자
people_text = st.text_area(
    "참가자 이름 (한 줄에 한 명)",
    "철수\n영희\n민수"
)

people = [p.strip() for p in people_text.split("\n") if p.strip()]

if len(people) < 1:
    st.stop()

food_price = st.number_input(
    "음식 총액",
    min_value=0,
    step=1000
)

st.divider()

drink_count = st.number_input(
    "음료 종류 수",
    min_value=0,
    step=1
)

drinks = []

for i in range(drink_count):

    st.subheader(f"음료 {i+1}")

    name = st.text_input(
        "음료 이름",
        key=f"name_{i}"
    )

    price = st.number_input(
        "금액",
        min_value=0,
        step=100,
        key=f"price_{i}"
    )

    mode = st.radio(
        "계산 방식",
        ["개수 기준", "인원 기준"],
        key=f"mode_{i}"
    )

    drink_data = {
        "name": name,
        "price": price,
        "mode": mode
    }

    if mode == "개수 기준":

        counts = {}

        for person in people:
            count = st.number_input(
                f"{person} 마신 개수",
                min_value=0,
                step=1,
                key=f"{i}_{person}"
            )

            if count > 0:
                counts[person] = count

        drink_data["drinkers"] = counts

    else:

        selected = st.multiselect(
            "마신 사람",
            people,
            key=f"drinkers_{i}"
        )

        drink_data["drinkers"] = selected

    drinks.append(drink_data)

st.divider()

if st.button("정산하기"):

    result = {p: 0 for p in people}

    # 음식값 더치페이
    food_share = food_price // len(people)
    remainder = food_price % len(people)

    for p in people:
        result[p] += food_share

    if remainder > 0:
        losers = random.sample(
            people,
            min(remainder, len(people))
        )

        for p in losers:
            result[p] += 1

    # 음료 계산
    for drink in drinks:

        price = drink["price"]

        if drink["mode"] == "개수 기준":

            counts = drink["drinkers"]

            total_count = sum(counts.values())

            if total_count == 0:
                continue

            base = price // total_count
            remainder = price % total_count

            temp = {}

            for person, count in counts.items():
                temp[person] = base * count

            tickets = []

            for person, count in counts.items():
                tickets.extend([person] * count)

            if remainder > 0:
                extra = random.sample(
                    tickets,
                    remainder
                )

                for p in extra:
                    temp[p] += 1

            for p, amount in temp.items():
                result[p] += amount

        else:

            drinkers = drink["drinkers"]

            if len(drinkers) == 0:
                continue

            base = price // len(drinkers)
            remainder = price % len(drinkers)

            for p in drinkers:
                result[p] += base

            if remainder > 0:

                extra = random.sample(
                    drinkers,
                    min(remainder, len(drinkers))
                )

                for p in extra:
                    result[p] += 1

    st.success("정산 완료")

    st.subheader("최종 결과")

    for person, amount in sorted(
        result.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        st.write(f"**{person}** : {amount:,}원")