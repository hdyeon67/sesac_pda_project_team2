import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager


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
    tdir, fdir = make_dirs(1)
    df.to_csv(tdir / 'step1_channel_signups.csv', index=False, encoding='utf-8-sig')

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
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f'{b.get_height():,.0f}', ha='center', va='bottom', fontsize=8)
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
    ax1.bar(x, df['revenue'], color='#4e79a7', alpha=0.75, label='매출액')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=20)
    ax1.set_ylabel('매출액', color='#4e79a7')
    ax1.tick_params(axis='y', labelcolor='#4e79a7')
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

    action_lines = ['=== Step 9-4 채널별 액션 추천 (각 3개) ===']
    for _, r in final.iterrows():
        ch = r['acquisition_source']
        cohort = r['best_cohort']
        action_lines.append(f'\n[{ch}] 액션 후보')
        if ch == 'referral':
            action_lines.append(f'1. {cohort} 코호트 중심 추천 리워드 상향(A/B): 추천인·피추천인 보상 구조 최적화')
            action_lines.append('2. 추천 링크/코드 진입 퍼널 단축: 가입-첫결제까지 단계 축소 및 이탈 구간 개선')
            action_lines.append('3. 고가치 추천인 군 분리 운영: 상위 추천인 대상 시즌성 인센티브 캠페인 운영')
        elif ch == 'youtube':
            action_lines.append(f'1. {cohort} 페르소나 전용 크리에이티브 확장: 메시지/썸네일/CTA 버전 분리')
            action_lines.append('2. 영상 소재-랜딩 일치도 개선: 콘텐츠 주제와 랜딩 오퍼를 1:1 매핑')
            action_lines.append('3. 시청 구간 리타겟팅 운영: 조회완료/중도이탈 세그먼트별 재집행')
        elif ch == 'google_ads':
            action_lines.append(f'1. {cohort} 전환 키워드 묶음 분리: 고의도 키워드 중심 입찰 전략 재구성')
            action_lines.append('2. 검색어 리포트 기반 네거티브 키워드 확장: 비효율 트래픽 유입 차단')
            action_lines.append('3. 디바이스/시간대 입찰 조정: 웹 중심 고효율 구간에 예산 집중')
        else:
            action_lines.append(f'1. {cohort} 코호트 전용 캠페인 분리 운영')
            action_lines.append('2. 상위 코호트 유사 오디언스 확장 테스트')
            action_lines.append('3. 채널 내 TOP5 코호트 순환 운영으로 성과 방어')
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
