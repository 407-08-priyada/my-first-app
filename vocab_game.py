import time
import streamlit as st

st.title("⏱️ เกมเติมศัพท์จับเวลา")

# 1. กำหนดค่าเริ่มต้นใน session_state ถ้ายังไม่มี
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "is_ended" not in st.session_state:
    st.session_state.is_ended = False


# 📌 ฟังก์ชันเคลียร์ค่าเมื่อกดปุ่มเริ่มใหม่
def reset_game():
    for k in ["ans1", "ans2", "ans3", "ans4"]:
        if k in st.session_state:
            st.session_state[k] = ""
    st.session_state.start_time = time.time()  # เริ่มเวลาใหม่
    st.session_state.is_ended = False  # รีเซ็ตสถานะจบเกม


# ----------------------------------------------------
# 📌 ฟังก์ชัน MessageBox (Dialog)
# ----------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog():
    st.balloons()
    score = 0

    u_ans1 = st.session_state.get("ans1", "").strip().lower()
    u_ans2 = st.session_state.get("ans2", "").strip().lower()
    u_ans3 = st.session_state.get("ans3", "").strip().lower()
    u_ans4 = st.session_state.get("ans4", "").strip().lower()

    # ตรวจข้อ 1
    if u_ans1 == "apple":
        st.success("✅ ข้อ 1: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 1: ยังไม่ถูกต้อง (คุณตอบ '{u_ans1}')")

    # ตรวจข้อ 2
    if u_ans2 == "fish":
        st.success("✅ ข้อ 2: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 2: ยังไม่ถูกต้อง (คุณตอบ '{u_ans2}')")

    # ตรวจข้อ 3 (mango)
    if u_ans3 == "mango":
        st.success("✅ ข้อ 3: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 3: ยังไม่ถูกต้อง (คุณตอบ '{u_ans3}')")

    # ตรวจข้อ 4 (pencil)
    if u_ans4 == "pencil":
        st.success("✅ ข้อ 4: ถูกต้อง")
        score += 1
    else:
        st.error(f"❌ ข้อ 4: ยังไม่ถูกต้อง (คุณตอบ '{u_ans4}')")

    st.divider()
    st.info(f"🏆 ได้คะแนนรวม: {score} / 4 คะแนน")

    if score == 4:
        st.success("🎉 You win! เก่งมากค่ะ!")
    else:
        st.error("💀 You lose! พยายามใหม่อีกครั้งนะ")


# ----------------------------------------------------
# 📌 ฟังก์ชันล็อกโซนเวลานับถอยหลัง ไม่ให้กวนช่องพิมพ์
# ----------------------------------------------------
@st.fragment
def countdown_timer():
    if (
        st.session_state.start_time is not None
        and not st.session_state.is_ended
    ):
        timer_placeholder = st.empty()
        while True:
            time_left = int(30 - (time.time() - st.session_state.start_time))
            if time_left > 0:
                timer_placeholder.error(f"⏳ เหลือเวลา: {time_left} วินาที")
                time.sleep(0.5)
            else:
                st.session_state.is_ended = True
                st.rerun()
                break


# ----------------------------------------------------
# 1. ปุ่มเริ่มเล่นเกม
# ----------------------------------------------------
st.button("🎮 เริ่มเล่นเกม / รีเซ็ตเกม", on_click=reset_game)

st.divider()

is_playing = (
    st.session_state.start_time is not None and not st.session_state.is_ended
)

if not is_playing and not st.session_state.is_ended:
    st.warning("💡 กรุณากดปุ่ม '🎮 เริ่มเล่นเกม' ด้านบนเพื่อเริ่มจับเวลาและทำโจทย์")

# 2. ช่องรับคำตอบ (ดึงคำศัพท์จากใบงาน และทำจำนวนขีดล่างตรงล็อกเป๊ะๆ)
st.text_input(
    "ข้อ 1: An `a _ _ l e` a day keeps the doctor away. 🍎",
    key="ans1",
    disabled=not is_playing,
)
st.text_input(
    "ข้อ 2: Cats love to eat `f _ s h`. 🐟",
    key="ans2",
    disabled=not is_playing,
)
st.text_input(
    "ข้อ 3: This fruit is yellow, sweet, and has a big seed. It is a `m _ _ _ o`. 🥭",
    key="ans3",
    disabled=not is_playing,
)
st.text_input(
    "ข้อ 4: We use a `p _ _ _ _ l` to write or draw on paper. ✏️",
    key="ans4",
    disabled=not is_playing,
)

# 3. แสดงเวลานับถอยหลัง และปุ่มส่งคำตอบ
if is_playing:
    countdown_timer()

    if st.button("📥 ส่งคำตอบ"):
        st.session_state.is_ended = True
        st.rerun()

# 4. แสดง Dialog ผลลัพธ์เมื่อจบเกม
if st.session_state.is_ended:
    show_result_dialog()

st.divider()
st.write("นางสาวปรียาดา สารทอง เลขที่ 8 ม.4/7")
