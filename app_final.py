import streamlit as st
import numpy as np
# import matplotlib.pyplot as plt # Matplotlib 대신 Plotly 사용
import plotly.graph_objects as go # Plotly 사용
import scipy.stats as stats

# --- Matplotlib 한글 설정 (이제 Plotly에는 필요 없음) ---
# plt.rcParams['font.family'] = 'Malgun Gothic' # 주석 처리 또는 삭제
# plt.rcParams['axes.unicode_minus'] = False # 주석 처리 또는 삭제
# ------------------------------------------------------


# --- 웹 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 통계 분석 웹 프로그램", layout="wide")

st.title("📊 도담고 학생용 통계 분석 프로그램")
st.write("두 변수(X, Y)의 관계를 분석하고, 기술 통계, 상관계수, 회귀식, 산점도를 보여줍니다.")

# --- 데이터 입력 섹션 ---
st.header("데이터 입력")

# 변수명 입력
col_var_name1, col_var_name2 = st.columns(2)
with col_var_name1:
    x_var_name = st.text_input("X 변수명 입력:", "X", key="x_var_name_input")
with col_var_name2:
    y_var_name = st.text_input("Y 변수명 입력:", "Y", key="y_var_name_input")

st.write("---") # 구분선 추가

# X, Y 값 입력 (예전처럼 통합된 텍스트 영역 사용)
col_data_input1, col_data_input2 = st.columns(2)
with col_data_input1:
    x_data_str = st.text_area(f"{x_var_name} 값 입력 (각 값은 줄바꿈):", height=150, key="x_data_text_area")
with col_data_input2:
    y_data_str = st.text_area(f"{y_var_name} 값 입력 (각 값은 줄바꿈):", height=150, key="y_data_text_area")


# --- 분석 실행 버튼 ---
analyze_button = st.button("통계 분석 실행", key="analyze_button")


