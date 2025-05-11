# 輸入八字, 根據 config.py 找出天干地支關係

from config import basic, relation

def analyze_bazi(heavenly_stems, earthly_branches):
    """
    分析八字，找出天干地支的關係
    :param heavenly_stems: 天干列表 [年干, 月干, 日干, 時干]
    :param earthly_branches: 地支列表 [年支, 月支, 日支, 時支]
    :return: 分析結果
    """
    positions = ["年", "月", "日", "時"]
    results = {
        "hidden_stems": [],
        "heavenly_relations": [],
        "branch_relations": [],
        "wen_chang": {
            "day_stem": None,
            "location": None,
            "found_positions": []
        }
    }

    # 找出地支藏干
    for i, branch in enumerate(earthly_branches):
        hidden = basic.hidden_stems.get(branch, [])
        results["hidden_stems"].append({f"{positions[i]}支 {branch}": hidden})

    # 找出天干相合關係並計算相合後的五行
    for i, stem1 in enumerate(heavenly_stems):
        for j, stem2 in enumerate(heavenly_stems):
            if i < j and stem2 in relation.heavenly_relations["合"].get(stem1, []):
                combined_element = relation.get_combined_element(stem1, stem2)
                if combined_element:
                    results["heavenly_relations"].append(
                        f"{positions[i]}干 {stem1} 合 {positions[j]}干 {stem2} 化為 {combined_element}"
                    )
                else:
                    results["heavenly_relations"].append(
                        f"{positions[i]}干 {stem1} 合 {positions[j]}干 {stem2}"
                    )

    # 找出地支關係
    for i, branch1 in enumerate(earthly_branches):
        for j, branch2 in enumerate(earthly_branches):
            if i < j:
                # 檢查六合關係
                if branch2 in relation.branch_relations["六合"].get(branch1, []):
                    element = relation.get_branch_combined_element(branch1, branch2)
                    if element:
                        results["branch_relations"].append(
                            f"{positions[i]}支 {branch1} 六合 {positions[j]}支 {branch2} 化為 {element}"
                        )
                    else:
                        results["branch_relations"].append(
                            f"{positions[i]}支 {branch1} 六合 {positions[j]}支 {branch2}"
                        )

                # 檢查半三合關係
                element = relation.get_half_combine_element(branch1, branch2)
                if element:
                    results["branch_relations"].append(
                        f"{positions[i]}支 {branch1} 半三合 {positions[j]}支 {branch2} 化為 {element}"
                    )

                # 檢查拱合關係
                element = relation.get_arch_combine_element(branch1, branch2)
                if element:
                    results["branch_relations"].append(
                        f"{positions[i]}支 {branch1} 拱 {positions[j]}支 {branch2} 化為 {element}"
                    )

                # 檢查三合關係（需要三個地支）
                for k, branch3 in enumerate(earthly_branches):
                    if j < k:
                        element = relation.get_three_combine_element(branch1, branch2, branch3)
                        if element:
                            results["branch_relations"].append(
                                f"{positions[i]}支 {branch1} {positions[j]}支 {branch2} {positions[k]}支 {branch3} 三合化為 {element}"
                            )

    # 查找文昌贵人（使用日干）
    day_stem = heavenly_stems[2]  # 日干
    wen_chang = relation.get_wen_chang(day_stem)
    if wen_chang:
        results["wen_chang"] = f"日干 {day_stem} 的文昌貴人在 {wen_chang}"

    return results

# 測試輸入八字
heavenly_stems_input = ["庚", "戊", "乙", "丙"]  # [年干, 月干, 日干, 時干]
earthly_branches_input = ["午", "戌", "卯", "戌"]  # [年支, 月支, 日支, 時支]

analysis = analyze_bazi(heavenly_stems_input, earthly_branches_input)

# 輸出分析結果
print("地支藏干:")
for hidden in analysis["hidden_stems"]:
    for position, stems in hidden.items():
        print(f"{position} 藏干: {', '.join(stems)}")

print("\n天干相合關係:")
for relation in analysis["heavenly_relations"]:
    print(relation)

print("\n地支關係:")
for relation in analysis["branch_relations"]:
    print(relation)

print("\n文昌貴人:")
wen_chang = analysis["wen_chang"]
if wen_chang["day_stem"]:
    print(f"日干 {wen_chang['day_stem']} 的文昌貴人在 {wen_chang['location']}")
    if wen_chang["found_positions"]:
        print(f"在八字中出現在: {', '.join(wen_chang['found_positions'])}")
    else:
        print("在八字中未出現文昌貴人")