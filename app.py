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
# [1단계] 부스 시작 전: 초기 소지금 및 상품별 개수(재고) 설정 화면
# ==========================================
if not st.session_state.setup_done:
    st.title("⚙️ 진로부스 상점 세팅 페이지")
    st.write("참가자의 **초기 소지금**과 각 **상품별 개수(재고)**를 설정한 뒤 상점을 열어주세요.")

    # 1. 초기 소지금 설정
    initial_coin = st.number_input("참가자 초기 소지금 (코인)", min_value=0, value=100, step=10)

    st.divider()

    st.subheader("📦 상품별 초기 개수(재고) 설정")
    st.write("상품들의 가격과 함께 준비된 수량을 입력해 주세요.")

    # 기본 상품 템플릿 데이터 (이름, 가격) - 젤리 항목 추가 완료!
    default_items = [
        {"name": "버터", "price": 12},
        {"name": "강아지 키링", "price": 20},
        {"name": "주사위 키링", "price": 20},
        {"name": "키캡 (정상)", "price": 25},
        {"name": "키캡 (비정상)", "price": 12},
        {"name": "퉁퉁퉁 사후르", "price": 28},
        {"name": "고오급볼펜", "price": 35},
        {"name": "과일젤리", "price": 3},
        {"name": "스키틀즈", "price": 3},
        {"name": "???", "price": 70}
    ]

    # 세션에 상품 리스트가 아직 없다면 기본 상품들을 불러와 초기화
    if not st.session_state.products:
        st.session_state.products = [
            {"name": item["name"], "price": item["price"], "stock": 10} for item in default_items
        ]

    # 각 상품별 재고 수량을 조절할 수 있는 입력 필드 생성
    updated_products = []
    for idx, prod in enumerate(st.session_state.products):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{prod['name']}**")
        with col2:
            st.markdown(f"💰 {prod['price']} 코인")
        with col3:
            new_stock = st.number_input(
                f"{prod['name']} 개수", 
                min_value=0, 
                value=prod['stock'], 
                step=1, 
                key=f"stock_input_{idx}",
                label_visibility="collapsed"
            )
        
        updated_products.append({
            "name": prod['name'],
            "price": prod['price'],
            "stock": new_stock
        })
        st.divider()

    # 상점 오픈 버튼
    if st.button("🚀 상점 오픈하기!", type="primary", use_container_width=True):
        st.session_state.coin_balance = initial_coin
        st.session_state.products = updated_products
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
    
    # 설정된 상품들을 순회하며 화면에 출력
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
    
