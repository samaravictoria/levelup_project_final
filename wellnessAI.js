export function generateWellnessTasks(emotion) {
  const tasks = {
    happy: [
      "Compartilhe algo bom que aconteceu hoje ✨",
      "Caminhe por 10 minutos 🏃‍♀️",
      "Agradeça alguém do time 💬"
    ],
    sad: [
      "Faça 5 minutos de respiração profunda 🌿",
      "Escute uma música reconfortante 🎧",
      "Escreva 3 linhas sobre seus sentimentos ✍️"
    ],
    angry: [
      "Respiração 4-7-8 por 1 minuto 😮‍💨",
      "Alongue pescoço e ombros 🧘",
      "Faça uma pausa longe da tela 🖥️"
    ],
    neutral: [
      "Beba água 💧",
      "Olhe pela janela por 1 minuto ☀️",
      "Organize sua mesa 📦"
    ],
    fear: [
      "Exercício de grounding dos 5 sentidos ✋",
      "Respire fundo 🌬️",
      "Encontre algo reconfortante perto de você 🫶"
    ]
  };

  return tasks[emotion] || ["Tire um minuto para respirar ❤️"];
}
