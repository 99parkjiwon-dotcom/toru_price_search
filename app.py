from flask import Flask, request
import urllib.parse
import pandas as pd

app = Flask(__name__)

def coupang_link(product):
    q = urllib.parse.quote(product)
    return f"https://www.coupang.com/np/search?q={q}"

def naver_link(product):
    q = urllib.parse.quote(product)
    return f"https://search.shopping.naver.com/search/all?query={q}"

def google_link(product):
    q = urllib.parse.quote(product)
    return f"https://www.google.com/search?tbm=shop&q={q}"


@app.route("/", methods=["GET", "POST"])
def home():
    single_cards = ""
    excel_rows = []

    if request.method == "POST":
        if request.form.get("type") == "single":
            product = request.form.get("product")
            single_cards = f"""
            <div class="card"><a href="{coupang_link(product)}" target="_blank">쿠팡 검색 →</a></div>
            <div class="card"><a href="{naver_link(product)}" target="_blank">네이버 쇼핑 →</a></div>
            <div class="card"><a href="{google_link(product)}" target="_blank">구글 쇼핑 →</a></div>
            """

        if request.form.get("type") == "excel":
            file = request.files.get("file")
            df = pd.read_excel(file)
            for product in df["product"].dropna():
                excel_rows.append(f"""
                <tr>
                    <td>{product}</td>
                    <td><a href="{coupang_link(product)}" target="_blank">쿠팡</a></td>
                    <td><a href="{naver_link(product)}" target="_blank">네이버</a></td>
                    <td><a href="{google_link(product)}" target="_blank">구글</a></td>
                </tr>
                """)

    excel_rows_html = "".join(excel_rows)

    return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>토루 최저가 검색</title>

<!-- Fonts -->
<link href="https://cdn.jsdelivr.net/gh/sunn-us/SUIT/fonts/static/woff2/SUIT.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
body {{
    margin: 0;
    background: #f3f6fb;
    font-family: SUIT, Inter, -apple-system;
    color: #0f172a;
}}

header {{
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    padding: 40px 20px;
    text-align: center;
}}

header h1 {{
    font-size: 34px;
    margin-bottom: 8px;
}}

header p {{
    opacity: 0.9;
}}

.container {{
    max-width: 1000px;
    margin: -40px auto 60px;
    padding: 0 20px;
}}

.section {{
    background: white;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(15,23,42,0.08);
}}

.section h2 {{
    margin-bottom: 6px;
}}

.section .desc {{
    color: #64748b;
    margin-bottom: 20px;
}}

form {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}}

input[type=text] {{
    flex: 1;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    font-size: 16px;
}}

button {{
    padding: 16px 26px;
    border-radius: 12px;
    border: none;
    background: #2563eb;
    color: white;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
}}

button:hover {{
    background: #1d4ed8;
}}

.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 18px;
    margin-top: 24px;
}}

.card {{
    background: #f8fafc;
    border-radius: 16px;
    padding: 26px;
    text-align: center;
    font-weight: 600;
    box-shadow: inset 0 0 0 1px #e5e7eb;
}}

.card a {{
    text-decoration: none;
    color: #2563eb;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 24px;
}}

th, td {{
    padding: 14px;
    border-bottom: 1px solid #e5e7eb;
    text-align: center;
}}

th {{
    background: #f8fafc;
    font-weight: 600;
}}

a {{
    color: #2563eb;
    font-weight: 600;
    text-decoration: none;
}}
</style>
</head>

<body>

<header>
    <h1>토루 최저가 검색</h1>
    <p>단일 검색 & 엑셀 업로드로 빠르게 최저가 탐색</p>
</header>

<div class="container">

    <div class="section">
        <h2>제품 단일 검색</h2>
        <div class="desc">하나의 제품을 바로 검색합니다</div>
        <form method="post">
            <input type="hidden" name="type" value="single">
            <input name="product" placeholder="예: 아이패드 프로 11인치" required>
            <button>검색</button>
        </form>
        <div class="cards">{single_cards}</div>
    </div>

    <div class="section">
        <h2>엑셀 업로드 검색</h2>
        <div class="desc">여러 제품을 한 번에 검색합니다</div>
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="type" value="excel">
            <input type="file" name="file" accept=".xlsx" required>
            <button>업로드</button>
        </form>

        <table>
            <tr>
                <th>제품명</th>
                <th>쿠팡</th>
                <th>네이버</th>
                <th>구글</th>
            </tr>
            {excel_rows_html}
        </table>
    </div>

</div>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)