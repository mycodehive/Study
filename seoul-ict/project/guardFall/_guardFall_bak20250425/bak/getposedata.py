import cv2
import mediapipe as mp
import time

def start_pose_detection():
    # MediaPipe의 pose 모듈과 그리기 도구 준비
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # 웹캠 열기
    cap = cv2.VideoCapture(0)

    # 시간 측정용 변수 초기화
    last_print_time = time.time()

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
                current_time = time.time()
                if current_time - last_print_time >= 3:
                    # 필요한 관절 값 추출
                    landmarks = results.pose_landmarks.landmark
                    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]

                    print("=== 3초마다 출력 ===")
                    print(f"왼쪽 어깨 - x: {left_shoulder.x:.3f}, y: {left_shoulder.y:.3f}, z: {left_shoulder.z:.3f}, 신뢰도: {left_shoulder.visibility}")
                    print(f"오른쪽 어깨 - x: {right_shoulder.x:.3f}, y: {right_shoulder.y:.3f}, z: {right_shoulder.z:.3f}, 신뢰도: {right_shoulder.visibility}")
                    print(f"왼쪽 무릎 - x: {left_knee.x:.3f}, y: {left_knee.y:.3f}, z: {left_knee.z:.3f}, 신뢰도: {left_knee.visibility}")
                    print(f"오른쪽 무릎 - x: {right_knee.x:.3f}, y: {right_knee.y:.3f}, z: {right_knee.z:.3f}, 신뢰도: {right_knee.visibility}")
                    print("====================")

                    last_print_time = current_time  # 마지막 출력 시간 갱신

            # 화면에 출력
            cv2.imshow('Pose Tracking', image)

            # 'q'를 누르면 종료
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# 이 조건을 추가해야 외부에서 import 시 실행되지 않음
if __name__ == "__main__":
    start_pose_detection()