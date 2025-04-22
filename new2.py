import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# Matplotlib 한글 설정 (웹 환경에서도 적용되도록 코드에 포함)
# 시스템에 'Malgun Gothic' 폰트가 없는 경우 다른 폰트 이름으로 변경해야 합니다.
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 부호 깨짐 방지

# --- 웹 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 통계 분석 웹 프로그램", layout="wide")

st.title("📊 학생용 통계 분석 프로그램")
st.write("두 변수(X, Y)의 관계를 분석하고, 기술 통계, 상관계수, 회귀식, 산점도를 보여줍니다.") # 설명 업데이트

# --- 데이터 입력 섹션 ---
st.header("데이터 입력")

col1, col2 = st.columns(2) # 화면을 2개의 열로 나눔

with col1:
    x_var_name = st.text_input("X 변수명 입력:", "X") # X 변수명 입력
    x_data_str = st.text_area(f"{x_var_name} 값 입력 (각 값은 줄바꿈):", height=150) # X 데이터 입력

with col2:
    y_var_name = st.text_input("Y 변수명 입력:", "Y") # Y 변수명 입력
    y_data_str = st.text_area(f"{y_var_name} 값 입력 (각 값은 줄바꿈):", height=150) # Y 데이터 입력


# --- 분석 실행 버튼 ---
analyze_button = st.button("통계 분석 실행")

