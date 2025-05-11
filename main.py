# 輸入八字, 根據 config.py 找出天干地支關係

from config import basic, relation
from lunar_python import Lunar, Solar
from datetime import datetime, timedelta


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

    
    ThisJieQi = lunar.getPrevJieQi().getName()  # 當前節氣
    NextJieQi = lunar.getNextJieQi().getName()  # 下一節氣

    this_jie_qi_starttime = lunar.getJieQiTable()[ThisJieQi].toYmdHms()
    next_jie_qi_starttime = lunar.getJieQiTable()[NextJieQi].toYmdHms()

    # 计算到下一节气的时间间隔
    birth_time = datetime(year, month, day, hour)
    this_jie_qi_time = datetime.strptime(this_jie_qi_starttime, "%Y-%m-%d %H:%M:%S")
    next_jie_qi_time = datetime.strptime(next_jie_qi_starttime, "%Y-%m-%d %H:%M:%S")
    time_to_this_jq = birth_time - this_jie_qi_time 
    time_to_next_jq = next_jie_qi_time - birth_time

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
        "this_jie_qi": ThisJieQi,  # 當前節氣
        "next_jie_qi": NextJieQi,  # 下一節氣
        "this_jie_qi_starttime" : this_jie_qi_starttime, # 當前節氣開始時間
        "next_jie_qi_starttime" : next_jie_qi_time,# 下一節氣開始時間
        "time_to_this_jq" : time_to_this_jq,
        "time_to_next_jq" : time_to_next_jq,
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


def get_bazi_from_solar_date(lunar_info):
    """
    從西曆日期獲取八字
    :param lunar_info: 農曆信息字典
    :return: (天干列表, 地支列表)
    """
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

def get_start_luck(lunar_info, gender, birth_date):
    """
    計算大運起始時間和年齡
    :param lunar_info: 農曆信息字典
    :param gender: 性別 (1:男, 0:女)
    :param birth_date: 出生日期時間
    :return: 大運信息字典
    """
    # 計大運法：3日=1歲,1日=4個月,1時辰=10日
    time_to_next_jq = lunar_info["time_to_next_jq"]
    print(time_to_next_jq)
    days = time_to_next_jq.days
    hours = time_to_next_jq.seconds // 3600

    # 計算大運起始年齡
    years = days // 3
    remaining_days = days % 3
    months = remaining_days * 4
    days = hours * 10
    
    # 計算大運起始時間
    luck_start_date = birth_date + timedelta(days=days + (years * 365) + (months * 30))
    
    return {
        "start_age": {
            "years": years,
            "months": months,
            "days": days
        },
        "start_date": luck_start_date,
        "gender": "男" if gender == 1 else "女",
        "year_gan": lunar_info["year_gan"],
        "month_gan": lunar_info["month_gan"],
        "month_zhi": lunar_info["month_zhi"]
    }


def get_luck_pillars(luck_info):
    """
    計算大運干支
    :param luck_info: 大運信息
    :return: 大運干支列表
    """
    gan = basic.heavenly_stems
    zhi = basic.earthly_branches
    
    month_gan = luck_info["month_gan"]
    month_zhi = luck_info["month_zhi"]
    gender = luck_info["gender"]
    year_gan = luck_info["year_gan"]
    
    # 判斷順行或逆行
    is_forward = (gender == "男" and year_gan in ["甲", "丙", "戊", "庚", "壬"]) or \
                 (gender == "女" and year_gan in ["乙", "丁", "己", "辛", "癸"])
    
    luck_pillars = []
    for i in range(8):  # 計算8個大運
        if is_forward:
            # 順行
            gan_index = (gan.index(month_gan) + i) % 10
            zhi_index = (zhi.index(month_zhi) + i) % 12
        else:
            # 逆行
            gan_index = (gan.index(month_gan) - i) % 10
            zhi_index = (zhi.index(month_zhi) - i) % 12
        
        luck_pillars.append(f"{gan[gan_index]}{zhi[zhi_index]}")
    
    return luck_pillars

def main():
    # 獲取用戶輸入
    print("請輸入出生日期時間（西曆）：")
    try:
        year = int(input("年（西元）: "))
        month = int(input("月: "))
        day = int(input("日: "))
        hour = int(input("時（24小時制）: "))
        gender = int(input("男1 女0: "))

        # 使用 LunarCalendar 獲取農曆信息
        lunar_info = solar_to_lunar(year, month, day, hour)
        birth_date = datetime(year, month, day, hour)

        # 獲取八字
        heavenly_stems, earthly_branches = get_bazi_from_solar_date(lunar_info)
        
        # 計算大運信息
        luck_info = get_start_luck(lunar_info, gender, birth_date)
        
        # 計算大運干支
        luck_pillars = get_luck_pillars(luck_info)
        
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
        
        # 輸出大運信息
        print("\n大運信息:")
        print(f"性別: {luck_info['gender']}")
        print(f"起運時間: {luck_info['start_date'].strftime('%Y年%m月%d日')}")
        print(f"起運年齡: {luck_info['start_age']['years']}歲{luck_info['start_age']['months']}個月{luck_info['start_age']['days']}日")
        print("\n大運干支:")
        for i, pillar in enumerate(luck_pillars):
            start_age = luck_info['start_age']['years'] + i * 10
            print(f"{start_age}-{start_age+9}歲: {pillar}")

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