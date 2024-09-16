const exp1 = document.querySelector('.exp-1');
const exp2 = document.querySelector('.exp-2');

exp1.addEventListener('mouseover', () => {
  exp2.classList.add('hidden');
});

exp1.addEventListener('mouseout', () => {
  exp2.classList.remove('hidden');
});

exp2.addEventListener('mouseover', () => {
  exp1.classList.add('hidden');
});

exp2.addEventListener('mouseout', () => {
  exp1.classList.remove('hidden');
});