# --- 분석 로직 및 결과 표시 섹션 ---
if analyze_button: # 버튼이 클릭되면 이 블록 실행
    st.header("분석 결과")

    x_data = []
    y_data = []
    errors = []

    # X 값 파싱
    for i, line in enumerate(x_data_str.splitlines()):
        if line.strip():
            try:
                x_data.append(float(line.strip()))
            except ValueError:
                errors.append(f"{x_var_name} 값 오류 (줄 {i+1}): '{line.strip()}'는 유효한 숫자가 아닙니다.")

    # Y 값 파싱
    for i, line in enumerate(y_data_str.splitlines()):
         if line.strip():
            try:
                y_data.append(float(line.strip()))
            except ValueError:
                 errors.append(f"{y_var_name} 값 오류 (줄 {i+1}): '{line.strip()}'는 유효한 숫자가 아닙니다.")

    # --- 데이터 유효성 검사 ---
    if errors:
        for err in errors:
            st.error(err) # 오류 메시지를 빨간색으로 표시
        st.warning("데이터 오류 발생. 분석을 중단합니다.")
        st.stop() # 오류 발생 시 분석 중단
    elif len(x_data) != len(y_data):
         st.error(f"오류: {x_var_name} 값 개수({len(x_data)})와 {y_var_name} 값 개수({len(y_data)})가 다릅니다. 쌍으로 입력해주세요.")
         st.warning("데이터 개수 불일치 오류. 분석을 중단합니다.")
         st.stop() # 오류 발생 시 분석 중단
    elif len(x_data) < 2:
         st.error(f"오류: 데이터 쌍은 최소 2개 이상이어야 합니다. 현재 {len(x_data)}개 입니다.")
         st.warning("데이터 개수 부족 오류. 분석을 중단합니다.")
         st.stop() # 오류 발생 시 분석 중단


    # 유효성 검사 통과 후 NumPy 배열로 변환
    x_np = np.array(x_data)
    y_np = np.array(y_data)

    st.success("데이터 읽기 및 유효성 검사 통과. 분석을 진행합니다.")

    # --- 간결한 결과 출력 시작 ---

    st.write("입력된 데이터:")
    st.text(f"  {x_var_name}: {x_np}") # st.text는 고정폭 글꼴로 표시
    st.text(f"  {y_var_name}: {y_np}")


    # 기술 통계 (평균 및 표준편차 추가)
    mean_x = np.mean(x_np)
    mean_y = np.mean(y_np)
    # 표준편차 계산 (표본 표준편차: ddof=1) - 데이터가 1개 이하면 표준편차 계산 불가하므로 조건 추가
    std_x = np.std(x_np, ddof=1) if len(x_np) > 1 else None
    std_y = np.std(y_np, ddof=1) if len(y_np) > 1 else None


    st.subheader("기술 통계")
    st.write(f"**{x_var_name}**의 평균 (X̄): {mean_x:.4f}")
    # 표준편차 결과 출력 추가 (데이터 1개 초과 시에만)
    if std_x is not None:
         st.write(f"**{x_var_name}**의 표준편차 (Sx): {std_x:.4f}")
    else:
         st.write(f"**{x_var_name}**의 표준편차: 데이터 부족 ({len(x_np)}개)으로 계산 불가")


    st.write(f"**{y_var_name}**의 평균 (ȳ): {mean_y:.4f}")
    # 표준편차 결과 출력 추가 (데이터 1개 초과 시에만)
    if std_y is not None:
         st.write(f"**{y_var_name}**의 표준편차 (Sy): {std_y:.4f}")
    else:
         st.write(f"**{y_var_name}**의 표준편차: 데이터 부족 ({len(y_np)}개)으로 계산 불가")

    st.write("_(표준편차는 데이터가 평균으로부터 얼마나 퍼져있는지를 나타냅니다.)_")


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

    if not can_calculate_correlation:
         st.info(f"데이터가 모두 같아 상관계수 계산 불가")
    elif abs(correlation_coefficient) >= 0.7:
        st.info("강한 양/음의 상관관계")
    elif abs(correlation_coefficient) >= 0.3:
        st.info("보통 양/음의 상관관계")
    elif abs(correlation_coefficient) >= 0.1:
         st.info("약한 양/음의 상관관계")
    else:
        st.info("거의 상관관계 없음")

    if can_calculate_correlation: # 상관계수 계산 가능할 때만 방향 설명
        if correlation_coefficient > 0:
            st.info("양의 상관관계: 한 변수 증가 시 다른 변수도 증가 경향")
        elif correlation_coefficient < 0:
            st.info("음의 상관관계: 한 변수 증가 시 다른 변수 감소 경향")


    # 회귀식 계산
    st.subheader("회귀식")

    slope = None
    intercept = mean_y

    can_calculate_regression = sum_of_sq_x_deviations != 0

    if can_calculate_regression:
        slope = sum_of_products_of_deviations / sum_of_sq_x_deviations
        intercept = mean_y - slope * mean_x

        st.write(f"회귀식: Ŷ = **{intercept:.4f}** + **{slope:.4f}**X")
        st.write(f"_(여기서 X는 '{x_var_name}', Ŷ는 '{y_var_name}'에 대한 예측값)_")
    else:
        st.warning(f"{x_var_name} 값이 모두 같아 회귀식 계산 불가 (수직선 형태)")
        st.write(f"'{x_var_name}'는 고정값(**{mean_x:.4f}**), '{y_var_name}'의 평균값은 **{mean_y:.4f}**")

    # 산점도 시각화
    st.subheader("산점도")
    st.write(f"'{x_var_name}'와 '{y_var_name}'의 산점도 그래프:")


    # --- 그래프 그리기 시작 (Streamlit에 표시) ---
    fig, ax = plt.subplots(figsize=(8, 6)) # Figure와 Axes 객체를 생성

    ax.scatter(x_np, y_np, color='blue', label='Data Points') # 산점도 그리기

    # 회귀선 추가 (기울기를 계산할 수 있을 때만)
    if can_calculate_regression:
        # X 데이터의 범위를 약간 넓혀서 선을 그리면 그래프 양 끝까지 보기 좋음
        # 데이터 범위가 0인 경우 (min==max) 에러 방지
        if np.max(x_np) - np.min(x_np) == 0:
            x_range = np.array([x_np[0] - 1 if x_np[0] - 1 < x_np[0] else x_np[0], x_np[0] + 1 if x_np[0] + 1 > x_np[0] else x_np[0] + 1]) # 데이터 점 좌우로 임의 범위 설정, 데이터가 한 점일 때 범위가 0이 되지 않도록 처리
        else:
            x_range = np.array([np.min(x_np) - (np.max(x_np) - np.min(x_np)) * 0.1,
                                np.max(x_np) + (np.max(x_np) - np.min(x_np)) * 0.1])

        y_line = intercept + slope * x_range
        ax.plot(x_range, y_line, color='red', label=f'회귀선 (Ŷ = {intercept:.2f} + {slope:.2f}X)')
        ax.set_title(f'[{x_var_name}]와 [{y_var_name}]의 산점도 및 회귀선')

    elif len(np.unique(x_np)) == 1: # X 값이 모두 같아서 수직선 형태일 때
         ax.axvline(x=mean_x, color='red', linestyle='--', label=f'X = {mean_x:.2f} ({x_var_name})')
         ax.set_title(f'[{x_var_name}] 값이 고정된 산점도')
    else:
         ax.set_title('산점도 (데이터 부족)')


    ax.set_xlabel(x_var_name)
    ax.set_ylabel(y_var_name)
    ax.grid(True)
    ax.legend()

    # Streamlit에 그래프 표시
    st.pyplot(fig) # 생성한 Figure 객체를 Streamlit에 전달하여 표시
    plt.close(fig) # 그래프 표시 후 메모리 해제 (Streamlit 권장)


    st.write("--- 통계 분석 완료 ---")
