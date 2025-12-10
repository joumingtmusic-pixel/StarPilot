"""
價格監控 API - Render 部署範例
提供 RESTful API 查詢商品價格

使用方式：
1. 本地測試：python render_範例_價格監控API.py
2. 部署到 Render
3. API 端點：https://your-app.onrender.com/api/prices
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 模擬資料庫（實際應用中應使用真實資料庫）
price_data = {
    "產品A": {
        "current_price": 1200,
        "last_update": datetime.now().isoformat(),
        "history": [
            {"date": "2024-01-01", "price": 1000},
            {"date": "2024-01-15", "price": 1100},
            {"date": "2024-02-01", "price": 1200}
        ]
    },
    "產品B": {
        "current_price": 850,
        "last_update": datetime.now().isoformat(),
        "history": [
            {"date": "2024-01-01", "price": 900},
            {"date": "2024-01-15", "price": 875},
            {"date": "2024-02-01", "price": 850}
        ]
    },
    "產品C": {
        "current_price": 1500,
        "last_update": datetime.now().isoformat(),
        "history": [
            {"date": "2024-01-01", "price": 1400},
            {"date": "2024-01-15", "price": 1450},
            {"date": "2024-02-01", "price": 1500}
        ]
    }
}


@app.route('/')
def home():
    """首頁 - API 說明"""
    return jsonify({
        "message": "價格監控 API",
        "version": "1.0.0",
        "endpoints": {
            "/api/prices": "取得所有產品價格",
            "/api/prices/<product>": "取得特定產品價格",
            "/api/health": "健康檢查"
        },
        "example": "GET /api/prices/產品A"
    })


@app.route('/api/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/prices')
def get_all_prices():
    """取得所有產品的價格"""
    try:
        return jsonify({
            "success": True,
            "data": price_data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/prices/<product>')
def get_product_price(product):
    """取得特定產品的價格"""
    try:
        if product in price_data:
            return jsonify({
                "success": True,
                "product": product,
                "data": price_data[product],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"找不到產品：{product}",
                "available_products": list(price_data.keys())
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/prices/<product>/history')
def get_price_history(product):
    """取得產品的歷史價格"""
    try:
        if product in price_data:
            return jsonify({
                "success": True,
                "product": product,
                "history": price_data[product]["history"],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"找不到產品：{product}"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/prices/compare')
def compare_prices():
    """比較多個產品的價格"""
    try:
        # 從查詢參數取得產品列表
        products = request.args.get('products', '').split(',')

        result = {}
        for product in products:
            product = product.strip()
            if product in price_data:
                result[product] = price_data[product]["current_price"]

        if not result:
            return jsonify({
                "success": False,
                "error": "請提供有效的產品名稱",
                "example": "/api/prices/compare?products=產品A,產品B"
            }), 400

        # 找出最便宜和最貴的產品
        cheapest = min(result.items(), key=lambda x: x[1])
        expensive = max(result.items(), key=lambda x: x[1])

        return jsonify({
            "success": True,
            "comparison": result,
            "cheapest": {
                "product": cheapest[0],
                "price": cheapest[1]
            },
            "most_expensive": {
                "product": expensive[0],
                "price": expensive[1]
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理"""
    return jsonify({
        "success": False,
        "error": "找不到該端點",
        "available_endpoints": [
            "/",
            "/api/health",
            "/api/prices",
            "/api/prices/<product>",
            "/api/prices/<product>/history",
            "/api/prices/compare"
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理"""
    return jsonify({
        "success": False,
        "error": "伺服器內部錯誤"
    }), 500


if __name__ == '__main__':
    # Render 會自動設定 PORT 環境變數
    port = int(os.environ.get('PORT', 5000))

    # 開發模式
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"""
    🚀 價格監控 API 已啟動
    📍 本地網址：http://localhost:{port}
    📡 可用端點：
       - GET /                      # API 說明
       - GET /api/health            # 健康檢查
       - GET /api/prices            # 所有產品價格
       - GET /api/prices/產品A      # 特定產品價格
       - GET /api/prices/產品A/history  # 價格歷史
       - GET /api/prices/compare?products=產品A,產品B  # 價格比較
    """)

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
