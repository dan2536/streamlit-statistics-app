import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
# Matplotlib 한글 설정 (웹 환경에서도 적용되도록 코드에 포함)
plt.rcParams['font.family'] = 'Malgun Gothic' # 예시: Windows 사용자라면 'Malgun Gothic' 시도
plt.rcParams['axes.unicode_minus'] = False # 마이너스 부호 깨짐 방지

# --- 웹 페이지 기본 설정 ---
st.set_page_config(page_title="학생용 통계 분석 웹 프로그램", layout="wide")

st.title("📊 학생용 통계 분석 프로그램")
st.write("두 변수(X, Y)의 관계를 분석하고, 기술 통계, 상관계수, 회귀식, 산점도를 보여줍니다.")

# --- 데이터 입력 섹션 ---
st.header("데이터 입력")

# 변수명 입력
col_var_name1, col_var_name2 = st.columns(2)
with col_var_name1:
    x_var_name = st.text_input("X 변수명 입력:", "X")
with col_var_name2:
    y_var_name = st.text_input("Y 변수명 입력:", "Y")

st.write("---") # 구분선 추가

# 응답자 수 입력
num_respondents = st.number_input("총 응답자(데이터 쌍) 수 입력:", min_value=2, value=2, step=1)

st.write(f"아래에 {num_respondents}명의 응답자 데이터를 입력해주세요.")

# 각 응답자별 데이터 입력 칸 생성
# 사용자 입력에 따라 동적으로 위젯을 생성할 때는 Streamlit의 'key'가 중요합니다.
input_cols = st.columns(2) # X와 Y 입력을 나란히 배치할 열
x_inputs = {} # X 입력 위젯 값 저장 딕셔너리
y_inputs = {} # Y 입력 위젯 값 저장 딕셔너리
input_errors = [] # 입력별 오류 저장 리스트

# 응답자 수 만큼 입력 칸 생성
for i in range(int(num_respondents)):
    # 각 입력 칸에 고유한 'key'를 부여해야 Streamlit이 값을 제대로 추적합니다.
    x_inputs[i] = input_cols[0].text_input(f"응답자 {i+1}: {x_var_name} 값", key=f"x_input_{i}")
    y_inputs[i] = input_cols[1].text_input(f"응답자 {i+1}: {y_var_name} 값", key=f"y_input_{i}")


# --- 분석 실행 버튼 ---
# 버튼은 모든 입력 칸 아래에 위치
analyze_button = st.button("통계 분석 실행")

