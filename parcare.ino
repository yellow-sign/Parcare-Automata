#include <Stepper.h>
const int stepsPerRevolution = 2048;
const int stepsPerSlot = 1500;

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

int currentSlot = 1;

void setup() {
    Serial.begin(9600);
    myStepper.setSpeed(15);  // RPM
    Serial.println("Ready for slot selection (1-4)");
}

void loop() {
    if (Serial.available()) {
        int targetSlot = Serial.parseInt();
        if (targetSlot >= 1 && targetSlot <= 4 && targetSlot != currentSlot){
            // Calculul numarului de spatii, pasi
            int slotsToMove = (4 + targetSlot - currentSlot) % 4;
            int stepsToMove = -slotsToMove * stepsPerSlot;
            // Negativ pentru a se misca 28BYJ-48 in sensul acelor de ceasornic
            myStepper.step(stepsToMove);
            currentSlot = targetSlot;

            Serial.print("Moved to slot: ");
            Serial.println(currentSlot);
        }
    }
}
