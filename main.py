from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def slope_score(avg):
    if avg < 10:
        return 15
    elif avg < 15:
        return 8
    else:
        return 0

def hard_cut(farm, eco):
    if farm == "Y":
        return False
    if eco == 1:
        return False
    return True

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <title>태양광 부지 판정</title>
        </head>
        <body>
            <h2>태양광 부지 판정 프로그램</h2>

            <label>평균 경사도:</label><br>
            <input type="number" id="slope" value="12"><br><br>

            <label>농업진흥구역 여부:</label><br>
            <select id="farm">
                <option value="N">아님</option>
                <option value="Y">해당</option>
            </select><br><br>

            <label>생태자연도 등급:</label><br>
            <select id="eco">
                <option value="3">3등급</option>
                <option value="2">2등급</option>
                <option value="1">1등급</option>
            </select><br><br>

            <button onclick="check()">판정하기</button>

            <h3 id="result"></h3>

            <script>
                function check() {
                    let slope = document.getElementById("slope").value;
                    let farm = document.getElementById("farm").value;
                    let eco = document.getElementById("eco").value;

                    fetch(`/check?slope=${slope}&farm=${farm}&eco=${eco}`)
                        .then(res => res.json())
                        .then(data => {
                            document.getElementById("result").innerText =
                                "판정 결과: " + (data.판정 || data.result);
                        });
                }
            </script>
        </body>
    </html>
    """

@app.get("/check")
def check(slope: float, farm: str, eco: int):
    if not hard_cut(farm, eco):
        return {"판정": "진행 비추천"}

    score = slope_score(slope)

    if score >= 15:
        result = "진행 유망"
    elif score >= 8:
        result = "조건부 가능"
    else:
        result = "진행 비추천"

    return {
        "경사점수": score,
        "판정": result
    }
