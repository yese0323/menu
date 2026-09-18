import streamlit as st
from collections import Counter

# 페이지 설정
st.set_page_config(page_title="진로부스 상점", page_icon="🎯", layout="wide")

# 세션 상태 초기화
if "setup_done" not in st.session_state:
    st.session_state.setup_done = False
if "coin_balance" not in st.session_state:
    st.session_state.coin_balance = 100
if "products" not in st.session_state:
    st.session_state.products = []
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# ==========================================
# [1단계] 부스 시작 전: 상품 및 초기 소지금 설정 화면
# ==========================================
if not st.session_state.setup_done:
    st.title("⚙️ 진로부스 상점 세팅 페이지")
    st.write("부스를 시작하기 전에 참가자 초기 소지금과 **판매할 여러 개의 상품**을 등록해 주세요.")

    # 초기 소지금 설정
    initial_coin = st.number_input("참가자 초기 소지금 (코인)", min_value=0, value=100, step=10)

    st.divider()

    st.subheader("🛍️ 여러 개의 상품 등록하기")
    st.write("상품명, 가격, 개수를 입력하고 **'상품 추가'**를 누르면 아래 리스트에 계속해서 추가됩니다.")

    # 상품 입력 폼 (폼 내부에 고유 키값 부여)
    with st.form("multi_product_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            p_name = st.text_input("상품명 (예: 볼펜, 키링, 간식 등)")
        with col2:
            p_price = st.number_input("상품 가격 (코인)", min_value=0, value=10, step=1)
        with col3:
            p_stock = st.number_input("상품 개수 (재고)", min_value=1, value=10, step=1)
        
        submitted = st.form_submit_button("➕ 상품 추가하기")
        if submitted:
            if p_name.strip() == "":
                st.warning("상품명을 올바르게 입력해주세요!")
            else:
                st.session_state.products.append({
                    "name": p_name,
                    "price": p_price,
                    "stock": p_stock
                })
                st.success(f"'{p_name}'이(가) 리스트에 추가되었습니다!")

    # 현재 추가된 상품 목록 리스트 확인 및 삭제 기능
    st.divider()
    st.markdown(f"### 📋 등록된 상품 리스트 (총 {len(st.session_state.products)}개)")
    
    if st.session_state.products:
        for idx, prod in enumerate(st.session_state.products):
            col_a, col_b, col_c, col_d = st.columns([3, 2, 2, 1])
            col_a.write(f"**{idx+1}. {prod['name']}**")
            col_b.write(f"가격: {prod['price']} 코인")
            col_c.write(f"재고: {prod['stock']} 개")
            if col_d.button("삭제", key=f"del_prod_{idx}"):
                st.session_state.products.pop(idx)
                st.rerun()
    else:
        st.info("아직 추가된 상품이 없습니다. 위에서 상품을 추가해 보세요.")

    st.divider()

    # 상점 오픈 버튼
    if st.button("🚀 상점 오픈하기!", type="primary", use_container_width=True):
        if not st.session_state.products:
            st.error("최소 1개 이상의 상품을 등록해야 상점을 오픈할 수 있습니다!")
        else:
            st.session_state.coin_balance = initial_coin
            st.session_state.setup_done = True
            st.rerun()

# ==========================================
# [2단계] 상점 오픈 후: 실제 구매 및 이용 화면
# ==========================================
else:
    # 사이드바 설정
    with st.sidebar:
        st.title("🛒 진로부스 메뉴판")
        st.markdown(f"### 현재 소지금: **{st.session_state.coin_balance:,} 코인**")
        
        # 소지금 수동 조절
        new_bal = st.number_input("소지금 수동 변경", min_value=0, value=st.session_state.coin_balance, step=10)
        if st.button("잔액 반영"):
            st.session_state.coin_balance = new_bal
            st.rerun()

        st.divider()
        if st.button("🔄 세팅 화면으로 돌아가기 (초기화)"):
            st.session_state.setup_done = False
            st.session_state.products = []
            st.session_state.inventory = []
            st.rerun()

    # 메인 상점 화면
    st.title("🎯 진로부스 상점")
    st.write("원하는 상품을 골라 코인으로 구매해 보세요!")

    st.header("🛍️ 상품 목록")
    
    # 여러 개 등록된 상품들을 순회하며 화면에 출력
    for idx, prod in enumerate(st.session_state.products):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        col1.markdown(f"### {prod['name']}")
        col2.markdown(f"💰 **{prod['price']}** 코인")
        
        # 재고 확인 및 구매 버튼 처리
        if prod['stock'] > 0:
            col3.markdown(f"📦 남은 개수: **{prod['stock']}**개")
            buy_btn = col4.button("구매하기", key=f"buy_item_{idx}")
            
            if buy_btn:
                if st.session_state.coin_balance >= prod['price']:
                    st.session_state.coin_balance -= prod['price']
                    prod['stock'] -= 1
                    st.session_state.inventory.append(prod['name'])
                    st.success(f"'{prod['name']}' 구매 완료!")
                    st.rerun()
                else:
                    st.error("보유 코인이 부족합니다!")
        else:
            col3.markdown("❌ **품절**")
            col4.button("품절", key=f"sold_item_{idx}", disabled=True)
            
        st.divider()

    # 구매 인벤토리(가방) 영역
    st.header("🎒 내가 구매한 상품 목록")
    if st.session_state.inventory:
        item_counts = Counter(st.session_state.inventory)
        for item_name, count in item_counts.items():
            st.write(f"- **{item_name}** : {count}개")
    else:
        st.write("아직 구매한 상품이 없습니다.")
