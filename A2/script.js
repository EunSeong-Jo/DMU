let currentStep = 1;
let totalSaved = 0;
const stepAmount = 100000;
const maxStep = 3;

window.onload = () => {
  totalSaved = parseInt(localStorage.getItem('springSaved') || "0");
  document.getElementById('goalAmount').innerText = (stepAmount * maxStep).toLocaleString();

  const expectedStep = Math.min(Math.floor(totalSaved / stepAmount) + 1, maxStep);
  currentStep = expectedStep;
  moveCharacterToStep(currentStep);
  updateStatus();
};

function saveMoney() {
  totalSaved += 50000;
  localStorage.setItem('springSaved', totalSaved);

  const expectedStep = Math.min(Math.floor(totalSaved / stepAmount) + 1, maxStep);
  if (expectedStep > currentStep) {
    currentStep = expectedStep;
    moveCharacterToStep(currentStep);
  }

  updateStatus();
}

function moveCharacterToStep(stepNumber) {
  const character = document.getElementById("character");
  const step = document.querySelector(`.step${stepNumber}`);
  const stage = document.querySelector(".stage");

  const left = step.offsetLeft + (step.offsetWidth / 2) - (character.offsetWidth / 2);
  const bottom = step.offsetTop + step.offsetHeight;

  character.style.left = `${left}px`;
  character.style.bottom = `${stage.offsetHeight - bottom + 5}px`;
}

function updateStatus() {
  const status = document.getElementById("statusText");
  status.innerText = `현재 저축액: ${totalSaved.toLocaleString()}원`;

  if (currentStep >= maxStep) {
    status.innerText += "\n🎉 목표 달성!";
  }
}
