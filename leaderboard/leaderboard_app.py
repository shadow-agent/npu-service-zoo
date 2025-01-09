import pandas as pd

# CSV 파일 경로 설정
file_paths = [
    "../results/translation/Korean2English/leaderboard.csv",
    "../results/translation/English2Korean/leaderboard.csv",
]

# 과제 이름 설정
task_names = ["KO→EN Translation", "EN→KO Translation"]

# 테이블들을 HTML로 연속 추가
tables_content = ""
for i, (file_path, task_name) in enumerate(zip(file_paths, task_names)):
    # CSV 데이터 로드 및 소수점 세 자리 반올림
    data = pd.read_csv(file_path).round(3)

    # 테이블 헤더와 행 생성
    headers = "".join(f"<th>{col}</th>" for col in data.columns)
    rows = "".join(
        "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
        for row in data.values
    )

    # 테이블 섹션 추가
    tables_content += f"""
    <section>
        <h2>{task_name}</h2>
        <table id="leaderboard-{i}" class="display">
            <thead>
                <tr>{headers}</tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </section>
    """

# HTML 파일 생성
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Service Leaderboard</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #121212;
            color: #E0E0E0;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #B0B0B0;
            margin: 0;
        }}
        .logo {{
            height: 50px;
        }}
        section {{
            margin-bottom: 40px;
        }}
        h2 {{
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: #B0B0B0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background-color: #323232;
            color: #FFFFFF;
            padding: 10px;
            text-align: center;
        }}
        td {{
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #2C2C2C;
        }}
        tr:hover {{
            background-color: #424242;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Service Leaderboard</h1>
        <img src="ac6c6784959948e1aa377e8b01cfed51.webp" alt="Furiosa Logo" class="logo">
    </div>
    {tables_content}

    <!-- DataTables Script -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {{
            // Initialize DataTables for all tables
            {''.join([f'$("#leaderboard-{i}").DataTable({{ "paging": true, "pageLength": 10, "info": false, "lengthChange": false, "searching": false, "order": [[7, "desc"]] }});' for i in range(len(file_paths))])}
        }});
    </script>
</body>
</html>
"""

# HTML 파일 저장
with open("leaderboard.html", "w", encoding="utf-8") as file:
    file.write(html_content)