# --- 분석 로직 및 결과 표시 섹션 ---
if analyze_button: # 버튼이 클릭되면 이 블록 실행
    st.header("분석 결과")

    x_data = []
    y_data = []
    errors = [] # 데이터 파싱 오류

    # X 값 파싱 (줄바꿈 기준으로 분리)
    x_lines = x_data_str.strip().splitlines()
    y_lines = y_data_str.strip().splitlines()

    # 데이터 개수 일치 기본 확인 (파싱 전에)
    if len(x_lines) != len(y_lines):
         st.error(f"오류: 입력된 {x_var_name} 값의 줄 수({len(x_lines)})와 {y_var_name} 값의 줄 수({len(y_lines)})가 다릅니다. 쌍으로 입력해주세요.")
         st.warning("데이터 개수 불일치 오류. 분석을 중단합니다.")
         st.stop() # 오류 발생 시 분석 중단

    # 각 줄을 숫자로 변환하면서 오류 확인
    for i, line in enumerate(x_lines):
        if line.strip(): # 비어있지 않은 줄만 처리
            try:
                x_data.append(float(line.strip()))
            except ValueError:
                errors.append(f"{x_var_name} 값 오류 (줄 {i+1}): '{line.strip()}'는 유효한 숫자가 아닙니다.")
        # else: # 빈 줄은 무시

    for i, line in enumerate(y_lines):
         if line.strip(): # 비어있지 않은 줄만 처리
            try:
                y_data.append(float(line.strip()))
            except ValueError:
                 errors.append(f"{y_var_name} 값 오류 (줄 {i+1}): '{line.strip()}'는 유효한 숫자가 아닙니다.")
        # else: # 빈 줄은 무시

    # --- 데이터 유효성 검사 (파싱 후 최종 확인) ---

    if errors:
        for err in errors:
            st.error(err) # 개별 입력 오류 표시
        st.warning("입력 데이터에 오류가 있습니다. 분석을 중단합니다.")
        st.stop() # 오류 발생 시 분석 중단

    # 파싱 결과의 데이터 개수 최종 확인 (빈 줄 무시 등으로 인해 발생 가능)
    if len(x_data) != len(y_data):
         st.error(f"내부 오류: 유효한 {x_var_name} 값 개수({len(x_data)})와 유효한 {y_var_name} 값 개수({len(y_data)})가 다릅니다. 쌍으로 입력해주세요.")
         st.warning("데이터 개수 불일치 오류. 분석을 중단합니다.")
         st.stop()

    # 최소 데이터 쌍 개수 확인
    if len(x_data) < 2:
         st.error(f"오류: 유효한 데이터 쌍은 최소 2개 이상이어야 합니다. 현재 {len(x_data)}개 입니다.")
         st.warning("데이터 부족 오류. 분석을 중단합니다.")
         st.stop()


    # 유효성 검사 통과 후 NumPy 배열로 변환
    x_np = np.array(x_data)
    y_np = np.array(y_data)

    st.success("데이터 입력 및 유효성 검사 통과. 분석을 진행합니다.")

    # --- 간결한 결과 출력 시작 ---

    st.write("입력된 데이터 요약:")
    st.text(f"  {x_var_name} 값 ({len(x_np)}개): {x_np}") # st.text는 고정폭 글꼴로 표시
    st.text(f"  {y_var_name} 값 ({len(y_np)}개): {y_np}")
    st.write("---") # 구분선 추가


    # 기술 통계 (평균, 중앙값, 최빈값, 표준편차 추가)
    mean_x = np.mean(x_np)
    mean_y = np.mean(y_np)

    # 중앙값 계산
    median_x = np.median(x_np)
    median_y = np.median(y_np)

    # 최빈값 계산 (데이터가 1개 이상일 때만 시도)
    mode_x_result = None
    mode_y_result = None
    if len(x_np) > 0:
        try:
            mode_x_result = stats.mode(x_np, keepdims=False)
        except Exception as e:
            st.warning(f"{x_var_name} 최빈값 계산 중 오류 발생: {e}")
            mode_x_result = None

    if len(y_np) > 0:
        try:
            mode_y_result = stats.mode(y_np, keepdims=False)
        except Exception as e:
            st.warning(f"{y_var_name} 최빈값 계산 중 오류 발생: {e}")
            mode_y_result = None


    # 표준편차 계산 (표본 표준편차: ddof=1) - 데이터가 1개 초과일 때만 계산
    std_x = np.std(x_np, ddof=1) if len(x_np) > 1 else None
    std_y = np.std(y_np, ddof=1) if len(y_np) > 1 else None


    st.subheader("기술 통계")

    # 평균 출력
    st.write(f"**{x_var_name}**의 평균 (X̄): {mean_x:.4f}")
    st.write(f"**{y_var_name}**의 평균 (ȳ): {mean_y:.4f}")
    st.write("_(평균은 데이터를 모두 더한 뒤 개수로 나눈 값으로, 데이터의 중심을 나타냅니다.)_")
    st.write("---") # 구분선

    # 중앙값 출력
    st.write(f"**{x_var_name}**의 중앙값: {median_x:.4f}")
    st.write(f"**{y_var_name}**의 중앙값: {median_y:.4f}")
    st.write("_(중앙값은 데이터를 크기 순서대로 나열했을 때 가장 중앙에 위치하는 값으로, 극단적인 값에 영향을 덜 받습니다.)_")
    st.write("---") # 구분선

    # 최빈값 출력
    st.write(f"**{x_var_name}**의 최빈값:")
    if mode_x_result is not None and len(x_np) > 0:
        mode_val_x = mode_x_result.mode
        count_x = mode_x_result.count[0] if not np.isscalar(mode_x_result.count) else mode_x_result.count

        if count_x == 1 and len(x_np) == len(np.unique(x_np)):
             st.info(f"  모든 {x_var_name} 값이 한 번씩만 나타나 최빈값이 없습니다.")
        else:
             if isinstance(mode_val_x, np.ndarray):
                 if mode_val_x.size > 1:
                      st.write(f"  {mode_val_x} (개수: {count_x}회)")
                      st.info("  참고: 최빈값이 여러 개입니다.")
                 else:
                      st.write(f"  {mode_val_x.item()} (개수: {count_x}회)")
             else:
                  st.write(f"  {mode_val_x} (개수: {count_x}회)")

    elif len(x_np) == 0:
         st.info(f"  {x_var_name} 값이 없어 최빈값을 계산할 수 없습니다.")


    st.write(f"**{y_var_name}**의 최빈값:")
    if mode_y_result is not None and len(y_np) > 0:
        mode_val_y = mode_y_result.mode
        count_y = mode_y_result.count[0] if not np.isscalar(mode_y_result.count) else mode_y_result.count

        if count_y == 1 and len(y_np) == len(np.unique(y_np)):
             st.info(f"  모든 {y_var_name} 값이 한 번씩만 나타나 최빈값이 없습니다.")
        else:
             if isinstance(mode_val_y, np.ndarray):
                 if mode_val_y.size > 1:
                      st.write(f"  {mode_val_y} (개수: {count_y}회)")
                      st.info("  참고: 최빈값이 여러 개입니다.")
                 else:
                      st.write(f"  {mode_val_y.item()} (개수: {count_y}회)")
             else:
                  st.write(f"  {mode_val_y} (개수: {count_y}회)")
    elif len(y_np) == 0:
         st.info(f"  {y_var_name} 값이 없어 최빈값을 계산할 수 없습니다.")

    st.write("_(최빈값은 데이터에서 가장 자주 나타나는 값으로, 하나 이상이거나 없을 수도 있습니다.)_")
    st.write("---") # 구분선


    # 표준편차 출력
    st.write(f"**{x_var_name}**의 표준편차 (Sx):")
    if std_x is not None:
         st.write(f"  {std_x:.4f}")
    else:
         st.info(f"  데이터 부족 ({len(x_np)}개)으로 계산 불가")

    st.write(f"**{y_var_name}**의 표준편차 (Sy):")
    if std_y is not None:
         st.write(f"  {std_y:.4f}")
    else:
         st.info(f"  데이터 부족 ({len(y_np)}개)으로 계산 불가")
    st.write("_(표준편차는 데이터가 평균으로부터 얼마나 퍼져있는지(산포도)를 나타내는 값입니다.)_")

    st.write("---") # 구분선


    # 상관계수 계산
    x_deviations = x_np - mean_x
    y_deviations = y_np - mean_y
    sum_of_products_of_deviations = np.sum(x_deviations * y_deviations)
    sum_of_sq_x_deviations = np.sum(x_deviations**2)
    sum_of_sq_y_deviations = np.sum(y_deviations**2)

    numerator = sum_of_products_of_deviations
    denominator = np.sqrt(sum_of_sq_x_deviations * sum_of_sq_y_deviations)

    correlation_coefficient = 0
    can_calculate_correlation = denominator != 0

    if can_calculate_correlation:
        correlation_coefficient = numerator / denominator

    st.subheader("상관계수 (r)")
    st.write(f"**{x_var_name}**와 **{y_var_name}**의 상관계수 r = **{correlation_coefficient:.4f}**")

    if not can_calculate_correlation and len(x_np) >= 2:
         st.info(f"데이터가 모두 같아 상관계수 계산 불가")
    elif abs(correlation_coefficient) >= 0.7:
        st.info("강한 양/음의 상관관계")
    elif abs(correlation_coefficient) >= 0.3:
        st.info("보통 양/음의 상관관계")
    elif abs(correlation_coefficient) >= 0.1:
         st.info("약한 양/음의 상관관계")
    elif len(x_np) >= 2 :
        st.info("거의 상관관계 없음")


    if can_calculate_correlation:
        if correlation_coefficient > 0:
            st.info("양의 상관관계: 한 변수 증가 시 다른 변수도 증가 경향")
        elif correlation_coefficient < 0:
            st.info("음의 상관관계: 한 변수 증가 시 다른 변수는 감소 경향")
    elif len(x_np) < 2:
         st.info("데이터 부족으로 상관계수 계산 불가")


    # 회귀식 계산
    st.subheader("회귀식")
    # 👇👇👇 여기에 회귀식 설명을 추가합니다 👇👇👇
    st.write("회귀식은 두 변수(X와 Y) 사이의 가장 잘 맞는 직선 관계를 나타내는 공식이에요. 이 공식을 이용하면 X 값을 알 때 Y 값을 예측해 볼 수 있습니다.")
    # 👆👆👆 여기에 회귀식 설명을 추가합니다 👆👆👆


    slope = None
    intercept = mean_y

    can_calculate_regression = sum_of_sq_x_deviations != 0

    if can_calculate_regression:
        slope = sum_of_products_of_deviations / sum_of_sq_x_deviations
        intercept = mean_y - slope * mean_x

        st.write(f"회귀식: Ŷ = **{intercept:.4f}** + **{slope:.4f}**X")
        st.write(f"_(여기서 X는 '{x_var_name}', Ŷ는 '{y_var_name}'에 대한 예측값)_")
    elif len(x_np) >= 2:
        st.warning(f"{x_var_name} 값이 모두 같아 회귀식 계산 불가 (수직선 형태)")
        st.write(f"'{x_var_name}'는 고정값(**{mean_x:.4f}**), '{y_var_name}'의 평균값은 **{mean_y:.4f}**")
    else:
         st.warning("데이터 부족으로 회귀식 계산 불가")


    # 산점도 시각화
    st.subheader("산점도")
    st.write("산점도는 조사한 데이터 쌍(X 값과 Y 값) 하나하나를 점으로 나타낸 그래프입니다. 두 변수 사이에 어떤 관계(점들이 모여서 오른쪽 위/아래로 올라가는지, 흩어져 있는지)가 있는지 눈으로 쉽게 확인할 수 있습니다.")
    st.write("그래프 위에 마우스 커서를 올리면 보이는 우측 상단 작은 카메라 버튼을 눌러 png 사진 파일로 저장하여 보고서에 첨부할 수 있습니다.")
    st.empty()
    st.empty()
    st.write(f"'{x_var_name}'와 '{y_var_name}'의 산점도 그래프:")
    


    # --- 그래프 그리기 시작 (Plotly에 표시) ---
    # Plotly를 사용합니다.
    fig = go.Figure() # Plotly Figure 객체 생성

    if len(x_np) >= 2:
        # 산점도 데이터 추가
        fig.add_trace(go.Scatter(
            x=x_np,
            y=y_np,
            mode='markers', # 점으로 표시
            name='Data Points' # 범례 이름
        ))

        # 회귀선 추가 (계산 가능할 때만)
        if can_calculate_regression:
            if np.max(x_np) - np.min(x_np) == 0:
                 x_range = np.array([x_np[0] - 1, x_np[0] + 1])
            else:
                x_range = np.array([np.min(x_np) - (np.max(x_np) - np.min(x_np)) * 0.1,
                                    np.max(x_np) + (np.max(x_np) - np.min(x_np)) * 0.1])

            y_line = intercept + slope * x_range
            fig.add_trace(go.Scatter(
                x=x_range,
                y=y_line,
                mode='lines', # 선으로 표시
                name=f'회귀선 (Ŷ = {intercept:.2f} + {slope:.2f}X)', # 범례 이름
                line=dict(color='red') # 선 색상
            ))

        elif len(np.unique(x_np)) == 1: # X 값이 모두 같아서 수직선 형태일 때
             fig.add_trace(go.Scatter(
                x=[mean_x, mean_x], # X 값 고정
                y=[np.min(y_np), np.max(y_np)], # Y 값 최소~최대 범위
                mode='lines',
                name=f'X = {mean_x:.2f} ({x_var_name})',
                line=dict(color='red', dash='dash') # 점선
            ))


        # 그래프 레이아웃 업데이트 (제목, 축 이름)
        if can_calculate_regression:
             fig.update_layout(title=f'[{x_var_name}]와 [{y_var_name}]의 산점도 및 회귀선',
                               xaxis_title=x_var_name,
                               yaxis_title=y_var_name,
                               width=700, # 예시 너비 (픽셀 단위)
                               height=500) # 예시 높이 (픽셀 단위)
        elif len(np.unique(x_np)) == 1:
              fig.update_layout(title=f'[{x_var_name}] 값이 고정된 산점도',
                               xaxis_title=x_var_name,
                               yaxis_title=y_var_name, 
                               width=700, # 예시 너비 (픽셀 단위)
                               height=500) # 예시 높이 (픽셀 단위)
        else:
             fig.update_layout(title=f'[{x_var_name}]와 [{y_var_name}]의 산점도', # 데이터 2개 이상이지만 회귀선/수직선 없는 경우
                               xaxis_title=x_var_name,
                               yaxis_title=y_var_name,
                               width=700, # 예시 너비 (픽셀 단위)
                               height=500) # 예시 높이 (픽셀 단위)
    

        # Streamlit에 Plotly 그래프 표시
        st.plotly_chart(fig, use_container_width=False) # use_container_width로 화면 너비에 맞춤


    else: # 데이터 쌍이 2개 미만이어서 산점도를 그릴 수 없을 때
        st.info("데이터 쌍이 2개 미만이라 산점도를 그릴 수 없습니다.")


    # plt.close(fig) # Plotly 사용 시 필요 없음


    st.write("--- 통계 분석 완료 ---")

    # 여기에 이름 표시 코드를 추가합니다
    st.caption("제작: 도담고 사회문제탐구 교사가 도담고 3학년 학생들을 사랑하고 응원하는 마음으로 제작함")
