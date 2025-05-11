# 輸入八字, 根據 config.py 找出天干地支關係

from config import basic, relation
from lunar_python import Lunar, Solar
from datetime import datetime


def solar_to_lunar(year, month, day, hour=0, minute=0, second=0):
    """
    將國曆轉換為農曆
    :param year: 西元年
    :param month: 月
    :param day: 日
    :param hour: 時
    :param minute: 分
    :param second: 秒
    :return: 農曆日期字典
    """
    solar = Solar.fromYmdHms(year, month, day, hour, minute, second)
    lunar = solar.getLunar()
    
    return {
        "year": lunar.getYearInChinese(),  # 農曆年
        "month": lunar.getMonthInChinese(),  # 農曆月
        "day": lunar.getDayInChinese(),  # 農曆日
        "hour": lunar.getTimeZhi(),  # 時辰
        #"leap": lunar.isLeap(),  # 是否閏月
        "year_gan": lunar.getYearGan(),  # 年干
        "year_zhi": lunar.getYearZhi(),  # 年支
        "month_gan": lunar.getMonthGan(),  # 月干
        "month_zhi": lunar.getMonthZhi(),  # 月支
        "day_gan": lunar.getDayGan(),  # 日干
        "day_zhi": lunar.getDayZhi(),  # 日支
        "hour_gan": lunar.getTimeGan(),  # 時干
        "hour_zhi": lunar.getTimeZhi(),  # 時支
        "festival": lunar.getFestivals(),  # 節日
        "jie_qi": lunar.getJieQi()  # 節氣
    }

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
        results["wen_chang"]["day_stem"] = day_stem
        results["wen_chang"]["location"] = wen_chang
        # 检查四个地支中是否存在文昌贵人
        for i, branch in enumerate(earthly_branches):
            if branch == wen_chang:
                results["wen_chang"]["found_positions"].append(f"{positions[i]}支")

    return results

def get_bazi_from_solar_date(year, month, day, hour):
    """
    從西曆日期獲取八字
    :param year: 西元年
    :param month: 月
    :param day: 日
    :param hour: 時 (24小時制)
    :return: (天干列表, 地支列表)
    """
    # 使用 LunarCalendar 獲取農曆信息
    lunar_info = solar_to_lunar(year, month, day, hour)
    
    # 提取天干地支
    heavenly_stems = [
        lunar_info["year_gan"],  # 年干
        lunar_info["month_gan"],  # 月干
        lunar_info["day_gan"],   # 日干
        lunar_info["hour_gan"]   # 時干
    ]
    
    earthly_branches = [
        lunar_info["year_zhi"],  # 年支
        lunar_info["month_zhi"], # 月支
        lunar_info["day_zhi"],   # 日支
        lunar_info["hour_zhi"]   # 時支
    ]
    
    return heavenly_stems, earthly_branches

def main():
    # 獲取用戶輸入
    print("請輸入出生日期時間（西曆）：")
    try:
        year = int(input("年（西元）: "))
        month = int(input("月: "))
        day = int(input("日: "))
        hour = int(input("時（24小時制）: "))
        
        # 獲取八字
        heavenly_stems, earthly_branches = get_bazi_from_solar_date(year, month, day, hour)
        
        # 分析八字
        analysis = analyze_bazi(heavenly_stems, earthly_branches)
        
        # 輸出分析結果
        print("\n八字排盤:")
        print("=" * 40)
        print(f"出生時間: {year}年{month}月{day}日{hour}時")
        print("=" * 40)
        print(f"年柱: {heavenly_stems[0]}{earthly_branches[0]}")
        print(f"月柱: {heavenly_stems[1]}{earthly_branches[1]}")
        print(f"日柱: {heavenly_stems[2]}{earthly_branches[2]}")
        print(f"時柱: {heavenly_stems[3]}{earthly_branches[3]}")
        print("=" * 40)

        print("\n地支藏干:")
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
                
    except ValueError:
        print("輸入錯誤！請輸入有效的數字。")
    except Exception as e:
        print(f"發生錯誤：{str(e)}")

if __name__ == "__main__":
    main()