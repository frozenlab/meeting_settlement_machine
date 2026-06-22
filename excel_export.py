from io import BytesIO
import pandas as pd

def create_excel(result, details, items, food_price, unit):
    result_df = pd.DataFrame(
        [
            {
                "이름": person,
                "정산금액": amount
            }
            for person, amount in result.items()
        ]
    )
    detail_rows = []

    for person, detail_list in details.items():
        for detail in detail_list:
            detail_rows.append({
                "이름" : person, "내역" : detail
            })
    detail_df = pd.DataFrame(detail_rows)

    item_df = pd.DataFrame(
        [
            {
                "항목명" : item.name,
                "금액" : item.price,
                "메모" : item.memo
            }
            for item in items
        ]
    )

    food_df = pd.DataFrame(
        [
            {
                "음식총액": food_price,
                "잔액처리단위": unit
            }
        ]
    )

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        result_df.to_excel(writer, sheet_name = "정산결과", index = False)
        detail_df.to_excel(writer, sheet_name = "추가부담내역", index = False)
        item_df.to_excel(writer, sheet_name = "항목내역", index = False)
        food_df.to_excel(writer, sheet_name = "설정", index = False)
    
    return buffer.getvalue()