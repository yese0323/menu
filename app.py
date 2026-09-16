import streamlit as st

st.set_page_config(page_title="나만의 상점 메뉴판", page_icon="🛒")

st.title("🛒 나만의 상점 메뉴판")

# 세션 상태를 이용해 소지금과 구매 내역 관리 (새로고침해도 유지)
if "balance" not in st.session_state:
    st.session_state.balance = 10000

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# 1. 소지금 설정 영역
st.header("보유 자산")
st.write(f"현재 소지금: **{st.session_state.balance:,}원**")

new_balance = st.number_input("소지금 설정", min_value=0, value=st.session_state.balance, step=1000)
if st.button("소지금 변경 적용"):
    st.session_state.balance = new_balance
    st.success(f"소지금이 {new_balance:,}원으로 설정되었습니다!")
    st.rerun()

st.divider()

# 2. 상품 목록 영역 (나중에 상품을 채워넣을 공간)
st.header("상품 목록")
st.info("상품과 가격을 알려주시면 이곳에 구매 버튼이 생성됩니다!")

# (참고용 예시 상품 구조)
# products = [{"name": "아메리카노", "price": 4000}]
