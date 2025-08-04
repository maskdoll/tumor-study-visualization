import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

# 加载数据
df = pd.read_csv("patients.csv")

# 添加完整剂量标签用于图例
df['dose_label'] = 'mRNA-4157 ' + df['dose']

# 颜色和图案映射
dose_colors = {
    'mRNA-4157 0.1mg': '#1f77b4',  # 蓝色
    'mRNA-4157 0.2mg': '#ff7f0e',  # 橙色
}

endpoint_patterns = {
    'PD': r'\\\\',              # 右斜线 - 进展/复发
    'No_PD_or_Death': ''          # 空白 - 无进展或死亡
}

# 创建图表
plt.figure(figsize=(12, 8))
ax = plt.subplot()

# 按肿瘤类型和患者ID排序
df = df.sort_values(by=['tumor_type', 'patient_id'], ascending=[False, True])

# 创建自定义的y轴标签 (肿瘤类型 + 患者ID)
y_labels = [f"{row['tumor_type']} [{row['patient_id']}]" for _, row in df.iterrows()]

# 绘制水平条带
for i, (_, row) in enumerate(df.iterrows()):
    ax.barh(
        y=i,
        width=row['time'],
        color=dose_colors[row['dose_label']],
        hatch=endpoint_patterns[row['endpoint']],
        edgecolor='black',
        height=0.7
    )

# 设置坐标轴和网格
ax.set_yticks(range(len(df)))
ax.set_yticklabels(y_labels, fontsize=12)
ax.set_xlabel('Time on Study (Weeks)', fontsize=14, fontweight='bold')
ax.set_title('Patient Timeline by Tumor Type', fontsize=16, fontweight='bold')
ax.xaxis.set_major_locator(MultipleLocator(20))
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.set_xlim(0, 140)

# 创建图例
dose_legend = [
    mpatches.Patch(facecolor=color, edgecolor='black', label=dose)
    for dose, color in dose_colors.items()
]

endpoint_legend = [
    mpatches.Patch(facecolor='white', edgecolor='black', hatch=pattern, label=endpoint.replace('_', ' '))
    for endpoint, pattern in endpoint_patterns.items()
]

# 添加图例
legend_dose = ax.legend(handles=dose_legend, title='Dose', loc='upper right')
ax.add_artist(legend_dose)
ax.legend(handles=endpoint_legend, title='Endpoint', loc='lower right')

# 添加研究时间标记
plt.axvline(x=52, color='gray', linestyle=':', alpha=0.7, linewidth=1.5)
plt.text(52, len(df) + 0.1, '1 Year', ha='center', fontsize=10, backgroundcolor='white')

# 优化布局并保存
plt.tight_layout()
plt.savefig('patient_timeline.png', dpi=300, bbox_inches='tight')
plt.close()  # 关闭图形窗口

print("成功生成 patient_timeline.png 图片!")
