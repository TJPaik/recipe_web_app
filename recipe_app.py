import streamlit as st
import time

# --- 암호 확인 로직 (앱 시작 부분에 추가) ---
def check_password():
    """비밀번호 입력 및 확인 함수"""
    # Streamlit Secrets 사용 (권장)
    # 앱 배포 후 Streamlit Community Cloud 설정에서 'APP_PASSWORD' 라는 Secret을 설정해야 함
    # 로컬 테스트 시에는 secrets.toml 파일을 사용하거나 아래 기본값을 임시로 사용
    try:
        # secrets.toml 또는 클라우드 환경의 secrets에서 값 가져오기 시도
        correct_password = st.secrets["APP_PASSWORD"]
    except FileNotFoundError:
        # 로컬에 secrets.toml 파일이 없고 클라우드 환경도 아닐 경우 (또는 secrets에 APP_PASSWORD가 없을 경우)
        st.warning("Secrets 설정 파일을 찾을 수 없습니다. 기본 비밀번호 '1234'를 사용합니다. (배포 시 Secrets 설정 필수)", icon="⚠️")
        correct_password = "1234" # 로컬 테스트용 기본 비밀번호 (실제 배포 시 Secrets 사용!)
    except KeyError:
         # secrets 파일/환경은 있으나 APP_PASSWORD 키가 없을 경우
        st.warning("Secrets에 'APP_PASSWORD'가 정의되지 않았습니다. 기본 비밀번호 '1234'를 사용합니다. (배포 시 Secrets 설정 필수)", icon="⚠️")
        correct_password = "1234" # 로컬 테스트용 기본 비밀번호

    # 세션 상태를 사용하여 로그인 상태 유지
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("🔒 레시피 북 접근")
        st.markdown("이 레시피 북에 접근하려면 암호를 입력하세요.")
        # 비밀번호 입력 필드와 로그인 버튼을 form 안에 넣어 Enter 키로도 제출 가능하게 함
        with st.form("password_form"):
            password = st.text_input("암호:", type="password")
            submitted = st.form_submit_button("로그인")
            if submitted:
                if password == correct_password:
                    st.session_state["password_correct"] = True
                    st.success("로그인 성공!", icon="🎉")
                    time.sleep(0.5) # 성공 메시지 표시 후 잠시 대기
                    st.rerun() # 비밀번호 입력 필드 숨기고 앱 내용 표시
                else:
                    st.error("암호가 잘못되었습니다.", icon="🚨")
        return False # 비밀번호가 맞지 않거나 아직 제출 안 됐으면 False 반환
    else:
        return True # 비밀번호가 맞으면 True 반환

