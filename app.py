import streamlit as st

# 페이지 설정
st.set_page_config(page_title="진로부스 상점", page_icon="🎯")

st.title("진로부스 상점")
st.write("진로부스 체험을 통해 얻은 코인으로 다양한 상품을 구매해 보세요!")

# 1. 세션 상태 초기화 (소지금, 인벤토리)
if "coin_balance" not in st.session_state:
    st.session_state.coin_balance = 100  # 초기 코인 기본값

if "inventory" not in st.session_state:
    st.session_state.inventory = []

# 2. 소지금(코인) 설정 및 표시 영역
st.header("💰 보유 코인 관리")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 현재 소지금: **{st.session_state.coin_balance:,} 코인**")

with col2:
    custom_coin = st.number_input("코인 설정", min_value=0, value=st.session_state.coin_balance, step=10)
    if st.button("코인 적용하기"):
        st.session_state.coin_balance = custom_coin
        st.success(f"소지금이 {custom_coin:,} 코인으로 설정되었습니다!")
        st.rerun()

st.divider()

# 3. 상품 목록 영역 (추후 상품과 가격을 알려주시면 이곳에 추가됩니다)
st.header("🛍️ 진로부스 상품 목록")
st.info("💡 아직 등록된 상품이 없습니다. 판매할 상품 이름과 가격(코인)을 알려주세요!")

# (예시용 뼈대 코드 - 나중에 상품 데이터가 들어오면 이 부분이 활성화됩니다)
# products = [
#     {"id": 1, "name": "상품이름1", "price": 30},
#     {"id": 2, "name": "상품이름2", "price": 50}
# ]

st.divider()

# 4. 구매 인벤토리(가방) 영역
st.header("🎒 내가 구매한 상품")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.write(- f"{item}")
else:
    st.write("아직 구매한 상품이 없습니다.")