# --- 분석 로직 및 결과 표시 섹션 ---
if analyze_button: # 버튼이 클릭되면 이 블록 실행
    st.header("분석 결과")

    x_data = []
    y_data = []
    errors = [] # 데이터 파싱 오류

    # 각 응답자 입력 칸에서 값 읽어오기 및 파싱
    for i in range(int(num_respondents)):
        x_val_str = x_inputs[i].strip() # 입력 값 가져와서 좌우 공백 제거
        y_val_str = y_inputs[i].strip()

        # X 값 파싱 및 검증
        if not x_val_str:
             errors.append(f"응답자 {i+1}: {x_var_name} 값이 비어 있습니다.")
        else:
            try:
                x_data.append(float(x_val_str))
            except ValueError:
                errors.append(f"응답자 {i+1}: '{x_val_str}'는 유효한 {x_var_name} 숫자가 아닙니다.")

        # Y 값 파싱 및 검증
        if not y_val_str:
             errors.append(f"응답자 {i+1}: {y_var_name} 값이 비어 있습니다.")
        else:
            try:
                y_data.append(float(y_val_str))
            except ValueError:
                 errors.append(f"응답자 {i+1}: '{y_val_str}'는 유효한 {y_var_name} 숫자가 아닙니다.")

    # --- 데이터 유효성 검사 (파싱 후) ---
    # 이 단계에서는 파싱 오류, 개수 불일치(이 방식에서는 발생 어려움), 최소 개수만 확인

    if errors:
        for err in errors:
            st.error(err) # 개별 입력 오류 표시
        st.warning("입력 데이터에 오류가 있습니다. 분석을 중단합니다.")
        st.stop() # 오류 발생 시 분석 중단

    # 응답자 수와 실제 파싱된 데이터 개수 일치 확인 (이미 반복문에서 처리되므로 형식상 확인)
    if len(x_data) != len(y_data):
         # 이 경우는 위의 반복문에서 파싱 오류로 이미 걸러졌을 가능성이 높지만 안전을 위해 둠
         st.error(f"내부 오류: 파싱된 {x_var_name} 값 개수({len(x_data)})와 {y_var_name} 값 개수({len(y_data)})가 다릅니다.")
         st.warning("데이터 개수 불일치 오류. 분석을 중단합니다.")
         st.stop()

    # 최소 데이터 쌍 개수 확인
    if len(x_data) < 2:
         # 응답자 수 입력 min_value=2로 막아두었지만 안전을 위해 둠
         st.error(f"오류: 데이터 쌍은 최소 2개 이상이어야 합니다. 현재 {len(x_data)}개 입니다.")
         st.warning("데이터 개수 부족 오류. 분석을 중단합니다.")
         st.stop()


    # 유효성 검사 통과 후 NumPy 배열로 변환
    x_np = np.array(x_data)
    y_np = np.array(y_data)

    st.success("데이터 입력 및 유효성 검사 통과. 분석을 진행합니다.")

    # --- 간결한 결과 출력 시작 ---

    st.write("입력된 데이터 요약:")
    st.text(f"  {x_var_name} 값 ({len(x_np)}개): {x_np}")
    st.text(f"  {y_var_name} 값 ({len(y_np)}개): {y_np}")


    # 기술 통계 (평균 및 표준편차)
    mean_x = np.mean(x_np)
    mean_y = np.mean(y_np)
    # 표준편차 계산 (표본 표준편차: ddof=1) - 데이터가 1개 이하면 표준편차 계산 불가하므로 조건 추가
    std_x = np.std(x_np, ddof=1) if len(x_np) > 1 else None
    std_y = np.std(y_np, ddof=1) if len(y_np) > 1 else None


    st.subheader("기술 통계")
    st.write(f"**{x_var_name}**의 평균 (X̄): {mean_x:.4f}")
    # 표준편차 결과 출력 (데이터 1개 초과 시에만)
    if std_x is not None:
         st.write(f"**{x_var_name}**의 표준편차 (Sx): {std_x:.4f}")
    else:
         st.info(f"**{x_var_name}**의 표준편차: 데이터 부족 ({len(x_np)}개)으로 계산 불가")


    st.write(f"**{y_var_name}**의 평균 (ȳ): {mean_y:.4f}")
    # 표준편차 결과 출력 (데이터 1개 초과 시에만)
    if std_y is not None:
         st.write(f"**{y_var_name}**의 표준편차 (Sy): {std_y:.4f}")
    else:
         st.info(f"**{y_var_name}**의 표준편차: 데이터 부족 ({len(y_np)}개)으로 계산 불가")

    st.write("_(표준편차는 데이터가 평균으로부터 얼마나 퍼져있는지를 나타냅니다.)_")


    # 상관계수 계산
    st.subheader("상관계수 (r)")
    # 상관계수 계산 및 출력 로직은 이전과 동일


    # 회귀식 계산
    st.subheader("회귀식")
    # 회귀식 계산 및 출력 로직은 이전과 동일


    # 산점도 시각화
    st.subheader("산점도")
    st.write(f"'{x_var_name}'와 '{y_var_name}'의 산점도 그래프:")

    # --- 그래프 그리기 시작 (Streamlit에 표시) ---
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(x_np, y_np, color='blue', label='Data Points')

    # 회귀선 추가 (기울기를 계산할 수 있을 때만)
    can_calculate_correlation = sum_of_sq_x_deviations != 0 # 상관계수 분모 0 아니면 회귀선 가능
    can_calculate_regression = sum_of_sq_x_deviations != 0 # 회귀식 분모 0 아니면 회귀선 가능

    if can_calculate_regression:
        if np.max(x_np) - np.min(x_np) == 0:
            x_range = np.array([x_np[0] - 1 if x_np[0] - 1 < x_np[0] else x_np[0], x_np[0] + 1 if x_np[0] + 1 > x_np[0] else x_np[0] + 1])
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

    st.pyplot(fig)
    plt.close(fig)


    st.write("--- 통계 분석 완료 ---")
