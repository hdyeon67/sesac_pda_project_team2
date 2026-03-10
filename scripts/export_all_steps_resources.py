import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
NB_PATH = ROOT / '01_eda.ipynb'
OUT_ROOT = ROOT / 'resources' / 'all_steps'


def ensure_font():
    font_candidates = ['NanumGothic', 'Malgun Gothic', 'AppleGothic']
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for font_name in font_candidates:
        if font_name in installed:
            plt.rcParams['font.family'] = font_name
            break
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_theme(
        style='whitegrid',
        font_scale=0.95,
        rc={'font.family': plt.rcParams['font.family'], 'axes.unicode_minus': False},
    )


def run_notebook_cells():
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    ctx = {}

    def display(*args, **kwargs):
        return None

    ctx['display'] = display

    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if not src.strip():
            continue
        exec(compile(src, f'cell_{i}', 'exec'), ctx, ctx)

    return ctx


def make_dirs(step_num):
    base = OUT_ROOT / f'step{step_num:02d}'
    tdir = base / 'tables'
    fdir = base / 'figures'
    tdir.mkdir(parents=True, exist_ok=True)
    fdir.mkdir(parents=True, exist_ok=True)
    return tdir, fdir


def save_step1(ctx):
    df = ctx['step1_df'].copy()
    growth_df = ctx['growth_df'].copy()
    tdir, fdir = make_dirs(1)
    df.to_csv(tdir / 'step1_channel_signups.csv', index=False, encoding='utf-8-sig')
    growth_df.to_csv(tdir / 'step1_growth_mau_revenue.csv', index=False, encoding='utf-8-sig')

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(df['acquisition_source'], df['signups'], color='#4e79a7')
    for b, pct in zip(bars, df['share_pct']):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    ax.set_title('Step 1. 채널별 신규 가입자 수')
    ax.set_xlabel('채널')
    ax.set_ylabel('가입자 수')
    ax.tick_params(axis='x', rotation=20)
    plt.tight_layout()
    fig.savefig(fdir / 'step1_channel_signups.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(10.5, 5.2))
    ax1.plot(growth_df['month'], growth_df['MAU'], color='#2a9d8f', marker='o', linewidth=2.2, label='MAU')
    ax1.set_ylabel('MAU', color='#2a9d8f')
    ax1.tick_params(axis='y', labelcolor='#2a9d8f')
    ax2 = ax1.twinx()
    ax2.plot(growth_df['month'], growth_df['total_revenue'], color='#e76f51', marker='s', linewidth=2.2, label='총매출')
    ax2.set_ylabel('총매출', color='#e76f51')
    ax2.tick_params(axis='y', labelcolor='#e76f51')
    ax1.set_title('Step 1B. 3개월 스냅샷 성장 추이 (MAU / 총매출)')
    ax1.set_xlabel('월')
    ax1.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    fig.savefig(fdir / 'step1_growth_mau_revenue.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step2(ctx):
    df = ctx['step2_df'].copy()
    tdir, fdir = make_dirs(2)
    df.to_csv(tdir / 'step2_paid_conversion_by_channel.csv', index=False, encoding='utf-8-sig')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(df['acquisition_source'][::-1], df['paid_conversion_pct'][::-1], color='#59a14f')
    ax.set_title('Step 2. 채널별 유료전환율')
    ax.set_xlabel('유료전환율(%)')
    plt.tight_layout()
    fig.savefig(fdir / 'step2_paid_conversion_by_channel.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step3(ctx):
    df = ctx['step3_df'].copy()
    tdir, fdir = make_dirs(3)
    df.to_csv(tdir / 'step3_revenue_vs_conversion.csv', index=False, encoding='utf-8-sig')

    labels = df['acquisition_source']
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.bar(x, df['revenue'], color='#4e79a7', alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20)
    ax.set_title('Step 3-1. 채널별 매출액')
    ax.set_ylabel('매출액')
    ax.ticklabel_format(style='plain', axis='y')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y):,}'))
    max_rev = df['revenue'].max()
    rev_offset = max_rev * 0.02 if max_rev > 0 else 1
    for b in bars:
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height() + rev_offset,
            f'{b.get_height():,.0f}',
            ha='center',
            va='bottom',
            fontsize=8,
        )
    plt.tight_layout()
    fig.savefig(fdir / 'step3_1_revenue_bar.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.plot(x, df['paid_conversion_pct'], color='#e15759', marker='o', linewidth=2.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20)
    ax.set_title('Step 3-2. 채널별 유료전환율')
    ax.set_ylabel('유료전환율(%)')
    for xi, yi in zip(x, df['paid_conversion_pct']):
        ax.text(xi, yi + 0.5, f'{yi:.1f}%', ha='center', va='bottom', fontsize=9)
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    fig.savefig(fdir / 'step3_2_paid_conversion_line.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    bars = ax1.bar(
        x,
        df['revenue'],
        color='#4e79a7',
        alpha=1.0,          # Step 3-1처럼 꽉 찬 막대
        edgecolor='#4e79a7',
        linewidth=0.0,
        label='매출액',
        zorder=2,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=20)
    ax1.set_ylabel('매출액', color='#4e79a7')
    ax1.tick_params(axis='y', labelcolor='#4e79a7')
    ax1.ticklabel_format(style='plain', axis='y')
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y):,}'))
    ax1.grid(axis='y', alpha=0.25)
    max_rev = df['revenue'].max()
    rev_offset = max_rev * 0.03 if max_rev > 0 else 1
    ax1.set_ylim(0, max_rev * 1.16 if max_rev > 0 else 1)
    for b in bars:
        ax1.text(
            b.get_x() + b.get_width() / 2,
            b.get_height() + rev_offset,
            f'{b.get_height():,.0f}',
            ha='center',
            va='bottom',
            fontsize=8,
            color='#2f4b6e',
        )
    ax2 = ax1.twinx()
    ax2.plot(x, df['paid_conversion_pct'], color='#e15759', marker='o', linewidth=2.5, label='유료전환율(%)')
    ax2.set_ylabel('유료전환율(%)', color='#e15759')
    ax2.tick_params(axis='y', labelcolor='#e15759')
    for xi, yi in zip(x, df['paid_conversion_pct']):
        ax2.text(xi, yi + 0.5, f'{yi:.1f}%', ha='center', va='bottom', fontsize=9, color='#e15759')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc='upper right')
    ax1.set_title('Step 3-3. 채널별 매출액 vs 유료전환율 (통합)')
    plt.tight_layout()
    fig.savefig(fdir / 'step3_3_revenue_vs_conversion_combined.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step4(ctx):
    df = ctx['step4_df'].copy()
    tdir, fdir = make_dirs(4)
    df.to_csv(tdir / 'step4_retention_by_channel.csv', index=False, encoding='utf-8-sig')

    x = np.arange(len(df))
    w = 0.35
    fig, ax = plt.subplots(figsize=(11, 5))
    bars1 = ax.bar(x - w / 2, df['d7_retention_pct'], width=w, label='D7')
    bars2 = ax.bar(x + w / 2, df['d30_retention_pct'], width=w, label='D30')
    for b in bars1:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h, f'{h:.1f}%', ha='center', va='bottom', fontsize=8)
    for b in bars2:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h, f'{h:.1f}%', ha='center', va='bottom', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(df['acquisition_source'], rotation=20)
    ax.set_ylabel('리텐션(%)')
    ax.set_title('Step 4. 채널별 D7/D30 리텐션')
    ax.legend()
    plt.tight_layout()
    fig.savefig(fdir / 'step4_d7_d30_retention.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step5(ctx):
    roi_df = ctx['roi_df'].copy()
    roi_grade = ctx['roi_grade'].copy()
    tdir, fdir = make_dirs(5)

    roi_df.to_csv(tdir / 'step5_modelA_scores.csv', index=False, encoding='utf-8-sig')
    roi_grade.to_csv(tdir / 'step5_modelA_grades.csv', index=False, encoding='utf-8-sig')

    fig, ax = plt.subplots(figsize=(10.5, 5))
    colors = ['#e15759' if i < 2 else '#9aa0a6' for i in range(len(roi_df))]
    bars = ax.bar(roi_df['acquisition_source'], roi_df['final_score_roi'], color=colors)
    for i, b in enumerate(bars):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=9)
        if i < 2:
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height() + 1.8,
                f'TOP {i+1}',
                ha='center',
                va='bottom',
                fontsize=9,
                color='#e15759',
                fontweight='bold',
            )
    ax.set_title('Step 5. 모델 A 최종 종합 스코어 (ROI 포함)')
    ax.set_ylabel('점수')
    ax.tick_params(axis='x', rotation=20)
    plt.tight_layout()
    fig.savefig(fdir / 'step5_modelA_score_bar.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step6(ctx):
    pivot6 = ctx['pivot6'].copy()
    tdir, fdir = make_dirs(6)
    pivot6.to_csv(tdir / 'step6_age_channel_cvr_pivot.csv', encoding='utf-8-sig')
    pivot6.stack().reset_index(name='paid_conversion_pct').to_csv(
        tdir / 'step6_age_channel_cvr_long.csv', index=False, encoding='utf-8-sig'
    )

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.heatmap(
        pivot6,
        annot=True,
        fmt='.1f',
        cmap='YlGn',
        linewidths=0.5,
        linecolor='white',
        cbar_kws={'label': '전환율(%)'},
        ax=ax,
    )
    ax.set_title('Step 6. 연령대 × 채널 전환율 히트맵')
    ax.set_xlabel('채널', fontsize=11, labelpad=8)
    ax.set_ylabel('연령대', fontsize=11, labelpad=8)
    ax.tick_params(axis='x', rotation=30, labelsize=10)
    ax.tick_params(axis='y', rotation=0, labelsize=10)
    plt.tight_layout()
    fig.savefig(fdir / 'step6_age_channel_heatmap.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step7(ctx):
    pivot7 = ctx['pivot7'].copy()
    tdir, fdir = make_dirs(7)
    pivot7.to_csv(tdir / 'step7_device_channel_cvr_pivot.csv', encoding='utf-8-sig')
    pivot7.stack().reset_index(name='paid_conversion_pct').to_csv(
        tdir / 'step7_device_channel_cvr_long.csv', index=False, encoding='utf-8-sig'
    )

    channels = pivot7.columns.tolist()
    devices = pivot7.index.tolist()
    x = np.arange(len(channels))
    w = 0.8 / max(1, len(devices))

    fig, ax = plt.subplots(figsize=(12, 5))
    for i, dev in enumerate(devices):
        ax.bar(x + (i - (len(devices) - 1) / 2) * w, pivot7.loc[dev].values, width=w, label=dev)
    ax.set_xticks(x)
    ax.set_xticklabels(channels, rotation=20)
    ax.set_ylabel('전환율(%)')
    ax.set_title('Step 7. 디바이스 × 채널 전환율')
    ax.legend(title='디바이스')
    plt.tight_layout()
    fig.savefig(fdir / 'step7_device_channel_grouped_bar.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step8(ctx):
    seg = ctx['seg'].copy()
    seg_all_view = ctx['seg_all_view'].copy()
    top3_channels = list(ctx['top3_channels'])
    tdir, fdir = make_dirs(8)

    (tdir / 'step8_top3_channels.txt').write_text('\n'.join(top3_channels) + '\n', encoding='utf-8')

    for ch in top3_channels:
        out = (
            seg[seg['acquisition_source'] == ch][['age_group', 'device_type', 'signups', 'conversion_pct', 'ARPU', 'score_8']]
            .sort_values('score_8', ascending=False)
            .head(5)
            .reset_index(drop=True)
        )
        out.insert(0, 'rank', out.index + 1)
        out.to_csv(tdir / f'step8_2_top5_{ch}.csv', index=False, encoding='utf-8-sig')

    seg_all_view.to_csv(tdir / 'step8_3_integrated_top5_by_channel.csv', index=False, encoding='utf-8-sig')

    best_by_channel = (
        seg.sort_values('score_8', ascending=False)
        .groupby('acquisition_source', as_index=False)
        .head(1)
        .sort_values('score_8', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    palette = ['#2a9d8f', '#66bb6a', '#90caf9']
    bars = ax.bar(best_by_channel['acquisition_source'], best_by_channel['score_8'], color=palette[: len(best_by_channel)], width=0.58)
    for b, (_, r) in zip(bars, best_by_channel.iterrows()):
        ax.text(
            b.get_x() + b.get_width() / 2,
            b.get_height() + 0.7,
            f"{b.get_height():.1f}\n{r['age_group']} | {r['device_type']}",
            ha='center',
            va='bottom',
            fontsize=8,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='#d1d5db', alpha=0.9),
        )
    ax.set_title('Step 8-4A. 채널별 최고 코호트 통합점수', fontsize=12, pad=12)
    ax.set_ylabel('코호트 통합점수')
    ax.set_xlabel('채널')
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    fig.savefig(fdir / 'step8_4a_best_cohort_score_by_channel.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    viz = seg_all_view.head(10).copy()
    viz['label'] = viz['acquisition_source'] + ' | ' + viz['age_group'] + ' | ' + viz['device_type']
    viz = viz.sort_values('score_8', ascending=True)

    fig, ax = plt.subplots(figsize=(12.2, 6.2))
    bar_colors = sns.color_palette('YlGn', n_colors=len(viz))
    ax.barh(viz['label'], viz['score_8'], color=bar_colors)
    for y, s in zip(viz['label'], viz['score_8']):
        ax.text(s + 0.5, y, f'{s:.1f}', va='center', fontsize=8)
    ax.set_title('Step 8-4B. 통합 코호트 점수 TOP10', fontsize=12, pad=10)
    ax.set_xlabel('통합점수')
    ax.set_ylabel('코호트(채널 | 연령대 | 디바이스)')
    ax.grid(axis='x', alpha=0.25)
    plt.tight_layout()
    fig.savefig(fdir / 'step8_4b_integrated_top10_cohort_score.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def save_step9(ctx):
    final = ctx['final'].copy()
    tdir, fdir = make_dirs(9)

    summary = final[
        ['priority', 'acquisition_source', 'priority_score', 'recommended_budget_pct', 'best_cohort', 'best_cvr', 'best_arpu', 'avg_score']
    ].copy()
    summary.to_csv(tdir / 'step9_1_final_summary.csv', index=False, encoding='utf-8-sig')

    rec_lines = ['=== Step 9-3 최종 권고 ===']
    for _, r in final.iterrows():
        rec_lines.append(
            f"- {r['priority']} {r['acquisition_source']}: 권장 예산 {r['recommended_budget_pct']:.1f}%, 대표 코호트={r['best_cohort']}"
        )
    (tdir / 'step9_3_recommendations.txt').write_text('\n'.join(rec_lines) + '\n', encoding='utf-8')

    action_lines = ['=== Step 9-4 채널별 액션 추천 (목적/기대 시나리오 포함) ===']
    action_lines.append('[용어 간단 설명]')
    action_lines.append('- CVR: 유입 대비 유료전환 비율')
    action_lines.append('- ARPU: 사용자 1인당 평균 매출')
    action_lines.append('- 리타겟팅: 이탈 가능성이 높은 유저를 다시 타겟해 재노출하는 방식')
    action_lines.append('- 네거티브 키워드: 비효율 검색어 노출을 차단해 광고비 낭비를 줄이는 키워드')
    action_lines.append('- A/B 테스트: 두 가지 버전을 병행 실험해 성과가 높은 안을 선택하는 방식')
    for _, r in final.iterrows():
        ch = r['acquisition_source']
        cohort = r['best_cohort']
        budget = r['recommended_budget_pct']
        action_lines.append(f"\n[{r['priority']}] {ch} | 권장 예산 {budget:.1f}% | 대표 코호트 {cohort}")
        if ch == 'referral':
            action_lines.append('1) 액션: 결제 확정 기반 더블 리워드')
            action_lines.append('   목적: 가입 수가 아니라 유료전환 수를 늘려 저리스크로 매출 효율을 높인다.')
            action_lines.append('   기대 시나리오: 추천 가입 후 결제 완료 시점에만 보상이 지급되어, 비용 대비 순매출이 안정적으로 증가한다.')
            action_lines.append('2) 액션: 추천 진입 퍼널 단축(링크→가입→결제) + A/B 테스트')
            action_lines.append('   목적: 추천 유입의 이탈 구간을 줄여 전환 속도를 높인다.')
            action_lines.append('   기대 시나리오: 추천 코드 입력/랜딩/결제 단계 마찰이 줄어 동일 트래픽 대비 CVR이 개선된다.')
            action_lines.append('3) 액션: 상위 추천인 그룹 인센티브 분리 운영')
            action_lines.append('   목적: 실제 매출 기여가 큰 추천인 집단에 예산을 집중한다.')
            action_lines.append('   기대 시나리오: 고성과 추천인 활동량이 증가해 예측 가능한 반복 유입 구조가 강화된다.')
        elif ch == 'youtube':
            action_lines.append('1) 액션: 체험 기간 내 조기 결제 프로모션')
            action_lines.append('   목적: 7일 체험 후 이탈하는 유저를 조기에 유료로 전환한다.')
            action_lines.append('   기대 시나리오: 체험 종료 전 결제 확정 비율이 올라가며, Q3(체험 이탈) 구간이 축소된다.')
            action_lines.append('2) 액션: 대표 코호트 맞춤 크리에이티브(메시지/썸네일/CTA) 확장')
            action_lines.append('   목적: 관심은 있지만 결제 직전에서 머무는 유저의 구매 의사를 자극한다.')
            action_lines.append('   기대 시나리오: 코호트 적합도가 높은 소재에서 CTR과 랜딩 전환율이 동시에 개선된다.')
            action_lines.append('3) 액션: 시청구간 기반 리타겟팅(완시청/중도이탈 분리)')
            action_lines.append('   목적: 의도 수준이 다른 유저를 분리 공략해 전환 효율을 높인다.')
            action_lines.append('   기대 시나리오: 완시청군은 결제 오퍼, 중도이탈군은 신뢰형 메시지로 재유입되어 전체 전환이 상승한다.')
        elif ch == 'google_ads':
            action_lines.append('1) 액션: Pro 의도형 키워드 묶음 분리 + 전용 랜딩')
            action_lines.append('   목적: 결제 가능성이 높은 검색 유입에만 예산을 집중한다.')
            action_lines.append('   기대 시나리오: 유입량은 다소 줄어도 고의도 트래픽 비중이 올라 CPA 대비 매출 효율이 개선된다.')
            action_lines.append('2) 액션: 검색어 리포트 기반 네거티브 키워드 확장')
            action_lines.append('   목적: 비의도/저품질 클릭을 차단해 불필요한 광고비를 줄인다.')
            action_lines.append('   기대 시나리오: 무효 트래픽이 감소하면서 동일 예산에서 유효 전환 수가 늘어난다.')
            action_lines.append('3) 액션: 디바이스·시간대 입찰 가중치 조정(웹 중심)')
            action_lines.append('   목적: 전환율이 높은 구간에 노출을 집중해 단기 효율을 높인다.')
            action_lines.append('   기대 시나리오: 저성과 시간/디바이스 노출이 줄고, 상위 코호트 중심으로 전환 밀도가 높아진다.')
        else:
            action_lines.append('1) 액션: 대표 코호트 전용 캠페인 분리 운영')
            action_lines.append('   목적: 성과가 높은 세그먼트 중심으로 예산을 재배치한다.')
            action_lines.append('   기대 시나리오: 평균 성과 하락 없이 상위 코호트의 기여도가 확대된다.')
    (tdir / 'step9_4_channel_actions.txt').write_text('\n'.join(action_lines) + '\n', encoding='utf-8')

    fig, ax1 = plt.subplots(figsize=(10.5, 5.2))
    x = np.arange(len(final))
    bars = ax1.bar(x, final['priority_score'], color=['#2a9d8f', '#66bb6a', '#90caf9'][: len(final)], width=0.58)
    ax1.set_xticks(x)
    ax1.set_xticklabels(final['acquisition_source'])
    ax1.set_ylabel('최종우선점수')
    ax1.set_title('Step 9-2. Step 8 기반 최종 채널 우선순위')
    for b in bars:
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height(), f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=9)

    ax2 = ax1.twinx()
    ax2.plot(x, final['recommended_budget_pct'], color='#e76f51', marker='o', linewidth=2.2)
    ax2.set_ylabel('권장예산비중(%)')
    for xi, yi in zip(x, final['recommended_budget_pct']):
        ax2.text(xi, yi + 0.7, f'{yi:.1f}%', ha='center', va='bottom', fontsize=8, color='#e76f51')

    plt.tight_layout()
    fig.savefig(fdir / 'step9_2_final_priority_budget.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    # Step 9-5: 현재 예산 100% 기준 전체 채널 재배분안(제약조건 반영)
    budget_df = ctx['roi_df'][['acquisition_source', 'final_score_roi']].copy()
    budget_df = budget_df.rename(columns={'acquisition_source': '채널', 'final_score_roi': 'score'})
    budget_df = budget_df.sort_values('score', ascending=False).reset_index(drop=True)

    # 집행 우선순위 고정: 1순위 google_ads, 2순위 youtube
    boost = {ch: 1.0 for ch in budget_df['채널']}
    preferred_boost = {
        'google_ads': 1.40,
        'youtube': 1.25,
    }
    for ch, v in preferred_boost.items():
        if ch in boost:
            boost[ch] = v

    budget_df['focus_boost'] = budget_df['채널'].map(boost)
    budget_df['budget_score'] = budget_df['score'] * budget_df['focus_boost']

    # 고정 제약(요청 시나리오):
    # - organic: 0%
    # - content_marketing: 2%
    # - referral: 12%
    # - instagram_influencer: 8%
    # - meta_ads: 10%
    # 나머지(68%)는 google_ads / youtube에만 배분
    fixed_alloc = {
        'organic': 0.0,
        'content_marketing': 2.0,
        'referral': 12.0,
        'instagram_influencer': 8.0,
        'meta_ads': 10.0,
    }
    remain_pct = 100.0 - sum(fixed_alloc.values())

    budget_df['budget_pct'] = 0.0
    mask_fixed = budget_df['채널'].isin(fixed_alloc.keys())
    mask_variable = ~mask_fixed
    mask_variable = mask_variable & budget_df['채널'].isin(['google_ads', 'youtube'])

    variable_score_sum = budget_df.loc[mask_variable, 'budget_score'].sum()
    if variable_score_sum > 0:
        budget_df.loc[mask_variable, 'budget_pct'] = (
            budget_df.loc[mask_variable, 'budget_score'] / variable_score_sum * remain_pct
        )

    for ch, pct in fixed_alloc.items():
        idx = budget_df.index[budget_df['채널'] == ch]
        if len(idx) > 0:
            budget_df.loc[idx[0], 'budget_pct'] = pct

    budget_df['budget_pct'] = budget_df['budget_pct'].round(1)
    diff = round(100.0 - budget_df['budget_pct'].sum(), 1)
    for i in budget_df.index:
        if budget_df.loc[i, '채널'] not in fixed_alloc:
            budget_df.loc[i, 'budget_pct'] = round(budget_df.loc[i, 'budget_pct'] + diff, 1)
            break

    budget_plan = budget_df[['채널', 'score', 'focus_boost', 'budget_pct']].copy()
    budget_plan = budget_plan.sort_values('budget_pct', ascending=False).reset_index(drop=True)
    budget_plan['tier'] = '테스트'
    budget_plan.loc[budget_plan.index < 3, 'tier'] = '집중'
    budget_plan.loc[(budget_plan.index >= 3) & (budget_plan.index < 5), 'tier'] = '유지'
    budget_plan.loc[budget_plan['채널'] == 'organic', 'tier'] = '제외(0%)'
    budget_plan.loc[budget_plan['채널'] == 'content_marketing', 'tier'] = '유지(소액)'
    budget_plan.to_csv(tdir / 'step9_5_budget_plan_100pct.csv', index=False, encoding='utf-8-sig')

    # Step 9-6: 단일 재배분안 시각화
    plot_df = budget_plan.sort_values('budget_pct', ascending=False).copy()
    colors = ['#2a9d8f' if i < 3 else '#a8dadc' for i in range(len(plot_df))]
    fig, ax = plt.subplots(figsize=(12, 5.5))
    bars = ax.bar(plot_df['채널'], plot_df['budget_pct'], color=colors)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'{b.get_height():.1f}%', ha='center', va='bottom', fontsize=8)
    ax.set_ylabel('예산 비율(%)')
    ax.set_title('Step 9-6. 현재 예산 100% 기준 채널별 재배분안')
    ax.set_xlabel('채널')
    ax.tick_params(axis='x', rotation=20)
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    fig.savefig(fdir / 'step9_6_budget_plan_100pct.png', dpi=180, bbox_inches='tight')
    plt.close(fig)


def write_index():
    lines = ['# All Step Resources', '']
    for step_dir in sorted(OUT_ROOT.glob('step*')):
        if not step_dir.is_dir():
            continue
        lines.append(f'## {step_dir.name}')
        for sub in ['tables', 'figures']:
            target = step_dir / sub
            lines.append(f'- {sub}')
            if target.exists():
                for fp in sorted(target.glob('*')):
                    lines.append(f'  - {fp.relative_to(ROOT)}')
        lines.append('')
    (OUT_ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    ensure_font()
    ctx = run_notebook_cells()

    save_step1(ctx)
    save_step2(ctx)
    save_step3(ctx)
    save_step4(ctx)
    save_step5(ctx)
    save_step6(ctx)
    save_step7(ctx)
    save_step8(ctx)
    save_step9(ctx)
    write_index()

    print('Export complete:', OUT_ROOT)


if __name__ == '__main__':
    main()
