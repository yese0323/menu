from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# 전역 변수로 소지금 관리 (초기값 10,000원)
user_data = {"balance": 10000}

# 나중에 알려주실 상품 목록을 담을 공간 (예시로 비워둡니다)
# 예: [{"id": 1, "name": "아메리카노", "price": 4000}]
products = []


@app.route("/")
def index():
    return render_template(
        "index.html", balance=user_data["balance"], products=products
    )


# 소지금 설정 API
@app.route("/set_balance", methods=["POST"])
def set_balance():
    data = request.get_json()
    new_balance = int(data.get("balance", 0))

    if new_balance < 0:
        return jsonify(
            {"success": False, "message": "금액은 0 이상이어야 합니다."}
        )

    user_data["balance"] = new_balance
    return jsonify(
        {
            "success": True,
            "balance": user_data["balance"],
            "message": f"소지금이 {new_balance:,}원으로 설정되었습니다.",
        }
    )


# 상품 구매 API (나중에 상품이 생기면 작동합니다)
@app.route("/buy/<int:product_id>", methods=["POST"])
def buy_product(product_id):
    # 상품 찾기 로직 (추후 상품 데이터 구조에 맞춰 완성될 예정)
    # 현재는 틀만 잡아둡니다.
    return jsonify({"success": False, "message": "아직 상품이 등록되지 않았습니다."})


if __name__ == "__main__":
    app.run(debug=True)
