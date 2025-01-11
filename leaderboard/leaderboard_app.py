import pandas as pd

# CSV 파일 경로 설정
file_paths = [
    "../results/translation/Korean2English/leaderboard.csv",
    "../results/translation/English2Korean/leaderboard.csv",
    "../results/chatbot/coqa/leaderboard.csv",
]

# 과제 이름 설정
task_names = ["KO→EN Translation", "EN→KO Translation", "NVIDIA-ChatRAG bench"]

def highlight_best_npu(data):
    if "device-type" in data.columns and "BERTScore" in data.columns:
        npu_data = data[data["device-type"] == "NPU"]
        if not npu_data.empty:
            best_row_idx = npu_data["BERTScore"].idxmax()
            data["highlight"] = False
            data.loc[best_row_idx, "highlight"] = True
        else:
            data["highlight"] = False
    else:
        data["highlight"] = False
    return data

# 전체 테이블 컨텐츠와 필터 옵션 생성
tables_content = ""
filters_content = {"device-type": set(), "device-name": set(), "llm": set(), "quantization": set()}

for i, (file_path, task_name) in enumerate(zip(file_paths, task_names)):
    data = pd.read_csv(file_path).round(3)
    data = highlight_best_npu(data)

    for col in filters_content.keys():
        filters_content[col].update(data[col].dropna().unique())

    headers = "".join(f"<th>{col}</th>" for col in data.columns if col != "highlight")
    rows = "".join(
        f"<tr class='highlight-row'>" + "".join(f"<td>{value}</td>" for value in row[:-1]) + "</tr>"
        if row[-1] else
        f"<tr>" + "".join(f"<td>{value}</td>" for value in row[:-1]) + "</tr>"
        for row in data.values
    )

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

filter_checkboxes_html = ""
for filter_name, options in filters_content.items():
    checkboxes_html = "".join(
        f'<label><input type="checkbox" class="{filter_name}" value="{value}"> {value}</label>'
        for value in sorted(options)
    )
    filter_checkboxes_html += f"""
    <div class="filter-group">
        <h3>{filter_name.replace('-', ' ').capitalize()}</h3>
        {checkboxes_html}
    </div>
    """

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
            background-color: #1a1a1a;
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
        .filters {{
            display: none;
            margin: 20px 0;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }}
        .filters.show {{
            display: grid;
        }}
        .filter-group {{
            background-color: #282828;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        h3 {{
            font-size: 1rem;
            margin-bottom: 10px;
            color: #FFFFFF;
        }}
        label {{
            display: inline-block;
            margin-right: 15px;
            color: #CCCCCC;
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
        #toggle-filters {{
            margin-bottom: 10px;
            background-color: #424242;
            color: #FFFFFF;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .logo {{
            height: 50px;
        }}
        .highlight-row {{
            background-color: #333300 !important; /* 검은색 90%, 노란색 10% */
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Service Leaderboard</h1>
        <img src="ac6c6784959948e1aa377e8b01cfed51.webp" alt="Furiosa Logo" class="logo">
    </div>
    
    <button id="toggle-filters">Show Filters</button>
    <div class="filters">
        {filter_checkboxes_html}
        <div style="grid-column: span 4; text-align: center;">
            <button id="apply-filters" style="margin-right: 10px;">Apply Filters</button>
            <button id="clear-filters">Clear Filters</button>
        </div>
    </div>

    {tables_content}

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {{
            const tables = [];
            {''.join([f'tables.push($("#leaderboard-{i}").DataTable({{ "paging": true, "pageLength": 10, "info": false, "lengthChange": false, "searching": false, "order": [[5, "desc"]] }}));' for i in range(len(file_paths))])}

            $("#toggle-filters").on("click", function() {{
                $(".filters").toggleClass("show");
                $(this).text($(".filters").hasClass("show") ? "Hide Filters" : "Show Filters");
            }});

            $("#apply-filters").on("click", function() {{
                const filters = {{}};
                $(".filter-group").each(function() {{
                    const filterName = $(this).find("h3").text().toLowerCase().replace(' ', '-');
                    filters[filterName] = $(this).find("input:checked").map(function() {{
                        return $(this).val();
                    }}).get();
                }});

                tables.forEach((table, i) => {{
                    table.rows().every(function() {{
                        const data = this.data();
                        const matches = Object.keys(filters).every((key, index) => {{
                            return filters[key].length === 0 || filters[key].includes(data[index]);
                        }});
                        $(this.node()).toggle(matches);
                    }});
                }});
            }});

            $("#clear-filters").on("click", function() {{
                $("input[type=checkbox]").prop("checked", false);
                tables.forEach((table) => {{
                    table.rows().every(function() {{
                        $(this.node()).show();
                    }});
                }});
            }});
        }});
    </script>
</body>
</html>
"""

with open("leaderboard.html", "w", encoding="utf-8") as file:
    file.write(html_content)