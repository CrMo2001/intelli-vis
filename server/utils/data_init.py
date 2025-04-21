import os
import pandas as pd

# 预定义数据路径和相关信息
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/湖北_外部能耗数据.xlsx")
print(DATA_PATH)
# 预加载数据描述
DATA_DESCRIPTION = """
湖北_外部能耗数据表，其中有4个sheet，分别是：
1. hubei_in_y_pro_ind_ene_off：具体内容如下
能源平衡表：类似于企业的资产负债表，记录一年内该地区各品种能源生产供应-加工转换-终端消费的完整链条；
来自《中国能源统计年鉴》地区能源平衡表（湖北，实物量）历年数据。
2. hubei_in_y_pro_ind_ene2_off：具体内容如下
分行业能源消费表：记录湖北省规模以上工业企业（年营收≥2000万元）各行业的能源消费详情，
该表与表1的区别在于：①专注工业部门 ②按国民经济行业分类详细划分 ③数据来源于企业直报系统；
来自《湖北统计年鉴》能源篇-规模以上工业分行业能源消费量（实物量）历年数据
3. hubei_in_y_pro_ind_prd_off：具体内容如下
重点碳排放工业产品监测表：记录湖北省高能耗、高排放（"双高"）产品的产量数据，如钢铁、水泥、电解铝等；
记录来自《湖北统计年鉴》中双碳及能耗相关工业品产量历年数据
4. hubei_in_y_pro_gdp_off：具体内容如下
经济能源关联表：记录湖北省地区生产总值及分行业增加值数据。此表与能源消耗数据结合，可计算单位GDP能耗强度、行业能效水平等关键指标；
记录来自《湖北统计年鉴》中地区生产总值以及分行业增加值的长表
"""

def load_data_sample():
    """生成数据样本，供DSPy模型分析使用"""
    sample_template = """
sheet:hubei_in_y_pro_ind_ene_off
{sample1}

sheet:hubei_in_y_pro_ind_ene2_off
{sample2}

sheet:hubei_in_y_pro_ind_prd_off
{sample3}

sheet:hubei_in_y_pro_gdp_off
{sample4}
"""
    
    sample1 = pd.read_excel(DATA_PATH, sheet_name="hubei_in_y_pro_ind_ene_off").head(5).to_csv(index=False)
    sample2 = pd.read_excel(DATA_PATH, sheet_name="hubei_in_y_pro_ind_ene2_off").head(5).to_csv(index=False)
    sample3 = pd.read_excel(DATA_PATH, sheet_name="hubei_in_y_pro_ind_prd_off").head(5).to_csv(index=False)
    sample4 = pd.read_excel(DATA_PATH, sheet_name="hubei_in_y_pro_gdp_off").head(5).to_csv(index=False)
    
    return sample_template.format(sample1=sample1, sample2=sample2, sample3=sample3, sample4=sample4)
