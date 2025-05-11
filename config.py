class basic:
    # 定義十天干
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

    # 定義十二支
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 定義十天干的陰陽
    

    # 修正後的地支藏干
    hidden_stems = {
        "子": ["癸"],  # 子藏癸
        "丑": ["己", "癸", "辛"],  # 丑藏己、癸、辛
        "寅": ["甲", "丙", "戊"],  # 寅藏甲、丙、戊
        "卯": ["乙"],  # 卯藏乙
        "辰": ["戊", "乙", "癸"],  # 辰藏戊、乙、癸
        "巳": ["丙", "庚", "戊"],  # 巳藏丙、庚、戊
        "午": ["丁", "己"],  # 午藏丁、己
        "未": ["己", "丁", "乙"],  # 未藏己、丁、乙
        "申": ["庚", "壬", "戊"],  # 申藏庚、壬、戊
        "酉": ["辛"],  # 酉藏辛
        "戌": ["戊", "辛", "丁"],  # 戌藏戊、辛、丁
        "亥": ["壬", "甲"],  # 亥藏壬、甲
    }

class relation:  
    # 定義天干相合關係
    heavenly_relations = {
        "合": {
            "甲": ["己"],  # 甲合己
            "乙": ["庚"],  # 乙合庚
            "丙": ["辛"],  # 丙合辛
            "丁": ["壬"],  # 丁合壬
            "戊": ["癸"],  # 戊合癸
            "己": ["甲"],  # 己合甲
            "庚": ["乙"],  # 庚合乙
            "辛": ["丙"],  # 辛合丙
            "壬": ["丁"],  # 壬合丁
            "癸": ["戊"]   # 癸合戊
        }
    }  

    # 定義天干相合後的五行
    heavenly_relations_elements = {
        ("甲", "己"): "土",  # 甲己合化土
        ("乙", "庚"): "金",  # 乙庚合化金
        ("丙", "辛"): "水",  # 丙辛合化水
        ("丁", "壬"): "木",  # 丁壬合化木
        ("戊", "癸"): "火"   # 戊癸合化火
    }

    @staticmethod
    def get_combined_element(stem1, stem2):
        """
        獲取兩個天干相合後的五行
        :param stem1: 第一個天干
        :param stem2: 第二個天干
        :return: 相合後的五行 (如果存在相合關係)
        """
        pair = (stem1, stem2) if (stem1, stem2) in relation.heavenly_relations_elements else (stem2, stem1)
        return relation.heavenly_relations_elements.get(pair, None)

    # 定義地支刑沖剋害關係
    branch_relations = {
        "刑": {
            "子": ["卯"],  # 子刑卯
            "丑": ["戌", "未"],  # 丑刑戌、未
            "寅": ["巳", "申"],  # 寅刑巳、申
            "卯": ["子"],  # 卯刑子
            "辰": ["辰"],  # 辰自刑
            "巳": ["寅", "巳"],  # 巳刑寅、自刑
            "午": ["午"],  # 午自刑
            "未": ["丑", "戌"],  # 未刑丑、戌
            "申": ["寅"],  # 申刑寅
            "酉": ["酉"],  # 酉自刑
            "戌": ["丑", "未"],  # 戌刑丑、未
            "亥": ["亥"]  # 亥自刑
        },
        "沖": {
            "子": ["午"],  # 子沖午
            "丑": ["未"],  # 丑沖未
            "寅": ["申"],  # 寅沖申
            "卯": ["酉"],  # 卯沖酉
            "辰": ["戌"],  # 辰沖戌
            "巳": ["亥"],  # 巳沖亥
            "午": ["子"],  # 午沖子
            "未": ["丑"],  # 未沖丑
            "申": ["寅"],  # 申沖寅
            "酉": ["卯"],  # 酉沖卯
            "戌": ["辰"],  # 戌沖辰
            "亥": ["巳"]  # 亥沖巳
        },
        "害": {
            "子": ["未"],  # 子害未
            "丑": ["午"],  # 丑害午
            "寅": ["巳"],  # 寅害巳
            "卯": ["辰"],  # 卯害辰
            "辰": ["卯"],  # 辰害卯
            "巳": ["寅"],  # 巳害寅
            "午": ["丑"],  # 午害丑
            "未": ["子"],  # 未害子
            "申": ["亥"],  # 申害亥
            "酉": ["戌"],  # 酉害戌
            "戌": ["酉"],  # 戌害酉
            "亥": ["申"]  # 亥害申
        }
    }
    # 定義地支六合關係（原 branch_relations["合"]）
    branch_relations["六合"] = {
        "子": ["丑"],  # 子丑合
        "丑": ["子"],  # 丑合子
        "寅": ["亥"],  # 寅亥合
        "卯": ["戌"],  # 卯戌合
        "辰": ["酉"],  # 辰酉合
        "巳": ["申"],  # 巳申合
        "午": ["未"],  # 午未合
        "未": ["未"],  # 午未合
        "申": ["巳"],  # 申合巳
        "酉": ["辰"],  # 酉合辰
        "戌": ["卯"],  # 戌合卯
        "亥": ["寅"]   # 亥合寅
    }

    # 定義地支三合關係
    branch_relations["三合"] = {
        "申": ["子", "辰"],  # 申子辰三合水局
        "亥": ["卯", "未"],  # 亥卯未三合木局
        "寅": ["午", "戌"],  # 寅午戌三合火局
        "巳": ["酉", "丑"]   # 巳酉丑三合金局
    }

    # 三合局五行屬性
    branch_three_combine_elements = {
        ("申", "子", "辰"): "水",  # 申子辰三合水局
        ("亥", "卯", "未"): "木",  # 亥卯未三合木局
        ("寅", "午", "戌"): "火",  # 寅午戌三合火局
        ("巳", "酉", "丑"): "金"   # 巳酉丑三合金局
    }

    # 半三合关系
    branch_half_combine = {
        ("申", "子"): "水",  # 申子半合水
        ("子", "辰"): "水",  # 子辰半合水
        ("亥", "卯"): "木",  # 亥卯半合木
        ("卯", "未"): "木",  # 卯未半合木
        ("寅", "午"): "火",  # 寅午半合火
        ("午", "戌"): "火",  # 午戌半合火
        ("巳", "酉"): "金",  # 巳酉半合金
        ("酉", "丑"): "金"   # 酉丑半合金
    }

    # 拱合关系
    branch_arch_combine = {
        ("申", "辰"): "水",  # 申辰拱水
        ("亥", "未"): "木",  # 亥未拱木
        ("寅", "戌"): "火",  # 寅戌拱火
        ("巳", "丑"): "金"   # 巳丑拱金
    }

    @staticmethod
    def get_three_combine_element(branch1, branch2, branch3):
        """
        获取三个地支三合后的五行
        :param branch1: 第一个地支
        :param branch2: 第二个地支
        :param branch3: 第三个地支
        :return: 三合后的五行 (如果存在三合关系)
        """
        # 将三个地支排序，确保顺序一致
        branches = sorted([branch1, branch2, branch3])
        return relation.branch_three_combine_elements.get(tuple(branches), None)

    @staticmethod
    def get_half_combine_element(branch1, branch2):
        """
        获取两个地支半三合后的五行
        :param branch1: 第一个地支
        :param branch2: 第二个地支
        :return: 半三合后的五行 (如果存在半三合关系)
        """
        pair = (branch1, branch2) if (branch1, branch2) in relation.branch_half_combine else (branch2, branch1)
        return relation.branch_half_combine.get(pair, None)

    @staticmethod
    def get_arch_combine_element(branch1, branch2):
        """
        获取两个地支拱合后的五行
        :param branch1: 第一个地支
        :param branch2: 第二个地支
        :return: 拱合后的五行 (如果存在拱合关系)
        """
        pair = (branch1, branch2) if (branch1, branch2) in relation.branch_arch_combine else (branch2, branch1)
        return relation.branch_arch_combine.get(pair, None)

    # 地支相合后的五行 地支六合. 子丑合土. 寅亥合木. 卯戌合火. 辰酉合金. 巳申合水. 午未合火.
    branch_relations_elements = {
        ("子", "丑"): "土",  # 子丑合化土
        ("寅", "亥"): "木",  # 寅亥合化木
        ("卯", "戌"): "火",  # 卯戌合化火
        ("辰", "酉"): "金",  # 辰酉合化金
        ("巳", "申"): "水",  # 巳申合化水
        ("午", "未"): "火",  # 午未合化火

    }

    @staticmethod
    def get_branch_combined_element(branch1, branch2):
        """
        获取两个地支相合后的五行
        :param branch1: 第一个地支
        :param branch2: 第二个地支
        :return: 相合后的五行 (如果存在相合关系)
        """
        pair = (branch1, branch2) if (branch1, branch2) in relation.branch_relations_elements else (branch2, branch1)
        return relation.branch_relations_elements.get(pair, None)

    # 文昌贵人查找表
    wen_chang_table = {
        "甲": "巳",  # 甲日文昌在巳
        "乙": "午",  # 乙日文昌在午
        "丙": "申",  # 丙日文昌在申
        "丁": "酉",  # 丁日文昌在酉
        "戊": "申",  # 戊日文昌在申
        "己": "酉",  # 己日文昌在酉
        "庚": "亥",  # 庚日文昌在亥
        "辛": "子",  # 辛日文昌在子
        "壬": "寅",  # 壬日文昌在寅
        "癸": "卯"   # 癸日文昌在卯
    }

    @staticmethod
    def get_wen_chang(day_stem):
        """
        获取文昌贵人所在的地支
        :param day_stem: 日干
        :return: 文昌贵人所在的地支
        """
        return relation.wen_chang_table.get(day_stem, None)

