"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a 人物, a 世帯…

See https://openfisca.org/doc/key-concepts/variables.html
"""

from datetime import date

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import where
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import DAY, ETERNITY, MONTH
from openfisca_core.variables import Variable
# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import 人物


# This variable is a pure input: it doesn't have a formula
class 誕生年月日(Variable):
    value_type = date
    default_value = date(1970, 1, 1)  # By default, if no value is set for a simulation, we consider the people involved in a simulation to be born on the 1st of Jan 1970.
    entity = 人物
    label = "人物の誕生年月日"
    definition_period = ETERNITY  # This variable cannot change over time.
    reference = "https://en.wiktionary.org/wiki/birthdate"


class 死亡年月日(Variable):
    value_type = date
    entity = 人物
    label = "人物の死亡年月日"
    definition_period = ETERNITY  # This variable cannot change over time.


class 年齢(Variable):
    value_type = int
    entity = 人物
    definition_period = MONTH
    label = "人物の年齢"

    def formula(対象人物, 対象期間, _parameters):
        誕生年月日 = 対象人物("誕生年月日", 対象期間)
        誕生年 = 誕生年月日.astype("datetime64[Y]").astype(int) + 1970
        誕生月 = 誕生年月日.astype("datetime64[M]").astype(int) % 12 + 1
        誕生日 = (誕生年月日 - 誕生年月日.astype("datetime64[M]") + 1).astype(int)

        誕生日を過ぎている = (誕生月 < 対象期間.start.month) + (誕生月 == 対象期間.start.month) * (誕生日 <= 対象期間.start.day)

        return (対象期間.start.year - 誕生年) - where(誕生日を過ぎている, 0, 1)  # If the birthday is not passed this year, subtract one year


class 学年(Variable):
    value_type = int
    entity = 人物
    definition_period = DAY
    label = "人物の学年"

    def formula(対象人物, 対象期間, _parameters):
        誕生年月日 = 対象人物("誕生年月日", 対象期間)
        誕生年 = 誕生年月日.astype("datetime64[Y]").astype(int) + 1970
        誕生月 = 誕生年月日.astype("datetime64[M]").astype(int) % 12 + 1
        # 誕生日 = (誕生年月日 - 誕生年月日.astype("datetime64[M]") + 1).astype(int)

        対象期間において早生まれ = (誕生月 < 4) * (4 <= 対象期間.start.month)
        早生まれではないが四月以降 = (4 < 誕生月) * (4 <= 対象期間.start.month)
        学年を繰り上げるべき = 対象期間において早生まれ + 早生まれではないが四月以降

        return (対象期間.start.year - 誕生年) + where(学年を繰り上げるべき, 1, 0)


class 行方不明年月日(Variable):
    value_type = bool
    entity = 人物
    definition_period = DAY
    label = "行方不明になった年月日"


class 生存状況パターン(Enum):
    __order__ = "生存 死亡 不明"
    生存 = "生存"
    死亡 = "死亡"
    不明 = "不明"


class 生存状況(Variable):
    value_type = Enum
    possible_values = 生存状況パターン
    default_value = 生存状況パターン.生存
    entity = 人物
    definition_period = DAY
    label = "生存状況"

class 労災障害等級パターン(Enum):
    __order__ = "第1級 第2級 第3級重度 第3級 第4級 第5級 第6級 第7級 第8級 第9級 第10級 第11級 第12級 第13級 第14級 障害なし"
    第1級 = "第1級"
    第2級 = "第2級"
    第3級重度 = "第3級重度"
    第3級 = "第3級"
    第4級 = "第4級"
    第5級 = "第5級"
    第6級 = "第6級"
    第7級 = "第7級"
    第8級 = "第8級"
    第9級 = "第9級"
    第10級 = "第10級"
    第11級 = "第11級"
    第12級 = "第12級"
    第13級 = "第13級"
    第14級 = "第14級"
    障害なし = "障害なし"

class 労災障害等級(Variable):
    value_type = Enum 
    possible_values = 労災障害等級パターン
    default_value = 労災障害等級パターン.障害なし
    entity = 人物
    definition_period = DAY
    label = "障害等級"

class 労災補償重度障害者該当(Variable):
    value_type = bool
    entity = 人物
    definition_period = DAY
    label = "重度障害者に該当しているか否か"

    def formula(対象人物, 対象期間, _parameters):
        
        障害等級状態 = 対象人物("障害等級", 対象期間)

        return (障害等級状態 == 労災障害等級パターン.第1級) + (障害等級状態 == 労災障害等級パターン.第2級) + (障害等級状態 == 労災障害等級パターン.第3級重度) 