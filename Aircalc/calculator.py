import cv2
import numpy as np
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1600)
cap.set(4, 900)

button_texts = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

radius = 85
x_offset = 220
y_offset = 280
gap = 175

buttons = []
for i in range(4):
    for j in range(4):
        cx = x_offset + j * gap
        cy = y_offset + i * gap
        buttons.append({
            "center": (cx, cy),
            "text": button_texts[i][j],
            "pressed": False,
            "press_time": 0
        })

expression = ""
history = []
last_pressed = None
last_click_time = 0
click_delay = 0.6
pinch_threshold = 50

BG_COLOR = (18, 18, 18)
BTN_BASE = (35, 35, 35)
BTN_SHADOW_DARK = (12, 12, 12)
BTN_SHADOW_LIGHT = (60, 60, 60)
BTN_HIGHLIGHT = (0, 255, 140)
DISPLAY_BG = (22, 22, 22)
DISPLAY_GLOW = (0, 255, 140)
TEXT_COLOR = (200, 255, 210)
HISTORY_BG = (22, 22, 22, 180)

def draw_neumorphic_button(img, center, text, radius, pressed):
    x, y = center
    base = (50, 50, 50) if not pressed else (20, 150, 80)
    shadow_dark = (10, 10, 10) if not pressed else (0, 70, 30)
    shadow_light = (80, 80, 80) if not pressed else (90, 220, 140)
    text_color = (230, 255, 230) if not pressed else (220, 255, 220)

    cv2.circle(img, (x + 8, y + 8), radius, shadow_dark, -1)
    cv2.circle(img, (x - 8, y - 8), radius, shadow_light, -1)
    cv2.circle(img, center, radius, base, -1)

    highlight_radius = int(radius * 0.6)
    cv2.circle(img, (x - int(radius * 0.4), y - int(radius * 0.4)), highlight_radius, shadow_light, -1)

    if pressed:
        cv2.circle(img, center, radius + 6, BTN_HIGHLIGHT, 6, lineType=cv2.LINE_AA)

    font_scale = 3 if len(text) == 1 else 2.5
    thickness = 7
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x = x - text_size[0] // 2
    text_y = y + text_size[1] // 2
    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness, lineType=cv2.LINE_AA)

def draw_display(img, expression):
    x1, y1, x2, y2 = 140, 80, 760, 190
    cv2.rectangle(img, (x1, y1), (x2, y2), DISPLAY_BG, -1)
    for i in range(10):
        alpha = (10 - i) / 100
        color = (int(DISPLAY_GLOW[0] * alpha), int(DISPLAY_GLOW[1] * alpha), int(DISPLAY_GLOW[2] * alpha))
        cv2.rectangle(img, (x1 - i, y1 - i), (x2 + i, y2 + i), color, 1, lineType=cv2.LINE_AA)

    font_scale = 3.2
    thickness = 8
    text_size = cv2.getTextSize(expression, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    max_width = x2 - x1 - 20
    expr = expression

    while text_size[0] > max_width and len(expr) > 1:
        expr = expr[1:]
        text_size = cv2.getTextSize(expr, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]

    text_x = x2 - text_size[0] - 20
    text_y = y2 - 30
    cv2.putText(img, expr, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, DISPLAY_GLOW, thickness, lineType=cv2.LINE_AA)

def draw_history_panel(img, history):
    overlay = img.copy()
    x1, y1, x2, y2 = 850, 80, 1250, 750
    alpha = 0.7
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (28, 28, 28), -1)
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    cv2.putText(img, "History", (880, 130), cv2.FONT_HERSHEY_SIMPLEX, 2.3, TEXT_COLOR, 5, lineType=cv2.LINE_AA)

    max_entries = 7
    for i, entry in enumerate(history[:max_entries]):
        opacity = 1 - (i / max_entries)
        color = (int(150 * opacity + 100), int(255 * opacity + 100), int(150 * opacity + 100))
        font_scale = 1.4
        thickness = 3
        y_pos = 190 + i * 75
        cv2.putText(img, entry, (870, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, lineType=cv2.LINE_AA)

def detect_click(point, buttons):
    for b in buttons:
        cx, cy = b["center"]
        dist = np.hypot(point[0] - cx, point[1] - cy)
        if dist < radius:
            return b
    return None

def draw_hand_feedback(img, index_tip, thumb_tip):
    cv2.circle(img, index_tip, 25, (0, 255, 140), 3)
    cv2.circle(img, thumb_tip, 25, (0, 255, 140), 3)
    cv2.line(img, index_tip, thumb_tip, (0, 255, 140), 4)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1600, 900))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    img[:] = BG_COLOR

    draw_display(img, expression)
    for btn in buttons:
        pressed = btn["pressed"]
        time_since_press = time.time() - btn["press_time"] if pressed else 1
        shrink = 8 * max(0, (0.2 - time_since_press) / 0.2)
        draw_neumorphic_button(img, btn["center"], btn["text"], int(radius - shrink), pressed)

    draw_history_panel(img, history)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        lm = hand_landmarks.landmark
        h, w, _ = img.shape

        index_tip = (int(lm[8].x * w), int(lm[8].y * h))
        thumb_tip = (int(lm[4].x * w), int(lm[4].y * h))

        draw_hand_feedback(img, index_tip, thumb_tip)

        dist = np.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
        current_time = time.time()

        if dist < pinch_threshold:
            btn = detect_click(index_tip, buttons)
            if btn and btn != last_pressed and (current_time - last_click_time) > click_delay:
                btn["pressed"] = True
                btn["press_time"] = current_time

                if btn["text"] == "=":
                    try:
                        result = str(eval(expression))
                        history.insert(0, f"{expression} = {result}")
                        if len(history) > 15:
                            history = history[:15]
                        expression = result
                    except:
                        expression = "Error"
                elif btn["text"] == "C":
                    expression = ""
                else:
                    expression += btn["text"]

                last_pressed = btn
                last_click_time = current_time
        else:
            last_pressed = None

    cv2.imshow("PRO Virtual Calculator", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
