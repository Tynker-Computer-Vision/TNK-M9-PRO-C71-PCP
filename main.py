import cv2
from cvzone.HandTrackingModule import HandDetector
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


def generate_equation():
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)
    operand1 = random.randint(1, 10)
    operand2 = random.randint(1, 10)
    equation = f"{operand1} {operator} {operand2}"
    return equation


def calculate_solution(equation):
    return eval(equation)


def generate_wrong_solution(solution):
    offset = random.randint(1, 5)
    wrong_solution = solution + offset
    return wrong_solution


detector = HandDetector(detectionCon=0.8)

state = "getQuestion"
choice = ""
while True:
    success, cameraFeedImg = cap.read()
    cameraFeedImg = cv2.flip(cameraFeedImg, 1)

    wHeight, wWidth, wChannel = cameraFeedImg.shape

    handsDetector = detector.findHands(cameraFeedImg, flipType=False)
    hands = handsDetector[0]
    cameraFeedImg = handsDetector[1]

    if state == "getQuestion":
        # Generate a random equation
        equation = generate_equation()

        # Calculate the correct solution
        solution = calculate_solution(equation)

        # Generate a wrong solution
        wrong_solution = generate_wrong_solution(solution)

        num = random.randint(0, 2)
        print(num)
        if num == 0:
            option1 = solution
            option2 = wrong_solution
        else:
            option1 = wrong_solution
            option2 = solution

        state = "getAnswer"

    else:

        cameraFeedImg = cv2.putText(cameraFeedImg, str(
            equation), (20, 250), cv2.FONT_HERSHEY_DUPLEX, 1.0, (125, 246, 55), 2)
        cameraFeedImg = cv2.putText(cameraFeedImg, str(round(option1, 2)), (int(
            wWidth/4), 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (125, 246, 55), 2)
        cameraFeedImg = cv2.putText(cameraFeedImg, str(round(option2, 2)), (int(
            wWidth/1.5), 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (125, 246, 55), 2)

        try:
            if hands:
                hand1 = hands[0]
                lmList1 = hand1["lmList"]
                indexFingerTop = lmList1[8]
                indexFingerBottom = lmList1[6]

                # Check which option is selected

                # Check if finger is over the choice area i.e y-axis value is less then 100
                if (indexFingerTop[1] < 100):
                    # There are only two options so check if x-axis of fingerTop is less then wWidth/2
                    if (indexFingerTop[0] < wWidth/2):
                        # Set choice variable to option 1
                        choice = option1
                    else:
                        # Else set the choice variable to option2
                        choice = option2

                    if choice == solution:
                        cameraFeedImg = cv2.putText(cameraFeedImg, "Corret!", (int(
                            wWidth/2.3), int(wHeight/2)), cv2.FONT_HERSHEY_DUPLEX, 1.0, (125, 246, 55), 2)
                    else:
                        cameraFeedImg = cv2.putText(cameraFeedImg, "Wrong!", (int(
                            wWidth/2.3), int(wHeight/2)), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 2)

                    state = "getQuestion"
                    cv2.imshow("Quiz App", cameraFeedImg)
                    cv2.waitKey(0)

        except Exception as e:
            print(e)

    cv2.imshow("Quiz App", cameraFeedImg)
    cv2.waitKey(1)
