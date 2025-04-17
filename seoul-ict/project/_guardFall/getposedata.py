import cv2
import mediapipe as mp

# MediaPipe의 pose 모듈과 그리기 도구 준비
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 웹캠 열기
cap = cv2.VideoCapture(0)

# MediaPipe Pose 객체 만들기 (최적화 옵션 포함)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # BGR → RGB 변환 (MediaPipe는 RGB 이미지만 받음)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 관절 감지
        results = pose.process(image)

        # 다시 RGB → BGR로 변환 (OpenCV용)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 관절이 감지되면 랜드마크 그리기
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # 관절 위치 출력 (예: 오른쪽 무릎)
            right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            print(f"오른쪽 무릎 위치 - x: {right_knee.x}, y: {right_knee.y}, z: {right_knee.z}")

        # 화면에 출력
        cv2.imshow('Pose Tracking', image)

        # 'q'를 누르면 종료
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