# --- 메인 앱 로직 실행 ---
if check_password():
    # --- 페이지 설정 (로그인 후에만 실행) ---
    # st.set_page_config는 스크립트 실행 시 한 번만 호출 가능하며 최상단에 위치해야 함.
    # 로그인 상태에 따라 페이지 설정을 다르게 하려면 복잡해지므로,
    # 페이지 설정은 로그인 여부와 관계없이 스크립트 상단에 한 번만 두는 것이 일반적.
    # 여기서는 로그인 성공 시에만 앱 콘텐츠가 보이도록 하므로, 페이지 설정 자체는 밖에 두어도 무방하나,
    # 로그인 화면에서도 동일한 페이지 설정을 원하면 check_password() 함수 호출 전에 위치.
    # 일관성을 위해 여기에 두되, 필요시 위로 이동 가능.
    st.set_page_config(
        page_title="나만의 레시피 북",
        page_icon="🍳",
        layout="wide"
    )

    # --- 앱 제목 ---
    st.title("🍳 나만의 레시피 북 (비공개)")
    st.caption("원하는 레시피를 검색하고, 태그로 필터링하세요.")

    # --- 레시피 데이터 (세션 상태 사용, 로그인 후에만 초기화/사용) ---
    if 'recipes' not in st.session_state:
        st.session_state['recipes'] = {
            "김치찌개": {
                "description": "얼큰하고 맛있는 한국인의 소울푸드",
                "ingredients": [
                    "잘 익은 김치 1/4포기", "돼지고기 (목살 또는 삼겹살) 200g", "두부 1/2모",
                    "양파 1/4개", "대파 1/2대", "청양고추 1개 (선택 사항)",
                    "멸치 다시마 육수 3컵", "고춧가루 1큰술", "다진 마늘 1/2큰술",
                    "국간장 1작은술", "설탕 1/2작은술 (김치 신맛에 따라 조절)", "식용유 약간"
                ],
                "instructions": [
                    "돼지고기는 먹기 좋게 썰고, 김치도 속을 털어내고 적당히 썬다.",
                    "두부, 양파, 대파, 고추도 썰어 준비한다.",
                    "냄비에 식용유를 두르고 돼지고기를 볶다가 김치를 넣고 함께 볶는다.",
                    "멸치 다시마 육수를 붓고 고춧가루, 다진 마늘을 넣어 끓인다.",
                    "찌개가 끓으면 양파와 두부를 넣고 한소끔 더 끓인다.",
                    "국간장과 설탕으로 간을 맞춘다.",
                    "마지막에 대파와 청양고추를 넣고 불을 끈다."
                ],
                "image_url": "https://img.khan.co.kr/news/2020/01/15/l_2020011601001866300140811.jpg",
                "tags": ["한식", "찌개", "매운맛", "돼지고기", "김치"]
            },
            "계란찜": {
                "description": "부드럽고 촉촉한 영양 만점 계란찜",
                "ingredients": [
                    "계란 3개", "물 또는 다시마 육수 150ml", "새우젓 1작은술 (또는 소금 약간)",
                    "다진 파 약간", "참기름 약간 (선택 사항)"
                ],
                "instructions": [
                    "계란을 볼에 풀고 물(육수)과 새우젓(소금)을 넣어 잘 섞는다.",
                    "체에 한번 걸러 알끈을 제거하면 더 부드럽다.",
                    "뚝배기나 내열 용기에 계란물을 붓는다.",
                    "냄비에 물을 약간 넣고 용기를 올린 뒤 뚜껑을 닫고 중약불에서 10~15분간 찐다. (전자레인지 사용 시 랩을 씌우고 구멍을 뚫어 3~4분 돌린다)",
                    "다 익으면 다진 파와 참기름을 뿌린다."
                ],
                 "image_url": None,
                 "tags": ["한식", "반찬", "간단", "아이들", "계란"]
            },
            "알리오 올리오": {
                "description": "마늘과 올리브 오일의 풍미가 가득한 파스타",
                "ingredients": [
                    "스파게티 면 100g", "마늘 5-6쪽", "페페론치노 2-3개 (또는 건고추)",
                    "올리브 오일 4큰술", "소금 약간", "후추 약간", "파슬리 가루 (선택 사항)",
                    "면수 1/2컵"
                ],
                "instructions": [
                    "끓는 물에 소금을 넣고 스파게티 면을 삶는다 (포장지 시간 참고). 면수는 버리지 않는다.",
                    "마늘은 편으로 썰고, 페페론치노는 잘게 부순다.",
                    "팬에 올리브 오일을 두르고 약불에서 마늘과 페페론치노를 볶아 향을 낸다.",
                    "마늘이 노릇해지면 삶은 면과 면수 1/2컵을 넣고 빠르게 섞는다.",
                    "오일과 면수가 유화되어 소스처럼 걸쭉해지면 소금, 후추로 간을 맞춘다.",
                    "불을 끄고 파슬리 가루를 뿌려 마무리한다."
                ],
                "image_url": None,
                "tags": ["양식", "파스타", "간단", "마늘", "매콤"]
            }
        }

    # --- 사이드바: 레시피 검색, 필터링, 선택 ---
    st.sidebar.header("🔍 레시피 탐색")

    # 1. 검색 기능 (이름 또는 재료)
    search_term = st.sidebar.text_input("레시피 이름 또는 재료 검색")

    # 2. 태그 필터링 기능
    all_tags = set()
    for recipe_data in st.session_state.recipes.values():
        all_tags.update(recipe_data.get("tags", []))

    selected_tags = st.sidebar.multiselect(
        "태그로 필터링 (모두 포함):",
        options=sorted(list(all_tags)),
    )

    # 3. 필터링 및 검색 로직 적용
    recipe_names = list(st.session_state.recipes.keys())
    filtered_recipe_names = []

    for name in recipe_names:
        recipe_data = st.session_state.recipes[name]
        matches_search = True
        matches_tags = True

        # 검색어 확인
        if search_term:
            search_term_lower = search_term.lower()
            name_match = search_term_lower in name.lower()
            ingredient_match = any(search_term_lower in ingredient.lower() for ingredient in recipe_data.get("ingredients", []))
            if not (name_match or ingredient_match):
                matches_search = False

        # 태그 확인
        if selected_tags:
            recipe_tags = set(recipe_data.get("tags", []))
            if not set(selected_tags).issubset(recipe_tags):
                matches_tags = False

        # 최종 필터링
        if matches_search and matches_tags:
            filtered_recipe_names.append(name)

    # 4. 필터링된 레시피 목록 표시 및 선택
    st.sidebar.divider()
    st.sidebar.subheader("📖 레시피 목록")

    selected_recipe_name = None # 먼저 None으로 초기화
    if not filtered_recipe_names:
        st.sidebar.warning("조건에 맞는 레시피가 없습니다.")
    else:
        selected_recipe_name = st.sidebar.radio(
            f"{len(filtered_recipe_names)}개의 레시피:",
            sorted(filtered_recipe_names), # 이름순 정렬
            index=0 if filtered_recipe_names else None,
            key="recipe_radio" # 명시적인 키 할당
        )

    # --- 메인 화면: 선택된 레시피 상세 정보 표시 ---
    if selected_recipe_name:
        st.subheader(f"📜 {selected_recipe_name}")
        recipe = st.session_state.recipes[selected_recipe_name]

        # 설명
        if "description" in recipe and recipe["description"]:
            st.markdown(f"*{recipe['description']}*")

        # 태그
        if "tags" in recipe and recipe["tags"]:
            tag_html = "".join([f'<span style="background-color: #f0f2f6; color: #31333f; border-radius: 5px; padding: 2px 6px; margin: 2px;">{tag}</span>' for tag in recipe["tags"]])
            st.markdown(f"**태그:** {tag_html}", unsafe_allow_html=True)
        else:
             st.markdown("**태그:** 없음")

        st.divider()

        # 이미지
        if "image_url" in recipe and recipe["image_url"]:
            st.image(recipe["image_url"], caption=selected_recipe_name, use_container_width=True)
            st.divider()

        # 재료 및 만드는 법
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥕 재료")
            if recipe.get("ingredients"):
                ingredient_list = "\n".join([f"- {item}" for item in recipe['ingredients']])
                st.markdown(ingredient_list)
            else:
                st.markdown("재료 정보가 없습니다.")
        with col2:
            st.markdown("#### 📝 만드는 법")
            if recipe.get("instructions"):
                instruction_list = "\n".join([f"{i+1}. {step}" for i, step in enumerate(recipe['instructions'])])
                st.markdown(instruction_list)
            else:
                st.markdown("만드는 법 정보가 없습니다.")

    else:
        # 필터링된 결과가 없을 때와 초기 상태 메시지 구분
        if search_term or selected_tags:
            st.warning("현재 검색 또는 필터 조건에 맞는 레시피가 없습니다. 조건을 변경해보세요.")
        else:
            st.info("👈 사이드바에서 레시피를 선택하거나, 검색 또는 태그 필터링을 사용해보세요.")

    # --- (사이드바 하단) 레시피 추가 기능 ---
    st.sidebar.divider()
    with st.sidebar.expander("✨ 새 레시피 추가"):
        # 각 입력 위젯에 고유한 key를 부여하여 상태 유지 문제 방지
        with st.form("new_recipe_form", clear_on_submit=True):
            new_recipe_name = st.text_input("레시피 이름*", help="필수 항목입니다.", key="new_name")
            new_description = st.text_input("간단한 설명", key="new_desc")
            new_ingredients = st.text_area("재료* (한 줄에 하나씩 입력)", height=150, help="필수 항목입니다.", key="new_ingr")
            new_instructions = st.text_area("만드는 법* (한 단계씩 줄 바꿔 입력)", height=250, help="필수 항목입니다.", key="new_instr")
            new_tags_input = st.text_input("태그 (쉼표(,)로 구분)", help="예: 한식, 찌개, 매운맛", key="new_tags")
            new_image_url = st.text_input("이미지 URL", key="new_img")

            submitted = st.form_submit_button("레시피 추가하기")
            if submitted:
                if not new_recipe_name or not new_ingredients or not new_instructions:
                    st.warning("레시피 이름, 재료, 만드는 법은 필수 항목입니다.", icon="⚠️")
                elif new_recipe_name in st.session_state.recipes:
                    st.error(f"'{new_recipe_name}' 이름의 레시피가 이미 존재합니다.", icon="🚨")
                else:
                    new_tags_list = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()]
                    ingredients_list = [item.strip() for item in new_ingredients.split('\n') if item.strip()]
                    instructions_list = [step.strip() for step in new_instructions.split('\n') if step.strip()]

                    st.session_state.recipes[new_recipe_name] = {
                        "description": new_description,
                        "ingredients": ingredients_list,
                        "instructions": instructions_list,
                        "image_url": new_image_url if new_image_url else None,
                        "tags": new_tags_list
                    }
                    st.success(f"'{new_recipe_name}' 레시피가 성공적으로 추가되었습니다!", icon="✅")
                    time.sleep(1.5)
                    st.rerun() # 레시피 목록 및 태그 목록 업데이트

    # --- (사이드바 하단) 레시피 삭제 기능 ---
    st.sidebar.divider()
    with st.sidebar.expander("🗑️ 레시피 삭제"):
        all_recipe_names_for_delete = sorted(list(st.session_state.recipes.keys()))

        if not all_recipe_names_for_delete:
            st.write("삭제할 레시피가 없습니다.")
        else:
            recipe_to_delete = st.selectbox(
                "삭제할 레시피 선택",
                options=[""] + all_recipe_names_for_delete,
                key="delete_select",
                index=0
            )
            if recipe_to_delete:
                # 삭제 버튼을 위한 placeholder 사용
                delete_button_placeholder = st.empty()
                # type="primary"는 빨간색 버튼 (주의 강조)
                if delete_button_placeholder.button(f"'{recipe_to_delete}' 삭제 확인", type="primary", key=f"delete_btn_{recipe_to_delete}"):
                    del st.session_state.recipes[recipe_to_delete]
                    delete_button_placeholder.success(f"'{recipe_to_delete}' 레시피가 삭제되었습니다.", icon="🗑️")
                    time.sleep(1.5)
                    st.rerun() # 앱 다시 실행하여 목록 업데이트

    # --- 로그아웃 버튼 (사이드바 가장 하단) ---
    st.sidebar.divider()
    if st.sidebar.button("로그아웃", key="logout_button"):
        st.session_state["password_correct"] = False
        # 로그아웃 후 확인 메시지 (선택적)
        st.success("로그아웃되었습니다.", icon="👋")
        time.sleep(1)
        st.rerun() # 로그인 화면으로 돌아가기
